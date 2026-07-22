#!/usr/bin/env python3
import argparse, json, urllib.request, urllib.error
from pathlib import Path
parser=argparse.ArgumentParser(description='Send a fixture input to an n8n webhook test URL.')
parser.add_argument('url'); parser.add_argument('fixture',type=Path)
args=parser.parse_args()
fixture=json.loads(args.fixture.read_text(encoding='utf-8'))
payload=json.dumps(fixture['input']).encode('utf-8')
request=urllib.request.Request(args.url,data=payload,headers={'Content-Type':'application/json'},method='POST')
try:
 with urllib.request.urlopen(request) as response:
  print('HTTP',response.status); print(response.read().decode())
except urllib.error.HTTPError as error:
 print('HTTP',error.code); print(error.read().decode())
