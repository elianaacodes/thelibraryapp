from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Contact, contact_schema, contacts_schema, Book, book_schema, books_schema, check_password_hash
from flask_login import login_user

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/syncFirebaseLogin', methods=['POST'])
def sync_firebase_login():

    email = request.json['email']
    uid = request.json['uid']

    logged_user = User.query.filter(User.email == email).first()
    if logged_user and check_password_hash(logged_user.password, uid):
        login_user(logged_user)
    else:
        logged_user = User(email, password = uid)
        db.session.add(logged_user)
        db.session.commit()

    return jsonify({"id":logged_user.id, "token": logged_user.token})


@api.route('/contacts', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    phone_number = request.json['phone_number']
    address = request.json['address']
    user_token = current_user_token.token

    print(f'Library: {current_user_token.token}')

    contact = Contact(first_name, last_name, email, phone_number, address, user_token = user_token )

    db.session.add(contact)
    db.session.commit()

    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_contacts(current_user_token):
    a_user = current_user_token.token
    contacts = Contact.query.filter_by(user_token = a_user).all()
    response = contacts_schema.dump(contacts)
    return jsonify(response)


@api.route('/contacts/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Contact.query.get(id)
    response = contact_schema.dump(contact)
    return jsonify(response)


@api.route('/contacts/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    contact = Contact.query.get(id) 
    contact.email = request.json['email']
    contact.first_name = request.json['first_name']
    contact.last_name = request.json['last_name']
    contact.phone_number = request.json['phone_number']
    contact.address = request.json['address']
    contact.user_token = current_user_token.token

    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)

@api.route('/contacts/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    response = contact_schema.dump(contact)
    return jsonify(response)


@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    year = request.json['year']
    title = request.json['title']
    pages = request.json['pages']
    author = request.json['author']
    user_id = current_user_token.token 
    
    
    book = Book(isbn, year, title, pages, author, user_id = user_id)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)



@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    user_id = current_user_token.token 
    books = Book.query.filter_by(user_id = user_id).all()
    response = books_schema.dump(books)
    return jsonify(response)


@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book_Token = current_user_token.token
    if book_Token == current_user_token.token:
        book = Book.query.get(id)
        response = book_schema.dump(book)
        return jsonify(response)
    else:
        return jsonify({'message': "Invalid Token"}), 401


@api.route('/books/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id) 
    book.isbn = request.json['isbn']
    book.year = request.json['year']
    book.title = request.json['title']
    book.pages = request.json['pages']
    book.author = request.json['author']
    book.user_id = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)