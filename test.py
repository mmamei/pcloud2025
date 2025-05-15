from requests import post,get
url = 'http://mamei-nb-leonida.tamburini.unimo.it:20880'
#get_url = f'{url}/health'
#response = get(get_url)
#print(response.text)

post_url = f'{url}/predict'
headers = {"Content-Type": "application/json"}
data = {
   "date": "2025-06-01",
    "layerid": "08|037|025|000|000"
}
response = post(post_url, headers=headers, json=data)
print(response.status_code)
print(response.text)
