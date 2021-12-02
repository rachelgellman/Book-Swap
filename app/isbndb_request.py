import requests
from app.secret import isbndb_key


class ISBNDB():
    def query_isbndb(book):
        url = 'https://api2.isbndb.com/books/{0}?{1}'.format(book, 'page=1&pageSize=1000&column=title&beta=0')
        header = {'Authorization': isbndb_key,
        'Accept': 'application/json'}
        r = requests.get(url, headers=header)

        print("isbdb query status code: " + str(r.status_code))
        return r.json()
        #print(r.json()['books'])
