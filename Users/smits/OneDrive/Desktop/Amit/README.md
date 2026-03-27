# 📚 Premium Library Management System (NexLib)

A high-performance, responsive Library Management System built with **FastAPI** (Backend) and **Vanilla HTML/CSS/JS** (Frontend). Features specialized dashboards for **Admins** and **Students**, automated fine calculations, and secure JWT-based authentication.

---

## 🏛️ Architecture Overview
- **Backend:** Python FastAPI (Asynchronous), SQLAlchemy ORM (SQLite by default).
- **Frontend:** Vanilla CSS (Glassmorphism design), HTML5, and Modern JS (`fetch` API).
- **Auth:** JWT Token-based authentication with bcrypt password hashing.
- **Roles:**
  - **Admin:** Catalog management (CRUD), View all issued books, Issue to any student, Return processing, Dashboard analytics.
  - **Student:** Account registration, Catalog browsing, One-click book issuing, Personal issue history, Fine tracking.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.8+** installed.

### 2. Installation
Navigate to the project root and install dependencies:
```bash
pip install -r backend/requirements.txt
```

### 3. Initialize & Seed Database
Reset and populate the database with sample data (Admin: `admin@library.com`, Student: `john@student.com`):
```bash
python seed_data.py
```

### 4. Run the Backend
Start the FastAPI server on port 8000:
```bash
uvicorn backend.main:app --reload --port 8000
```
> *API Documentation is available at http://127.0.0.1:8000/docs*

### 5. Run the Frontend
You can simply open `frontend/index.html` in any modern browser, or use a live server:
```bash
# Example using Python's built-in server
python -m http.server 3000 --directory frontend
```

---

## 🔐 Default Credentials
| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@library.com` | `admin123` |
| **Student** | `john@student.com` | `student123` |

---

## 🛠️ Key API Endpoints (Demonstrated via cURL)

### Login (Get Token)
```bash
curl -X POST "http://127.0.0.1:8000/login" -H "Content-Type: application/json" -d '{"email":"admin@library.com","password":"admin123"}'
```

### Add a Book (Admin Only)
```bash
curl -X POST "http://127.0.0.1:8000/books" -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" -d '{"title":"The Great Gatsby","author":"F. Scott Fitzgerald","quantity":5}'
```

---

## ✅ Testing Checklist
1. **Auth Flow:** Register a new student, logout, then login. Check that student dashboard displays "Welcome...".
2. **Catalog CRUD:** As Admin, add a new book title, edit its quantity, and verify it updates in the table.
3. **Issuing:** As a Student, click "Issue" on a book. Verify quantity decrements and record appears in "Your History".
4. **Returning & Fines:** (The seed data includes an overdue book!). Visit the **Return Book** page as Admin. Click "Return" for the overdue book and verify the ₹10/day fine is displayed.
5. **Security:** Logged in as a student, try to manually visit `admin_dashboard.html`. The system will automatically redirect to the student view.

---

*Built with ❤️ by Anti Gravity*
