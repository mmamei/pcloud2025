from requests import get, post
import time
url = 'https://europe-west8-pcloud2025.cloudfunctions.net/new_data'
name = 'sensor4'

with open('web2/CleanData_PM10.csv') as f:
    for line in f:
        date, val = line.strip().split(',')
        val = float(val)
        post(url, data={'sensor':name, 'date':date, 'val':val})
        time.sleep(3)

