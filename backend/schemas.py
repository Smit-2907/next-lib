from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# User schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: str = "student"

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

# Book schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: Optional[str] = None
    quantity: int = Field(1, ge=0)
    category: Optional[str] = None
    cover_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    quantity: Optional[int] = None

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True

# Issue Book schemas
class IssueRequest(BaseModel):
    book_id: int
    user_id: Optional[int] = None  # If student, this is inferred from auth

class ReturnRequest(BaseModel):
    issue_id: int

class IssuedBook(BaseModel):
    id: int
    book_id: int
    user_id: int
    issue_date: date
    due_date: date
    return_date: Optional[date] = None
    status: str
    fine: float
    book_title: Optional[str] = None
    student_name: Optional[str] = None

    class Config:
        from_attributes = True

# Stats schema
class LibrarySummary(BaseModel):
    total_books: int
    available_books: int
    issued_books: int
    total_students: int
