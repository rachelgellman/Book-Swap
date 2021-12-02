from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import SearchForm
from app.isbndb_request import ISBNDB

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

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.searchTerm.data)
        ISBNDB.query_isbndb(form.searchTerm.data)
    return render_template('search.html', form = form)
