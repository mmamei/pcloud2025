from requests import get, post
import time

server = 'http://127.0.0.1:8080'
name = 'sensor1'

with open('web2/CleanData_PM10.csv') as f:
    for line in f:
        date, val = line.strip().split(',')
        val = float(val)
        post(f'{server}/sensors/{name}', data={'date':date, 'val':val})
        time.sleep(3)

