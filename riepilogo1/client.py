from requests import get
import json

server = 'http://127.0.0.1:8080'
sensor = 'sensor1'

r = get(f'{server}/sensors/{sensor}')
data = json.loads(r.text)
max = 0
for d in data:
    if d['val'] > max:
        max = d['val']  
print(max)