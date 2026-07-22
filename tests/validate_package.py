#!/usr/bin/env python3
from pathlib import Path
import json, re, sys, uuid, yaml
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def fail(message): errors.append(message)
try: workflow=json.loads((ROOT/'workflow.json').read_text(encoding='utf-8'))
except Exception as e: print(f'Invalid workflow JSON: {e}'); sys.exit(1)
try: ai_schema=json.loads((ROOT/'schemas'/'ai-assessment.schema.json').read_text())
except Exception as e: fail(f'Invalid AI schema: {e}'); ai_schema={}
try: result_schema=json.loads((ROOT/'schemas'/'lead-qualification.schema.json').read_text())
except Exception as e: fail(f'Invalid result schema: {e}'); result_schema={}

if workflow.get('active') is not False: fail('Workflow must be inactive in source control.')
if (ROOT/'VERSION').read_text().strip()!='1.1.0': fail('VERSION must be 1.1.0.')
try: uuid.UUID(workflow.get('versionId',''))
except Exception: fail('versionId must be a valid UUID.')

nodes=workflow.get('nodes',[]); names=[n.get('name') for n in nodes]; ids=[n.get('id') for n in nodes]
if len(names)!=len(set(names)): fail('Node names must be unique.')
if len(ids)!=len(set(ids)): fail('Node IDs must be unique.')
for node_id in ids:
 try: uuid.UUID(node_id)
 except Exception: fail(f'Node ID is not UUID: {node_id}')
required={'Lead Webhook','Validate and Normalize Input','Input Valid?','Qualify Lead','Google Gemini Chat Model','Structured Output Parser','AI Processing Succeeded?','Build API Response','Return Validation Error','Return Processing Error','Return Qualification'}
missing=required-set(names)
if missing: fail(f'Missing nodes: {sorted(missing)}')
node_by_name={n['name']:n for n in nodes}

# Graph references and reachability on main connections
connections=workflow.get('connections',{})
for source,groups in connections.items():
 if source not in node_by_name: fail(f'Connection source missing: {source}')
 for output_type,outputs in groups.items():
  for branch in outputs:
   if branch:
    for edge in branch:
     if edge['node'] not in node_by_name: fail(f"Connection target missing: {edge['node']}")

adj={name:[] for name in names}
for source,groups in connections.items():
 for branch in groups.get('main',[]):
  if branch:
   adj[source].extend(edge['node'] for edge in branch)
seen=set(); stack=['Lead Webhook']
while stack:
 current=stack.pop()
 if current in seen: continue
 seen.add(current); stack.extend(adj.get(current,[]))
main_nodes={n['name'] for n in nodes if not n['type'].startswith('@n8n/n8n-nodes-langchain.lm') and 'outputParser' not in n['type']}
unreachable=main_nodes-seen
if unreachable: fail(f'Unreachable main-flow nodes: {sorted(unreachable)}')

# Node versions and critical settings
expected_versions={'Lead Webhook':2.1,'Validate and Normalize Input':2,'Input Valid?':2.2,'Qualify Lead':1.9,'Google Gemini Chat Model':1.1,'Structured Output Parser':1.3,'AI Processing Succeeded?':2.2,'Build API Response':2,'Return Validation Error':1.5,'Return Processing Error':1.5,'Return Qualification':1.5}
for name,ver in expected_versions.items():
 if node_by_name[name].get('typeVersion')!=ver: fail(f'{name} typeVersion must be {ver}.')
for name in ['Input Valid?','AI Processing Succeeded?']:
 if node_by_name[name]['parameters']['conditions']['options'].get('version') != 2: fail(f'{name} IF condition version must be 2.')
webhook=node_by_name['Lead Webhook']
if webhook['parameters'].get('httpMethod')!='POST' or webhook['parameters'].get('responseMode')!='responseNode': fail('Webhook must be POST with responseNode mode.')
try: uuid.UUID(webhook.get('webhookId',''))
except Exception: fail('webhookId must be a UUID.')
if not re.fullmatch(r'[a-z0-9-]+',webhook['parameters'].get('path','')): fail('Webhook path contains unsafe characters.')

