from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myProject'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'

sql = SQLAlchemy(app)


class Book_info(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.VARCHAR(50))
    author = sql.Column(sql.VARCHAR(25))


    def __str__(self):
        return f"Book Title: {self.title};\nBook Author: {self.author}"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if user == '' or email == '' or password == '':
            flash('შეიტანეთ ყველა ველი', 'error')
        else:
            session['username'] = user
            return redirect(url_for('user_page'))
    return render_template('login.html')


@app.route('/user_page')
def user_page():
    return render_template('user_page.html')


@app.route('/add_books', methods=['POST', 'GET'])
def add_books():
    if request.method == 'POST':
        t = request.form['title']
        a = request.form['author']
        if t=='' or a=='':
            flash('შეიტანეთ ყველა ველი', 'error')
        else:
            b1 = Book_info(title=t, author=a)
            sql.session.add(b1)
            sql.session.commit()
            flash('წიგნი დამატებულია', 'info')
    return render_template('add_books.html')


@app.route('/book_page')
def book_page():
    all_books = Book_info.query.all()
    return render_template('book_page.html', all_books= all_books)


@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('logout.html')


if __name__ == "__main__":
    app.run(debug=True)