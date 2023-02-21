from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import authors_model

class Book:

    # constant to hold db name
    DB = "books_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.num_of_pages = data["num_of_pages"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # empty list to show favorited authors
        self.author_favorites = []



    # CREATE
    @classmethod
    def save(cls, data):

        # insert query
        query = """INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"""

        # return id of newly created row in books
        return connectToMySQL(cls.DB).query_db(query,data)

    
    @classmethod
    def new_favorite(cls, data):

        #insert query
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s,%(author_id)s);"

        return connectToMySQL(cls.DB).query_db(query,data)


    # READ 
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"

        results = connectToMySQL(cls.DB).query_db(query)

        books = []
        
        for result in results:
            books.append(cls(result))
        
        return books

    @classmethod
    def get_book_with_favorites(cls, data):
        # get an instance of a book with all its favorited authors


        query = """
            SELECT * FROM books 
            LEFT JOIN favorites ON books.id = favorites.book_id
            LEFT JOIN authors ON favorites.author_id = authors.id
            WHERE books.id = %(id)s;"""

        results = connectToMySQL(cls.DB).query_db(query,data)

        book = cls(results[0])

        for row in results:
            author_data = {
                **row,
                "id" : row["authors.id"],
                "created_at" : row["authors.created_at"],
                "updated_at" : row["authors.updated_at"]
            }

            book.author_favorites.append(authors_model.Author(author_data))

        return book


    @classmethod
    def get_book_non_favorites(cls,data):
        # method to return a list of all authors
        # not favorited by a given book


        # check the list of favorites and if it is empty,
        # then return a list of all authors
        if not cls.get_book_with_favorites(data).author_favorites[0].id:
            return authors_model.Author.get_all()
        
        query = """
                SELECT * FROM authors
                WHERE id NOT IN
                (SELECT favorites.author_id FROM favorites
                LEFT JOIN authors ON favorites.author_id = authors.id
                WHERE book_id = %(id)s);"""

        results = connectToMySQL(cls.DB).query_db(query,data)

        authors = []

        for row in results:
            authors.append(authors_model.Author(row))
        
        return authors