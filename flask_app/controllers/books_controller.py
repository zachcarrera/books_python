from flask_app import app
from flask import render_template, redirect, request

from flask_app.models.books_model import Book
from flask_app.models.authors_model import Author



# route to show list of all books and form to create a new book
@app.route("/books")
def books():

    # query db for all books
    books = Book.get_all()
    return render_template("books.html", books = books)

# form submission to add a new book
@app.route("/new_book", methods=["POST"])
def new_book():
    
    # query db to create a new book
    Book.save(request.form)
    return redirect("/books")




# route to show one book's page
@app.route("/books/<int:book_id>")
def show_book(book_id):

    # query db for one book with all favorites
    book = Book.get_book_with_favorites({"id": book_id})

    # query db for all authors to display in dropdown
    authors = Book.get_book_non_favorites({"id": book_id})


    return render_template("show_book.html", book = book, authors = authors)


# form submission from book's page to add a favorite
@app.route("/book_favorite", methods=["POST"])
def favorite_book():

    print(request.form)

    Book.new_favorite(request.form)
    return redirect(f"/books/{request.form['book_id']}")