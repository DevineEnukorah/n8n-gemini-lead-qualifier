#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
from jsonschema import Draft7Validator
ROOT=Path(__file__).resolve().parents[1]
schema=json.loads((ROOT/'schemas'/'lead-qualification.schema.json').read_text())
validator=Draft7Validator(schema)
count=5000
completed=subprocess.run(['node',str(ROOT/'tests'/'runtime_samples.js'),str(count)],capture_output=True,text=True,check=True)
lines=[line for line in completed.stdout.splitlines() if line.strip()]
assert len(lines)==count, (len(lines),count)
for index,line in enumerate(lines):
    payload=json.loads(line)
    errors=list(validator.iter_errors(payload))
    assert not errors, f'Runtime output {index} failed schema: {errors}'
print(f'RUNTIME-SCHEMA BRIDGE PASSED: {count} generated outputs validated.')
