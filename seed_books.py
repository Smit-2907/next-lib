import requests

books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "quantity": 5},
    {"title": "1984", "author": "George Orwell", "quantity": 10},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien", "quantity": 7},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "quantity": 4},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger", "quantity": 6},
    {"title": "Atomic Habits", "author": "James Clear", "quantity": 12},
    {"title": "Digital Minimalism", "author": "Cal Newport", "quantity": 8}
]

url = "http://localhost:8012/books"

for book in books:
    try:
        response = requests.post(url, json=book)
        if response.ok:
            print(f"Added: {book['title']}")
        else:
            print(f"Failed to add {book['title']}: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
