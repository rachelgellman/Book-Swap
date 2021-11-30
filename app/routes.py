from app import app
from flask import render_template


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

@app.route('/search')
def search():
    form =
    return render_template('search.html')