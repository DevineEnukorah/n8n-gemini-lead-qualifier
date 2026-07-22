const fs=require('fs');
const path=require('path');
const ROOT=path.resolve(__dirname,'..');
const workflow=JSON.parse(fs.readFileSync(path.join(ROOT,'workflow.json'),'utf8'));
const code=workflow.nodes.find((n)=>n.name==='Build API Response').parameters.jsCode;
const fn=new Function('$json','$execution','$',code);
const source={request_id:'schema-bridge',received_at:'2026-07-22T00:00:00.000Z',security:{suspected_prompt_injection:false}};
const selector=()=>({first:()=>({json:source})});
let seed=42424242;
const rand=()=> (seed=(seed*1664525+1013904223)>>>0)/0x100000000;
const count=Number(process.argv[2] || 5000);
for(let i=0;i<count;i++){
  const raw={
    service_fit_score:Math.floor(rand()*41),
    budget_authority_score:Math.floor(rand()*26),
    urgency_score:Math.floor(rand()*21),
    requirements_clarity_score:Math.floor(rand()*16),
    spam_detected:rand()<0.12,
    summary_reason:'Assessment '+i,
    pain_points:['Manual task','Slow response'],
    suggested_reply:'Thank you for reaching out. Would you be available for a 15-minute discovery call?',
    confidence:Math.floor(rand()*101),
    requires_human_review:rand()<0.15,
  };
  const response=fn({output:raw},{id:'schema-bridge'},selector)[0].json;
  process.stdout.write(JSON.stringify(response.result)+'\n');
}
