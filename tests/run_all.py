#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
commands=[
 [sys.executable,str(ROOT/'tests'/'validate_package.py')],
 [sys.executable,str(ROOT/'tests'/'schema_test.py')],
 [sys.executable,str(ROOT/'tests'/'runtime_schema_test.py')],
 ['node',str(ROOT/'tests'/'expression_test.js')],
 ['node',str(ROOT/'tests'/'fixture_validation_test.js')],
 ['node',str(ROOT/'tests'/'runtime_test.js')],
]
for command in commands:
 print('>', ' '.join(command))
 completed=subprocess.run(command,cwd=ROOT)
 if completed.returncode: sys.exit(completed.returncode)
print('ALL LOCAL TESTS PASSED.')
