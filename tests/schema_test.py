#!/usr/bin/env python3
from pathlib import Path
import copy, json
from jsonschema import Draft7Validator
ROOT=Path(__file__).resolve().parents[1]
ai=json.loads((ROOT/'schemas'/'ai-assessment.schema.json').read_text())
result=json.loads((ROOT/'schemas'/'lead-qualification.schema.json').read_text())
aiv=Draft7Validator(ai); rv=Draft7Validator(result)
valid_ai={"service_fit_score":35,"budget_authority_score":20,"urgency_score":15,"requirements_clarity_score":12,"spam_detected":False,"summary_reason":"Strong fit.","pain_points":["Manual work"],"suggested_reply":"Would you be available for a 15-minute discovery call?","confidence":90,"requires_human_review":False}
valid_result={"lead_score":82,"category":"Hot","score_breakdown":{"service_fit":35,"budget_authority":20,"urgency":15,"requirements_clarity":12},"spam_detected":False,"summary_reason":"Strong fit.","pain_points":["Manual work"],"suggested_reply":"Would you be available for a 15-minute discovery call?","confidence":90,"requires_human_review":False}
assert not list(aiv.iter_errors(valid_ai)); assert not list(rv.iter_errors(valid_result))
mutations=[]
for key,value in [("service_fit_score",41),("budget_authority_score",-1),("confidence",101),("spam_detected","false")]:
 x=copy.deepcopy(valid_ai); x[key]=value; mutations.append((aiv,x,key))
x=copy.deepcopy(valid_ai); del x['summary_reason']; mutations.append((aiv,x,'missing'))
x=copy.deepcopy(valid_ai); x['extra']='x'; mutations.append((aiv,x,'extra'))
for key,value in [("lead_score",101),("category","Qualified"),("confidence",-1)]:
 x=copy.deepcopy(valid_result); x[key]=value; mutations.append((rv,x,key))
x=copy.deepcopy(valid_result); x['score_breakdown']['service_fit']=41; mutations.append((rv,x,'breakdown'))
x=copy.deepcopy(valid_result); x['pain_points']=['x']*11; mutations.append((rv,x,'pain_points'))
for validator,payload,label in mutations:
 assert list(validator.iter_errors(payload)), f'Mutation should fail: {label}'
print(f'SCHEMA TESTS PASSED: {len(mutations)} invalid mutations rejected.')
