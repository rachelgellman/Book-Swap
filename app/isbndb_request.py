import requests
from app.secret import isbndb_key


class ISBNDB():
    def query_isbndb(book, page, pageSize):
        url = 'https://api2.isbndb.com/books/{0}?page={1}&pageSize={2}&column=title&beta=0'.format(book, page, pageSize)
        header = {'Authorization': isbndb_key,
        'Accept': 'application/json'}
        r = requests.get(url, headers=header)

        print("isbdb query status code: " + str(r.status_code))
        return r.json()
        #print(r.json()['books'])
