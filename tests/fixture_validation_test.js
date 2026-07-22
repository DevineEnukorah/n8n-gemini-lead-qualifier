const fs = require('fs');
const path = require('path');
const assert = require('assert');
const ROOT = path.resolve(__dirname, '..');
const workflow = JSON.parse(fs.readFileSync(path.join(ROOT, 'workflow.json'), 'utf8'));
const code = workflow.nodes.find((n) => n.name === 'Validate and Normalize Input').parameters.jsCode;
const run = (input) => new Function('$json','$execution','$',code)({body:input},{id:'fixture-test'},()=>{})[0].json;
const dir=path.join(ROOT,'tests','fixtures');
let count=0;
for (const file of fs.readdirSync(dir).filter((f)=>f.endsWith('.json'))) {
  const fixture=JSON.parse(fs.readFileSync(path.join(dir,file),'utf8'));
  const output=run(fixture.input);
  if (fixture.expected.http_status === 400) assert.equal(output.valid,false,`${file} should be invalid`);
  else assert.equal(output.valid,true,`${file} should be valid: ${output.errors.join(', ')}`);
  if (fixture.id === 'prompt-injection') assert.equal(output.security.suspected_prompt_injection,true);
  if (fixture.id === 'unicode-normalization') {
    assert.equal(output.lead.name,'Devine');
    assert.equal(output.lead.company,'ACME');
    assert.equal(output.lead.email,'test@example.com');
  }
  count++;
}
console.log(`FIXTURE VALIDATION TESTS PASSED: ${count} fixtures.`);
