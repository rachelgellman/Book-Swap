from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import SearchForm, LoginForm, RegistrationForm, ButtonForm
from app.isbndb_request import ISBNDB
from app.models import User, Listings, Books
from app.secret import admin_pass
import time, math

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/browse')
def browse():
    listings = Listings.query.all()
    return render_template('browse.html', listings = listings)


@app.route('/post', methods=['GET','POST'])
@login_required
def post_search():
    form = SearchForm()
    if form.validate_on_submit():
        results = ISBNDB.query_isbndb(form.searchTerm.data, 1, 1000)
        if results['total'] == 0:
            flask("No Books with name {}".format(form.searchTerm.data))
            return redirect(url_for('post'))
        pages = math.ceil(results['total']/ 1000)
        flash("" + str(results['total']) + " results")
        books = {}
        i = 1
        while i <= pages:
            for book in results['books']:
                if Books.query.filter_by(isbn = book.get('isbn13', -1)).first() is None and not book.get('isbn13', -1) in books.keys():
                    b = Books(isbn = book['isbn13'],
                        name = book['title'],
                        author = ', '.join(book.get('authors', 'N/A')),
                        description = book.get('synopsys', 'N/A'),
                        cover_url = book['image'])
                    books[book['isbn13']] = b
            i += 1
            if i <= pages:
                time.sleep(1)
                results = ISBNDB.query_isbndb(form.searchTerm.data, i, 1000)
        db.session.add_all(books.values())
        db.session.commit()
        return render_template('post_with_books.html', form = form, books = Books.query.filter(Books.name.contains(form.searchTerm.data)).all())
    return render_template('search.html', form = form)

@app.route('/post/<isbn>', methods=['GET','POST'])
def post(isbn):
    b = Books.query.filter_by(isbn = isbn).first()
    if b is None:
        book = ISBNDB.query_by_isbn(isbn)
        if book == None:
            return render_template('book_not_found.html')
        book = book['book']
        b = Books(isbn = book['isbn13'],
            name = book['title'],
            author = ', '.join(book.get('authors', 'N/A')),
            description = book.get('synopsys', 'N/A'),
            cover_url = book['image'])
        db.session.add(b)
        db.session.commit()
    form = ButtonForm()
    form.submit.label.text = 'Post'
    if form.validate_on_submit():
        l = Listings(bid = b.id, uid = current_user.id, state = 'active')
        db.session.add(l)
        db.session.commit()
        current_user.listings.append(l)
        b.listings.append(l)

    return render_template('post.html', book = b, form = form)

@app.route('/book/<isbn>')
def book(isbn):
    b = Books.query.filter_by(isbn = isbn).first()
    if b is None:
        book = ISBNDB.query_by_isbn(isbn)
        if book == None:
            return render_template('book_not_found.html')
        book = book['book']
        b = Books(isbn = book['isbn13'],
            name = book['title'],
            author = ', '.join(book.get('authors', 'N/A')),
            description = book.get('synopsys', 'N/A'),
            cover_url = book['image'])
        db.session.add(b)
        db.session.commit()
    return render_template('book.html', book = b)

@app.route('/search', methods=['GET','POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if current_user.username != 'admin':
            flash("Must Be Admin")
            return redirect(url_for('index'))
        results = ISBNDB.query_isbndb(form.searchTerm.data, 1, 1000)
        if results['total'] == 0:
            flask("No Books with name {}".format(form.searchTerm.data))
            return redirect(url_for('search'))
        pages = math.ceil(results['total']/ 1000)
        flash("" + str(results['total']) + " results")
        books = {}
        i = 1
        while i <= pages:
            for book in results['books']:
                if Books.query.filter_by(isbn = book.get('isbn13', -1)).first() is None and not book.get('isbn13', -1) in books.keys():
                    b = Books(isbn = book['isbn13'],
                        name = book['title'],
                        author = ', '.join(book.get('authors', 'N/A')),
                        description = book.get('synopsys', 'N/A'),
                        cover_url = book['image'])
                    books[book['isbn13']] = b
            i += 1
            if i <= pages:
                time.sleep(1)
                results = ISBNDB.query_isbndb(form.searchTerm.data, i, 1000)
        db.session.add_all(books.values())
        db.session.commit()
        return render_template('search_with_books.html', form = form, books = Books.query.filter(Books.name.contains(form.searchTerm.data)).all())
    return render_template('search.html', form = form)

@app.route('/resetdb')
@login_required
def resetdb():
    if current_user.username != 'admin':
        flash("Must Be Admin")
        return redirect(url_for('index'))
    flash("Resetting database")
    logout_user()
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear Table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    user = User(username='admin', email = 'swelsh3@ithaca.edu')
    user.set_password(admin_pass)
    book = Books(isbn = -1, name = '', author = '', description = 'N/A', cover_url = 'https://images.isbndb.com/covers/29/24/9780397312924.jpg')
    db.session.add_all([user, book])
    db.session.commit()
    return redirect(url_for('index'))
