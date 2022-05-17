from . import bp as api
from .models import *
from flask import make_response, g, request, abort
from app.blueprints.auth.auth import token_auth
from helpers import require_admin

#create a new user (register a User)
@api.post('/user')
def post_user():
    user_dict = request.get_json()
    if not all(key in user_dict for key in ('first_name','last_name','email','password')):
        abort(400)
    # Create an empty User
    user = User()
    # SEt the attributes of that user to the payload
    user.from_dict(user_dict)
    # Save User
    user.save()
    # Send response
    return make_response(f"User {user.first_name} {user.last_name} was created with an id {user.id}",200)

#Edit a user by id
@api.put("/user/<int:id>")
@token_auth.login_required()
def put_user(id):
    user_dict = request.get_json()
    user = User.query.get(id)
    if not user:
        abort(404)
    user.from_dict(user_dict)
    user.save()
    return make_response(f"User {user.first_name} {user.last_name} with ID {user.id} has been updated", 200)


# Delete a user by ID
@api.delete('/user/<int:id>')
@token_auth.login_required()
def delete_user(id):
    user_to_delete = User.query.get(id)
    if not user_to_delete:
        abort(404)
    user_to_delete.delete()
    return make_response(f"User with id: {id} has been deleted", 200)

#books
# Return a list of all books
@api.get('/book')
def get_books():
    # Get all the books in the db
    books = Book.query.all()
    # Turn books to dictionary
    books_dicts= [book.to_dict() for book in books]
    # return the response
    return make_response({"books":books_dicts},200)

# Return book info for book by id
@api.get('/book/<int:id>')
def get_book(id):
    # Look up the book in the database
    book = Book.query.get(id)
    # Verify it exists
    if not book:
        abort(404)
    # Turn book into Dictionary
    book_dict = book.to_dict()
    # return Response
    return make_response(book_dict,200)

# Post->Create a new book
@api.post("/book")
@token_auth.login_required()
@require_admin
def post_book():
    # Get the Payload from the request
    book_dict = request.get_json()
    # Ensure the payload has all the approiate values
    if not all(key in book_dict for key in ('title','author','pages','summary','image','subject','user_id')):
        abort(400)
    # Create an empty book
    book = Book()
    # SEt the attributes of that book to the payload
    book.from_dict(book_dict)
    # Save book
    book.save()
    # Send response
    return make_response(f"Book {book.title} was created with an id {book.id}",200)

#PUT->edit a book by id 
@api.put("/book/<int:id>")
@token_auth.login_required()
@require_admin
def put_book(id):
    book_dict = request.get_json()
    book = Book.query.get(id)
    if not book:
        abort(404)
    book.from_dict(book_dict)
    book.save()
    return make_response(f"book {book.title} with ID {book.id} has been updated", 200)

#DELETE -> delete a book by id
@api.delete('/book/<int:id>')
@token_auth.login_required()
@require_admin
def delete_book(id):
    book_to_delete = Book.query.get(id)
    if not book_to_delete:
        abort(404)
    book_to_delete.delete()
    return make_response(f"Book with id: {id} has been deleted", 200)