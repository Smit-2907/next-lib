# NexLib: Project Codebase Explanation

This document provides a comprehensive overview of the NexLib project structure, architecture, and core components as of the latest version.

## 1. Project Overview
NexLib is a premium Library Management System focused on performance and modern design (Glassmorphism). It utilizes a **FastAPI** backend for asynchronous operations and a **Vanilla JS** frontend.

The project is structured for persistence, ensuring user data and loan protocols are maintained across sessions.

## 2. Updated Directory Structure
```
next-lib/
├── README.md               # Quick start and high-level documentation
├── run.bat                 # Single-click master startup script
├── seed_data.py            # Diagnostic script for resetting/initializing the library
├── backend/                # FastAPI Core Workspace
│   ├── main.py             # App entry, API routing, and Approval logic
│   ├── models.py           # SQLAlchemy Relational Models (with 'Pending' status support)
│   ├── schemas.py          # Data validation layer using Pydantic
│   ├── database.py         # Persistent Async SQLite configuration
│   ├── auth.py             # JWT & Password Security mechanisms
│   └── library.db          # ACTIVE SQLite Database (The Source of Truth)
└── frontend/               # Vanilla Workspace (HTML/CSS/JS)
    ├── app.js              # Central Logic: Auth, Dashboard Sync, Approval handling
    ├── style.css           # Global Design System (Aesthetics)
    ├── admin_dashboard.html# Command Center for admins
    └── student_dashboard.html / books.html / issue.html / login.html
```

## 3. Core Logic & Persistence

### The Persistence Protocol
Unlike earlier versions, the current system is built for **Persistence**. 
- The `run.bat` script is now non-destructive; it launches the system without wiping your database. 
- The `library.db` file in the `/backend` folder stores all data permanently.

### Pending/Approval Workflow
A key architectural feature is the **Issue Protocol**:
1. **Request Phase**: When a Student requests a book, a record is created in `IssuedBook` with `status="pending"`.
2. **Approval Phase**: Admins monitor these requests and finalize them via the `approve_issue` endpoint, which then deducts stock from the `Book` record and updates the status to `issued`.

## 4. UI Design System
The frontend follows a strict **Glassmorphism** aesthetic defined in `style.css`. 
- **app.js**: Dynamically injects layouts (Sidebars, Badges) based on user roles.
- **Role Detection**: Any page can identify if the learner is an Admin or Student and show/hide capabilities (e.g., hidden Edit buttons for students).

## 5. Maintenance
To fully reset the library to factory settings (WARNING: deletes all custom users), run:
`python seed_data.py` from the root directory.

*Engineered with precision for Next-Gen Library Management.*
