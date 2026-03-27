# 📚 NexLib: The Elite Library Management System

NexLib is a premium, high-performance Library Management System designed with **FastAPI** for an asynchronous backend and a **Glassmorphism-inspired** Vanilla Frontend.

---

## ✨ Advanced Features (New!)

- **💎 Elite Collection**: Pre-seeded with 12+ premium titles across Technology, Business, Sci-Fi, and Design.
- **📊 Command Center Analytics**: Real-time **Genre Distribution Charts** and Loan Traffic monitoring for Administrators.
- **🛡️ Robust Core**: Cross-directory execution support with absolute-path database synchronization.
- **⚡ Modern Auth**: Secure JWT-based entry with automatic post-registration login.
- **🎨 Glassmorphism UI**: A stunning, responsive interface built with Vanilla CSS and modern micro-animations.

---

## 🏛️ Architecture

- **Backend:** FastAPI (Python 3.13+), SQLAlchemy (Async), SQLite.
- **Frontend:** Vanilla HTML5 / CSS3 / ES6 Javascript.
- **Database:** `library.db` (Located in `/backend`).

---

## 🚀 Quick Start

### 1. Installation
Install the necessary high-performance dependencies:
```bash
pip install fastapi uvicorn sqlalchemy bcrypt "python-jose[cryptography]" python-multipart aiosqlite "pydantic[email]"
```

### 2. Synchronization & Seeding
Initialize the Elite Collection and setup default user profiles:
```bash
python seed_data.py
```

### 3. Launching the Core (Backend)
Start the library core on its dedicated port:
```bash
cd backend
uvicorn main:app --reload --port 8000
```
> *API Schema available at http://127.0.0.1:8000/docs*

### 4. Launching the Interface (Frontend)
Serve the stunning frontend layout:
```bash
python -m http.server 3001 --directory frontend
```
> *Access the dashboard at http://localhost:3001*

---

## 🔐 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| **Systems Architect** | `admin@library.com` | `admin123` |
| **John Watson (Student)** | `john@student.com` | `student123` |

---

## ✅ Live Checklist
1. **Analytics Monitor**: As Admin, check the "Genre Distribution" to see real-time collection stats.
2. **Issue Protocol**: As a Student, explore the "Digital Archive" and request an elite book.
3. **Fine Engine**: Return an overdue book (like John Watson's) and monitor automated fine calculations.

*Engineered with precision by AntiGravity & Mark II*
