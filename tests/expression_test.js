const fs=require('fs');
const path=require('path');
const assert=require('assert');
const ROOT=path.resolve(__dirname,'..');
const workflow=JSON.parse(fs.readFileSync(path.join(ROOT,'workflow.json'),'utf8'));
const selector=(name)=>({first:()=>({json:{request_id:'req',valid:true,errors:[]}})});
const json={valid:true,error:undefined,errors:[],request_id:'req',lead:{name:'A'},security:{suspected_prompt_injection:false}};
let count=0;
function compile(expr){
  new Function('$json','$',`return (${expr});`)(json,selector);
  count++;
}
function walk(value){
  if (typeof value==='string' && value.startsWith('={{') && value.endsWith('}}')) {
    compile(value.slice(3,-2).trim());
  } else if (typeof value==='string' && value.startsWith('=')) {
    const re=/\{\{([\s\S]*?)\}\}/g; let match;
    while ((match=re.exec(value))) compile(match[1].trim());
  } else if (Array.isArray(value)) value.forEach(walk);
  else if (value && typeof value==='object') Object.values(value).forEach(walk);
}
walk(workflow);
assert(count>=7,`Expected at least 7 expressions, got ${count}`);
console.log(`EXPRESSION TESTS PASSED: ${count} expressions compiled and evaluated.`);
