from buscabook.database import Base
from sqlalchemy import Column, Integer, String, Text

#Tabela dos usuários
class User(Base):
    __tablename__ = 'users'

    id = Column("id",Integer, primary_key=True, index=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

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
