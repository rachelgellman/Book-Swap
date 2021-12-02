from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import SearchForm
from app.isbndb_request import ISBNDB
from app.models import User, Listings, Books

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return render_template('base.html')


@app.route('/browse')
def browse():
    return render_template('browse.html')


@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/book/<isbn>')
def book(isbn):
    b = Books.query.filter_by(isbn = isbn).first()
    if b is None:
        return render_template('book_not_found.html')
    return render_template('book.html', book = b)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = ISBNDB.query_isbndb(form.searchTerm.data)
        flash("" + str(results['total']) + " results")
        for book in results['books']:
            if Books.query.filter_by(isbn = book['isbn13']).first() is None:
                b = Books(isbn = book['isbn13'],
                    name = book['title'],
                    author = ', '.join(book.get('authors', 'N/A')),
                    description = book.get('synopsys', 'N/A'),
                    cover_url = book['image'])
                db.session.add(b)
        db.session.commit()
        return render_template('search_with_books.html', form = form, books = Books.query.filter(Books.name.contains(form.searchTerm.data)).all())
    return render_template('search.html', form = form)
