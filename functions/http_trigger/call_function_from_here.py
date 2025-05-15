from requests import post

url = 'https://europe-west8-pcloud2025.cloudfunctions.net/hello_http/'
r = post(url,json={'name':'matteo'})
print(r.status_code)
print(r.text)

