import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import engine, Base
from backend.models import User, Book, IssuedBook
from backend.auth import get_password_hash
from datetime import date, timedelta

async def seed():
    print("Seeding database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create Users
        admin = User(
            name="Library Admin",
            email="admin@library.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        student1 = User(
            name="John Student",
            email="john@student.com",
            password_hash=get_password_hash("student123"),
            role="student"
        )
        student2 = User(
            name="Jane Doe",
            email="jane@student.com",
            password_hash=get_password_hash("student123"),
            role="student"
        )
        session.add_all([admin, student1, student2])
        await session.commit()

        # Create Books
        books = [
            Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="978-0743273565", quantity=5, category="Classic", cover_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=400"),
            Book(title="Clean Code", author="Robert C. Martin", isbn="978-0132350884", quantity=3, category="Technology", cover_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=400"),
            Book(title="Thinking, Fast and Slow", author="Daniel Kahneman", isbn="978-0374275631", quantity=2, category="Psychology", cover_url="https://images.unsplash.com/photo-1589998059171-3c2242500bf0?q=80&w=400"),
            Book(title="The Alchemist", author="Paulo Coelho", isbn="978-0062315007", quantity=10, category="Fiction", cover_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400")
        ]
        session.add_all(books)
        await session.commit()

        # Create some sample issued record
        issue1 = IssuedBook(
            book_id=1, 
            user_id=2, 
            issue_date=date.today() - timedelta(days=10), 
            due_date=date.today() - timedelta(days=3), 
            status="issued"
        )
        session.add(issue1)
        await session.commit()
        
        # Decrement book qty for issued book
        booked_book = await session.get(Book, 1)
        booked_book.quantity -= 1
        await session.commit()

    print("Success! Database seeded with 1 Admin, 2 Students, 4 Books, and 1 Overdue Issue.")
    print("Credentials:")
    print("Admin: admin@library.com / admin123")
    print("Student: john@student.com / student123")

if __name__ == "__main__":
    asyncio.run(seed())
