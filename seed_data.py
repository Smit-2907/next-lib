import asyncio
import os
import sys

# Ensure backend directory is in path
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base
from models import User, Book, IssuedBook
from auth import get_password_hash
from datetime import date, timedelta

async def seed():
    print("🚀 Initiating Library Expansion...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        # 👤 USERS
        admin = User(name="Systems Architect", email="admin@library.com", password_hash=get_password_hash("admin123"), role="admin")
        student1 = User(name="John Watson", email="john@student.com", password_hash=get_password_hash("student123"), role="student")
        student2 = User(name="Sara Croft", email="sara@student.com", password_hash=get_password_hash("student123"), role="student")
        session.add_all([admin, student1, student2])
        await session.commit()

        # 📚 THE ELITE COLLECTION
        books = [
            # Technology
            Book(title="Modern Cloud Architecture", author="Sarah Drasner", isbn="978-0132350884", quantity=5, category="Technology", cover_url="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=400"),
            Book(title="Refactoring", author="Martin Fowler", isbn="978-0201485677", quantity=3, category="Technology", cover_url="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?q=80&w=400"),
            Book(title="Zero to One", author="Peter Thiel", isbn="978-0804139298", quantity=8, category="Business", cover_url="https://images.unsplash.com/photo-1507413245164-6160d8298b31?q=80&w=400"),
            
            # Classics & Fiction
            Book(title="Dune: Part One", author="Frank Herbert", isbn="978-0441172719", quantity=10, category="Sci-Fi", cover_url="https://images.unsplash.com/photo-1532012197367-2cf3473959df?q=80&w=400"),
            Book(title="The Midnight Library", author="Matt Haig", isbn="978-0525559474", quantity=12, category="Fiction", cover_url="https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=400"),
            Book(title="Atomic Habits", author="James Clear", isbn="978-0735211292", quantity=15, category="Self-Help", cover_url="https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=400"),
            
            # Design & Art
            Book(title="The Design of Everyday Things", author="Don Norman", isbn="978-0465050659", quantity=4, category="Design", cover_url="https://images.unsplash.com/photo-1586717791821-3f44a563eb4c?q=80&w=400"),
            Book(title="Logo Modernism", author="Taschen", isbn="978-3836545303", quantity=2, category="Design", cover_url="https://images.unsplash.com/photo-1626785774573-4b799315345d?q=80&w=400"),
            Book(title="Sapiens", author="Yuval Noah Harari", isbn="978-0062316097", quantity=6, category="History", cover_url="https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=400"),
            
            # Additional Mix
            Book(title="The Pragmatic Programmer", author="David Thomas", isbn="978-0135957059", quantity=5, category="Technology", cover_url="https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=400"),
            Book(title="Rich Dad Poor Dad", author="Robert Kiyosaki", isbn="978-1612680194", quantity=20, category="Finance", cover_url="https://images.unsplash.com/photo-1541963463532-d68292c34b19?q=80&w=400"),
            Book(title="Creativity, Inc.", author="Ed Catmull", isbn="978-0812993011", quantity=3, category="Business", cover_url="https://images.unsplash.com/photo-1517433367423-c7e5b0f35086?q=80&w=400")
        ]
        session.add_all(books)
        await session.commit()

        # 📅 ACTIVITY LOGS
        # John has an overdue book
        session.add(IssuedBook(book_id=1, user_id=2, issue_date=date.today()-timedelta(days=15), due_date=date.today()-timedelta(days=8), status="issued"))
        # Sara has a current book
        session.add(IssuedBook(book_id=4, user_id=3, issue_date=date.today()-timedelta(days=2), due_date=date.today()+timedelta(days=5), status="issued"))
        
        # Decrement quantities
        b1 = await session.get(Book, 1); b1.quantity -= 1
        b4 = await session.get(Book, 4); b4.quantity -= 1
        await session.commit()

    print("✨ Successfully expanded to 12 Elite Titles & 3 Strategic User Profiles.")

if __name__ == "__main__":
    asyncio.run(seed())
