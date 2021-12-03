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
    def query_by_isbn(isbn):
        url = 'https://api2.isbndb.com/book/{0}'.format(isbn)
        header = {'Authorization': isbndb_key,
        'Accept': 'application/json'}
        r = requests.get(url, headers = header)
        print("get by isbn query status code: " + str(r.status_code))
        if str(r.status_code) == '404':
            return None
        return r.json()
