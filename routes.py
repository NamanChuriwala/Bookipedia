from flask import current_app as app
from flask import render_template
from flask import request, redirect, url_for
from flask_login import current_user, login_required, logout_user
from models import db, Books, Reviews
from forms import *

@app.route('/books/<bookname>', methods=['GET', 'POST'])
@login_required
def display_books(bookname):
    form = AddReview(request.form)
    book = Books.query.filter_by(title=bookname).first()
    if request.method == 'POST':
        added = verify_review(form=request.form, book=book)
        if added:
            return redirect(url_for('home'))
        return render_template('display_book.html', book=book,
                                user=current_user, form=AddReview(None),
                                message='Could not add review!')
    return render_template('display_book.html', book=book,
                            user=current_user, form=AddReview(None),
                            message='Add a review for this book?')

@app.route('/reviews/<id>')
@login_required
def display_review(id):
    try:
        reviews = Reviews.query.filter_by(bookid=id).all()
    except:
        reviews = []
    return render_template('display_review.html', reviews=reviews)

@app.route('/authors/<authorname>')
@login_required
def display_author(authorname):
    books = Books.query.filter_by(author=authorname).all()
    return render_template('display_author.html', books=books,
                            author=authorname)

def verify_review(form, book):
    rating = form.get('rating')
    review = form.get('review')
    review = Reviews(text=review, bookid=book.id)
    if rating:
        rating = int(rating)
        review.rating = rating
    try:
        db.session.add(review)
        db.session.commit()
        if rating:
            book.avg_rating = ((book.num_rating * book.avg_rating) + rating) / (book.num_rating + 1)
            book.num_rating += 1
            db.session.add(book)
            db.session.commit()
    except Exception as e:
        print(e)
        return False
    return True

def add_book(form):
    title = form.get('title')
    author = form.get('author')
    isbn = form.get('isbn')
    book = Books(title=title, author=author, isbn=isbn)
    year = form.get('year')
    if year:
        year = int(year)
        book.year = year
    review = form.get('review')
    rating = form.get('rating')
        
    try:
        db.session.add(book)
        db.session.commit()
    except Exception as e:
        print(e)
        return False
    book = Books.query.filter_by(title=title).first()
    if rating:
        rating = int(form.get('rating'))
        book.num_rating = 1
        book.avg_rating = rating
        review = Reviews(rating=rating, text=review, bookid=book.id)
    try:
        db.session.add(book)
        db.session.add(review)
        db.session.commit()
    except:
        return False
    return True

def find_book(form):
    title = request.form.get('title')
    title = "%{}%".format(title)
    try:
        books = Books.query.filter(Books.title.like(title)).all()
    except:
        return False
    if not books:
        return False
    print(books)
    return books

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/add_books', methods=['GET', 'POST'])
@login_required
def add_books():
    form = AddBook(request.form)
    message = 'Add Book'
    if request.method == 'POST' and form.validate_on_submit():
        added = add_book(request.form)
        if added:
            message = 'Book Added Successfully!'
        else:
            message = 'Book Already Exists'
        return render_template('add_books.html', form=AddBook(None),
                                message=message)
    return render_template('add_books.html', form=form,
                            message=message)

@app.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = FindBook(request.form)
    if request.method == 'GET':
        if form.errors:
            message = 'Book not found! Please retry or add book!!'
        else:
            message = 'Find a book to add a review!'
        return render_template('find_books.html',
                                form=FindBook(None),
                                message=message)

    if form.validate_on_submit():
        found = find_book(request.form)
        if found:
            books = found
            message = 'Select a book to add review!'
        else:
            books = []
            message = 'Book not found! Please retry or add book!'
        return render_template('find_books.html', form=FindBook(None),
                                books=books, message=message)


@app.route('/find_books', methods=['GET', 'POST'])
@login_required
def find_books():
    form = FindBook(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        found = find_book(request.form)
        if found:
            books = found
            message = 'Book Found!'
        else:
            books = []
            message = 'Book not found!'
        return render_template('find_books.html', form=FindBook(None),
                                books=books, message=message)
    return render_template('find_books.html', form=form, books=[],
                            message='Look for your book here')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
