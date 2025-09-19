from buscabook.database import Base
from sqlalchemy import Column, Integer, String, Text
import json

#Tabela dos usuários
class User(Base):
    __tablename__ = 'users'

    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    saved_books = Column("saved_books" ,Text, default="[]")

    def __init__(self, name, email, password, savade_books):
        self.name = name
        self.email = email
        self.password = password
        self.saved_books = savade_books
    
    def add_book(self, book_id):

        books = json.loads(self.saved_books)
        if book_id not in books:
            books.append(book_id)
        self.saved_books = json.dumps(books)

    def remove_book(self, book_id):

        books = json.loads(self.saved_books)
        if book_id in books:
            books.remove(book_id)
        self.saved_books = json.dumps(books)

    def get_books(self):
        return json.loads(self.saved_books)

#Tabela dos livros
class Book(Base):
    __tablename__ = 'books'

    id = Column("id", Integer, primary_key=True, index=True)
    title = Column("title", String, nullable=False)
    description = Column("description", Text, nullable=False)
    authors = Column("authors", Text, nullable=False)
    cover = Column("cover", String, nullable=False)
    publish_date = Column("publish_date", String, nullable=False)
    categories = Column("categories", Text, nullable=False)
    language = Column("language", String, nullable=False)
    info_link = Column("info_link", String)
    page_count = Column("page_count", Integer, nullable=False)

    def __init__(self, title, description, authors, cover, publish_date, categories, language, info_link, page_count):

        self.title = title
        self.description = description
        self.authors = authors
        self.cover = cover
        self.publish_date = publish_date
        self.categories = categories
        self.language = language
        self.info_link = info_link
        self.page_count = page_count
