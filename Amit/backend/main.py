import uvicorn
import os
import sys

# Auto-add current folder to path to support direct script execution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date, timedelta

# Standard imports
from database import engine, Base, get_db
from models import User, Book, IssuedBook
from schemas import (
    UserCreate, UserLogin, User as UserSchema, Token, 
    BookCreate, BookUpdate, Book as BookSchema, 
    IssueRequest, ReturnRequest, IssuedBook as IssuedBookSchema, 
    LibrarySummary
)
from auth import (
    get_password_hash, verify_password, create_access_token, 
    get_current_user, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="Pro Library Management System")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on Startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Optional: Seed default admin if none exists
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).filter(User.email == "admin@library.com"))
        if not result.scalars().first():
            admin_user = User(
                name="Admin",
                email="admin@library.com",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            session.add(admin_user)
            await session.commit()

# AUTH ENDPOINTS
@app.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user_in.email))
    user = result.scalars().first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# BOOK ENDPOINTS
@app.get("/books", response_model=List[BookSchema])
async def list_books(search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Book)
    if search:
        query = query.filter(Book.title.contains(search) | Book.author.contains(search))
    result = await db.execute(query)
    return result.scalars().all()

@app.post("/books", response_model=BookSchema, dependencies=[Depends(get_current_admin)])
async def add_book(book_in: BookCreate, db: AsyncSession = Depends(get_db)):
    new_book = Book(**book_in.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@app.get("/books/available", response_model=List[BookSchema])
async def list_available_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.quantity > 0))
    return result.scalars().all()

@app.put("/books/{book_id}", response_model=BookSchema, dependencies=[Depends(get_current_admin)])
async def update_book(book_id: int, book_in: BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in book_in.dict(exclude_unset=True).items():
        setattr(book, key, value)
    
    await db.commit()
    await db.refresh(book)
    return book

@app.delete("/books/{book_id}", dependencies=[Depends(get_current_admin)])
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()
    return {"message": "Book deleted successfully"}

# ISSUE/RETURN ENDPOINTS
@app.post("/issue", status_code=status.HTTP_201_CREATED)
async def issue_book(req: IssueRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = req.user_id if current_user.role == "admin" and req.user_id else current_user.id
    
    # Check book availability
    result = await db.execute(select(Book).filter(Book.id == req.book_id))
    book = result.scalars().first()
    if not book or book.quantity <= 0:
        raise HTTPException(status_code=400, detail="Book not available or not found")
    
    # Check if student already has this book issued
    check_issued = await db.execute(
        select(IssuedBook).filter(IssuedBook.book_id == req.book_id, IssuedBook.user_id == user_id, IssuedBook.status == "issued")
    )
    if check_issued.scalars().first():
        raise HTTPException(status_code=400, detail="Book already issued to this user")

    issue_date = date.today()
    due_date = issue_date + timedelta(days=7)
    
    new_issue = IssuedBook(
        book_id=req.book_id,
        user_id=user_id,
        issue_date=issue_date,
        due_date=due_date,
        status="issued"
    )
    
    book.quantity -= 1
    db.add(new_issue)
    await db.commit()
    return {"message": "Book issued successfully", "due_date": due_date.isoformat()}

@app.post("/return")
async def return_book(req: ReturnRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(IssuedBook).options(selectinload(IssuedBook.book)).filter(IssuedBook.id == req.issue_id, IssuedBook.status == "issued")
    )
    issue = result.scalars().first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue record not found or already returned")
    
    return_date = date.today()
    days_past = (return_date - issue.due_date).days
    fine = max(0, days_past * 10) # ₹10 per day
    
    issue.return_date = return_date
    issue.status = "returned"
    issue.fine = fine
    issue.book.quantity += 1
    
    await db.commit()
    return {"message": "Book returned successfully", "fine": fine}

@app.get("/issued", response_model=List[IssuedBookSchema], dependencies=[Depends(get_current_admin)])
async def get_all_issued(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(IssuedBook).options(selectinload(IssuedBook.book), selectinload(IssuedBook.user)))
    records = result.scalars().all()
    # Manual conversion to inject book title and student name
    out = []
    for r in records:
        schema = IssuedBookSchema.from_orm(r)
        schema.book_title = r.book.title
        schema.student_name = r.user.name
        out.append(schema)
    return out

@app.get("/my-issues", response_model=List[IssuedBookSchema])
async def get_my_issues(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(IssuedBook).options(selectinload(IssuedBook.book)).filter(IssuedBook.user_id == current_user.id)
    )
    records = result.scalars().all()
    out = []
    for r in records:
        schema = IssuedBookSchema.from_orm(r)
        schema.book_title = r.book.title
        out.append(schema)
    return out

# REPORTS
@app.get("/reports/summary", response_model=LibrarySummary, dependencies=[Depends(get_current_admin)])
async def get_summary(db: AsyncSession = Depends(get_db)):
    total_books = await db.scalar(select(func.sum(Book.quantity))) or 0
    total_titles = await db.scalar(select(func.count(Book.id))) or 0
    issued_count = await db.scalar(select(func.count(IssuedBook.id)).filter(IssuedBook.status == "issued")) or 0
    student_count = await db.scalar(select(func.count(User.id)).filter(User.role == "student")) or 0
    
    return {
        "total_books": total_titles,
        "available_books": (total_books),
        "issued_books": issued_count,
        "total_students": student_count
    }

@app.get("/reports/categories", dependencies=[Depends(get_current_admin)])
async def get_category_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book.category, func.count(Book.id)).group_by(Book.category))
    stats = result.all()
    return [{"category": s[0] or "General", "count": s[1]} for s in stats]

@app.get("/users", response_model=List[UserSchema], dependencies=[Depends(get_current_admin)])

async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
