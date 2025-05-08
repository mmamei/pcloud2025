import requests
sensor = 'sensor3'
import time
url = f'http://155.185.122.230:8080/sensorsfile/{sensor}'

day = 11
for i in range(10):
    files = {
        'file': (f'{day}-04-2025.csv', open('riepilogo1/CleanData_PM10.csv', 'rb'))
    }

    r = requests.post(url, files=files)
    print(r.status_code)
    print(r.text)
    day += 1
    time.sleep(10)
