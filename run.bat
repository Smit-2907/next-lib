@echo off
echo ==================================================
echo         Starting NexLib Library System...
echo ==================================================
echo.

echo [1/4] Skip seeding (database is persistent)...
:: python seed_data.py
echo.

echo [2/4] Starting backend server (FastAPI)...
start "NexLib Backend" cmd /k "cd backend && uvicorn main:app --reload --port 8000"
echo.

echo [3/4] Starting frontend server...
start "NexLib Frontend" cmd /k "python -m http.server 3001 --directory frontend"
echo.

echo [4/4] Waiting for servers to initialize...
timeout /t 3 /nobreak > NUL
echo.

echo Opening NexLib in your default browser...
start http://localhost:3001

echo.
echo ==================================================
echo  NexLib is running!
echo  Backend API: http://127.0.0.1:8000/docs
echo  Frontend UI: http://localhost:3001
echo  Leave these terminal windows open to keep
echo  the servers running. To stop, close the
echo  command prompt windows.
echo ==================================================
pause
