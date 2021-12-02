from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.forms import SearchForm, LoginForm, RegistrationForm
from app.isbndb_request import ISBNDB
from app.models import User, Listings, Books

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
    return render_template('browse.html')


@app.route('/post')
@login_required
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
