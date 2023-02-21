from flask_app import app
from flask import render_template, redirect, request

from flask_app.models.authors_model import Author
from flask_app.models.books_model import Book


# route to show authors list and form to create a new author
@app.route("/authors")
def index():

    # query db for all authors
    authors = Author.get_all()
    return render_template("index.html", authors = authors)


# form submission to add a new author
@app.route("/new_author", methods=["POST"])
def new_author():
    
    # query db to create a new author
    Author.save(request.form)
    return redirect("/authors")





# route to show one author's page
@app.route("/authors/<int:author_id>")
def show_author(author_id):

    # query db for one author with favorites
    author = Author.get_author_with_favorites({"id": author_id})

    # query db for all books to display in dropdown
    books = Author.get_author_non_favorites({"id": author_id})

    return render_template("show_author.html", author = author, books=books)


# form submission for adding a favorite from the authors page
@app.route("/author_favorite", methods=["POST"])
def author_favorite():

    Author.new_favorite(request.form)
    return redirect(f"/authors/{request.form['author_id']}")