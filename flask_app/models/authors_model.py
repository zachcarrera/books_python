from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import books_model

class Author:

    # constant to hold db name
    DB = "books_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # empty list to hold Book instances
        self.favorite_books = []


    # CREATE
    @classmethod
    def save(cls, data):

        # insert query
        query = """INSERT INTO authors (name) VALUES (%(name)s);"""

        # return id of newly created row in authors
        return connectToMySQL(cls.DB).query_db(query,data)



    @classmethod
    def new_favorite(cls, data):

        #insert query
        query = "INSERT INTO favorites (book_id, author_id) VALUES (%(book_id)s,%(author_id)s);"

        return connectToMySQL(cls.DB).query_db(query,data)



    # READ 
    @classmethod
    def get_all(cls):

        # select query
        query = "SELECT * FROM authors;"
        results = connectToMySQL(cls.DB).query_db(query)

        # map query results to Author instances
        authors = []
        for result in results:
            authors.append(cls(result))
        
        return authors


    @classmethod
    def get_author_with_favorites(cls, data):
        # get an author instance with all their favorites attached


        # select query
        query = """
            SELECT * FROM authors 
            LEFT JOIN favorites ON favorites.author_id = authors.id
            LEFT JOIN books ON books.id = favorites.book_id
            WHERE authors.id = %(id)s;"""

        results = connectToMySQL(cls.DB).query_db(query,data)

        # make an Author instance and populate author.favorite_books with Book instances
        author = cls(results[0])

        
        
        # if results[0]["books.id"] is None:
        #     return author


        for row in results:
            book_data = {
                **row, 
                "id" : row["books.id"],
                "created_at" : row["books.created_at"],
                "updated_at" : row["books.updated_at"]
            }

            author.favorite_books.append(books_model.Book(book_data))
        
        return author

    @classmethod
    def get_author_non_favorites(cls,data):
        # a method to return all books not favorited by the book

        # when an author has no favorites, 
        # return a list of all books
        if not cls.get_author_with_favorites(data).favorite_books[0].id:
            return books_model.Book.get_all()
        

        query = """
            SELECT * FROM books
            WHERE id NOT IN
                (SELECT favorites.book_id FROM authors 
                LEFT JOIN favorites ON favorites.author_id = authors.id
                WHERE authors.id = %(id)s);"""

        results = connectToMySQL(cls.DB).query_db(query,data)



        books = []
                
        for row in results:
            books.append(books_model.Book(row))
        
        return books