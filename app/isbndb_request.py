import requests
import secret

header = {'Authorization': secret.isbndb_key,
'Accept': 'application/json'}

url = 'https://api2.isbndb.com/books/{0}?{1}'.format('dune', 'page=1&pageSize=1000&column=title&beta=0')

r = requests.get(url, headers=header)

print(r.status_code)
print(r.json()['total'])
