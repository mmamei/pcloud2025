import requests
url = ' http://localhost:8080/upload'
files = {'file': open('upload/test_local_no_gcp/test.jpg','rb')}
values = {'key1':'value1','key2':'value2'}

r = requests.post(url, files=files, data=values)
print(r.status_code)
print(r.text)
