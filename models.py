from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable = False, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    books = db.relationship('Book', backref='user', lazy = True)

    def __init__(self, email='', first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash


    def __repr__(self):
        return f'User {self.email} has been added to the database.'
    
class Contact(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = False)
    last_name = db.Column(db.String(150), nullable = False)
    email = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, first_name, last_name, email, phone_number, address, user_token, id = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.user_token = user_token


    def __repr__(self):
        return f'The following contact has been added to the phonebook: {self.first_name} {self.last_name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class ContactSchema(ma.Schema):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'email','phone_number', 'address']

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)


class Book(db.Model):
    isbn = db.Column(db.String(17), primary_key=True)
    year = db.Column(db.Integer, unique = False, nullable = False)
    title = db.Column(db.String(75), unique = False, nullable = False)
    pages = db.Column(db.Integer,  unique = False, nullable = False)
    author = db.Column(db.String, unique = False, nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    
    def __init__(self,  isbn, year, title, pages, author,  user_id):
        self.isbn = isbn
        self.year = year
        self.title = title
        self.pages = pages
        self.author = author 
        self.user_id = user_id
    
    
    def __repr__(self):
        return f'{self.title} has been added to the library'
    
 
class BookSchema(ma.Schema):
    class Meta:
        fields = ['isbn', 'year', 'title', 'pages', 'author', 'user_id']

book_schema = BookSchema()
books_schema = BookSchema(many=True)