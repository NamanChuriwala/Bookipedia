from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reviews = db.relationship('Reviews', backref='book', lazy=True)
    title = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20))
    year = db.Column(db.Integer)
    author = db.Column(db.String(100))
    num_rating = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False,
                         unique=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text())
    rating = db.Column(db.Integer)
    bookid = db.Column(db.ForeignKey('books.id'), nullable=False)
