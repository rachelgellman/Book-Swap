import requests
import secret


class ISBNDB():
    header = {'Authorization': secret.isbndb_key,
    'Accept': 'application/json'}


    def query_isbndb(book):
        query_url = 'https://api2.isbndb.com/books/{0}?{1}'.format(book, 'page=1&pageSize=1000&column=title&beta=0')

        r = requests.get(url, headers=header)

        print(r.status_code)
        print(r.json()['books'])
