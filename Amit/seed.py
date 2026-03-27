import urllib.request
import json

books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "quantity": 5},
    {"title": "1984", "author": "George Orwell", "quantity": 10},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "quantity": 7},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 4},
    {"title": "Atomic Habits", "author": "James Clear", "quantity": 12},
    {"title": "Digital Minimalism", "author": "Cal Newport", "quantity": 8},
    {"title": "Pride and Prejudice", "author": "Jane Austen", "quantity": 3}
]

for book in books:
    try:
        data = json.dumps(book).encode("utf-8")
        req = urllib.request.Request("http://localhost:8012/books", data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as f:
            print(f"Added: {book['title']}")
    except Exception as e:
        print(f"Error adding {book['title']}: {e}")
