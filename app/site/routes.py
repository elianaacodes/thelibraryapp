from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from models import db, User, Book, book_schema, books_schema
from flask_login import current_user


site = Blueprint('site', __name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@site.route('/update')
def update():
    return render_template('update.html')

@site.route('/create_book', methods=['POST'])
def create_book():

    isbn = request.form['isbn']
    year = request.form['year']
    title = request.form['title']
    pages = request.form['pages']
    author = request.form['author']

    
    user_id = current_user.token
    
    # get user info
    
    book = Book(isbn = isbn, year=year, title=title, pages=pages, author=author, user_id = user_id )
    db.session.add(book)
    db.session.commit()
    
    return redirect(url_for('site.books'))


@site.route('/update_book/<isbn>/edit', methods=['POST', 'PUT'])
def update_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()

    if request.method in ['POST', 'PUT']:
        print("I printed!")
        if book:
            book.isbn = request.form['isbn']
            book.year = request.form['year']
            book.title = request.form['title']
            book.pages = request.form['pages']
            book.author = request.form['author']
            book.user_id = current_user.id

            db.session.commit()
            return redirect(url_for('site.books'))
        else:
            return "Book does not exist."
    return render_template('update.html', book=book)

@site.route('/delete_book/<isbn>', methods=['POST'])
def delete_book(isbn):
    book = Book.query.get(isbn)
    if book:
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('site.books'))
    
    
    return redirect(url_for('site.books'))