qualify=node_by_name['Qualify Lead']
if qualify.get('onError')!='continueRegularOutput': fail('Qualify Lead must route model failures into the normal output.')
if not qualify['parameters'].get('hasOutputParser'): fail('Qualify Lead must use the output parser.')
for phrase in ['untrusted data','service_fit_score','spam_detected','No reply recommended.','JSON.stringify($json.lead)','Do not reproduce HTML']:
 if phrase not in qualify['parameters'].get('text',''): fail(f'Embedded prompt missing: {phrase}')
model=node_by_name['Google Gemini Chat Model']
if model['parameters'].get('modelName')!='models/gemini-3.1-flash-lite': fail('Unexpected Gemini model.')
opts=model['parameters'].get('options',{})
if opts.get('temperature',1)>0.2: fail('Temperature is too high for structured qualification.')
parser=node_by_name['Structured Output Parser']
if parser['parameters'].get('autoFix') is not False: fail('Parser autoFix must be false without an extra parser model.')
try: embedded=json.loads(parser['parameters']['inputSchema'])
except Exception as e: fail(f'Embedded parser schema invalid: {e}'); embedded={}
if embedded!=ai_schema: fail('Embedded parser schema does not match ai-assessment.schema.json.')

codes={n['name']:n['parameters']['jsCode'] for n in nodes if n['type']=='n8n-nodes-base.code'}
for name,code in codes.items():
 if 'console.log' in code or 'console.error' in code: fail(f'{name} must not log lead data.')
 if len(code)<100: fail(f'{name} code appears incomplete.')

responses={'Return Validation Error':400,'Return Processing Error':502,'Return Qualification':200}
for name,status in responses.items():
 node=node_by_name[name]
 if node['parameters']['options'].get('responseCode')!=status: fail(f'{name} response code must be {status}.')
 headers=node['parameters']['options'].get('responseHeaders',{}).get('entries',[])
 header_map={h.get('name','').lower():h.get('value') for h in headers}
 if header_map.get('cache-control')!='no-store': fail(f'{name} missing Cache-Control no-store.')
 if header_map.get('x-content-type-options')!='nosniff': fail(f'{name} missing nosniff header.')

# No secrets or persisted credential identifiers
serialized=json.dumps(workflow).lower()
for token in ['sk-', 'api_key=', 'bearer ', '"password":']:
 if token in serialized: fail(f'Potential secret token found: {token}')
for node in nodes:
 creds=node.get('credentials',{})
 for value in creds.values():
  if isinstance(value,dict) and (value.get('id') or value.get('name')): fail(f'Credential reference exported in {node["name"]}.')

# Docs, fixtures, CI
for filename in ['tests/runtime_test.js','tests/expression_test.js','tests/fixture_validation_test.js','tests/schema_test.py','tests/runtime_schema_test.py','tests/runtime_samples.js','tests/send_fixture.py','README.md','SECURITY.md','PRIVACY.md','CHANGELOG.md','LICENSE','system-prompt.md','tests/LIVE_TEST_PLAN.md','marketplace/listing.md','TEST_REPORT.md','MANUAL_GITHUB_PUBLISH.md']:
 if not (ROOT/filename).is_file(): fail(f'Missing file: {filename}')
fixtures=list((ROOT/'tests'/'fixtures').glob('*.json'))
if len(fixtures)<15: fail('At least 15 fixtures are required.')
for fixture in fixtures:
 try: data=json.loads(fixture.read_text())
 except Exception as e: fail(f'Invalid fixture {fixture.name}: {e}'); continue
 if not isinstance(data.get('input'),dict) or not isinstance(data.get('expected'),dict): fail(f'Malformed fixture: {fixture.name}')
try:
 ci=yaml.safe_load((ROOT/'.github/workflows/validate.yml').read_text())
 if not isinstance(ci,dict): fail('CI workflow is invalid YAML.')
except Exception as e: fail(f'CI workflow YAML invalid: {e}')

if errors:
 print('PACKAGE VALIDATION FAILED')
 for error in errors: print('-',error)
 sys.exit(1)
print(f'PACKAGE VALIDATION PASSED: {len(nodes)} nodes, {len(fixtures)} fixtures, graph and security checks complete.')
