# 📚 NexLib: The Elite Library Management System

NexLib is a premium, high-performance Library Management System designed with **FastAPI** for an asynchronous backend and a **Glassmorphism-inspired** Vanilla Frontend.

---

## ✨ Advanced Features (Core Engrained)

- **🔄 Pending/Approval Workflow**: Students can request book loans, which appear as **Pending Requests** in the Admin Dashboard for official authorization.
- **🛡️ Persistent Persistence**: Database seeding is now optional. Your registered users, issued books, and custom records are preserved across app restarts.
- **💎 Elite Collection**: Pre-seeded with 12+ premium titles across Technology, Business, Sci-Fi, and Design.
- **📊 Command Center Analytics**: Real-time **Genre Distribution Charts** and Loan Traffic monitoring for Administrators.
- **⚡ Modern Auth**: Secure JWT-based entry with role-based navigation and automatic profile synchronization.
- **🎨 Glassmorphism UI**: A stunning, responsive interface built with Vanilla CSS and modern micro-animations.

---

## 🏛️ Architecture

- **Backend:** FastAPI (Python 3.13+), SQLAlchemy (Async), SQLite.
- **Frontend:** Vanilla HTML5 / CSS3 / ES6 Javascript.
- **Database:** `library.db` (Located in `/backend` for persistence).

---

## 🚀 Quick Start

### 1. Installation
Install the necessary high-performance dependencies:
```bash
pip install fastapi uvicorn sqlalchemy bcrypt "python-jose[cryptography]" python-multipart aiosqlite "pydantic[email]"
```

### 2. Synchronization & Initial Seeding (Run ONCE)
Initialize the database and setup default admin/student profiles. **Warning**: Running this will reset all existing data to defaults.
```bash
python seed_data.py
```

### 3. Launching the System
Run the main startup script from the root directory:
```powershell
.\run.bat
```
This will automatically launch the **Backend (8000)**, the **Frontend (3001)**, and open the library in your default browser.

---

## 🔐 Default Credentials

| Role | Email | Password |
|------|-------|----------|
| **Systems Architect** | `admin@library.com` | `admin123` |
| **John Watson (Student)** | `john@student.com` | `student123` |

---

## ✅ Feature Guide

1. **Student Protocol**: 
   - Login as a student and use the **Explore** tab to find a book.
   - Click **Issue Asset**. Your request will enter a **PENDING** state.
2. **Admin Protocol**:
   - Login as an admin and check the **Live Activity Feed**.
   - Review pending requests and click ✅ **Approve** or ❌ **Reject**.
3. **Synchronization**: Once approved, the book will appear in the student's **My Hub** as **ISSUED**.

*Engineered with precision by AntiGravity & Mark II*
