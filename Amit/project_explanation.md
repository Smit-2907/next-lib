# NexLib: Project Codebase Explanation

This document provides a comprehensive overview of the NexLib project structure, architecture, and core components.

## 1. Project Overview
NexLib is a premium, high-performance Library Management System designed with a **FastAPI** backend and a **Vanilla UI** (HTML/CSS/JS) frontend featuring a glassmorphism design. 

The project is divided into two main parts:
- **`/backend`**: Contains the FastAPI server, database configuration, and business logic.
- **`/frontend`**: Contains the raw HTML, CSS, and JS files served statically.

## 2. Directory Structure
```
Amit/
├── README.md               # Main project documentation
├── seed_data.py            # Script used to initialize the database with data
├── library.db              # Database file (also found inside backend/ for consistency)
├── backend/                # FastAPI Backend Workspace
│   ├── main.py             # Entry point for the FastAPI application
│   ├── models.py           # SQLAlchemy declarative database models
│   ├── schemas.py          # Pydantic schemas for data validation
│   ├── database.py         # Async DB configuration
│   ├── auth.py             # JWT authentication mechanisms
│   ├── requirements.txt    # Python dependencies
│   └── library.db          # Active SQLite Database
└── frontend/               # Vanilla JS Frontend Workspace
    ├── app.js              # Main JavaScript logic (auth, requests, layout injection)
    ├── style.css           # Glassmorphism aesthetic CSS rules
    ├── index.html          # Landing page
    ├── login.html          # Authentication gate
    ├── register.html       # Signup page
    ├── admin_dashboard.html# Dashboard for system admins
    ├── student_dashboard.html# Portal for students
    ├── books.html          # Catalog view
    └── return.html / issue.html # Operation views
```

## 3. Backend Architecture (FastAPI + Async SQLAlchemy)

### Database Setup (`database.py`)
Utilizes `aiosqlite` and Async SQLAlchemy for high-concurrency database interactions.

### Data Models (`models.py`)
Defines the relational schema:
- **`User`**: Has `id`, `name`, `email`, `password_hash`, `role` (admin/student).
- **`Book`**: Has `id`, `title`, `author`, `isbn`, `quantity`, `category`, and `cover_url`.
- **`IssuedBook`**: Junction table tying Users and Books with `issue_date`, `due_date`, `return_date`, `status`, and dynamic `fine` calculations.

### Schemas (`schemas.py`)
Utilizes Pydantic to establish robust Request/Response paradigms. Contains base models, create models, and response models (e.g., `BookCreate`, `BookSchema`, `IssueRequest`, etc.). 

### Main App (`main.py`)
Houses the application routes:
- **Auth Routes**: `/login`, `/register`.
- **Book Routes**: CRUD operations (`/books`, `/books/available`).
- **Transaction Routes**: Issue and Return operations (`/issue`, `/return`).
- **Reporting Routes**: Analytics aggregates for Admins (`/reports/summary`, `/reports/categories`).

## 4. Frontend Architecture (Vanilla JS)

### State & Auth Management (`app.js`)
Uses `sessionStorage` to store JWT tokens and roles. Provides shared utility functions like `checkAuth()`, `fetchApi()`, and `logout()`.

### Layout Injection
Instead of redundant HTML, `app.js` renders common components like Sidebars dynamically via `injectLayout()` based on the logged-in user's role.

### Dashboard Rendering
- Admin dashboard fetches real-time statistics and renders them into grid cards and tables.
- Student dashboard tracks "Currently Reading" and "Overdue Items" dynamically calculating deadlines natively in the browser.

## 5. Security Protocol
- No raw passwords saved. Everything is hashed by Bcrypt backend.
- Role-based routing enforces boundaries between System Administrators and regular Students.
- Token-based API validation for backend resource interactions.

## 6. How to Run
1. Serve the Backend on Port `8000` via Uvicorn (`cd backend && uvicorn main:app --reload --port 8000`).
2. Serve the Frontend independently e.g. Port `3001` via python HTTP server (`python -m http.server 3001 --directory frontend`).
