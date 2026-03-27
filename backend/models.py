from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False) # 'admin' or 'student'
    
    issued_books = relationship("IssuedBook", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(50))
    quantity = Column(Integer, nullable=False, default=1)
    category = Column(String(100))
    cover_url = Column(Text)
    
    issued_records = relationship("IssuedBook", back_populates="book")

class IssuedBook(Base):
    __tablename__ = "issued_books"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    issue_date = Column(Date, nullable=False, default=date.today)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="issued") # 'issued' or 'returned'
    fine = Column(Float, default=0.0)
    
    user = relationship("User", back_populates="issued_books")
    book = relationship("Book", back_populates="issued_records")
