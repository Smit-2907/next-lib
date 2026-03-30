@echo off
echo ==================================================
echo         Starting NexLib Library System...
echo ==================================================
echo.

echo [1/5] Checking uv installation...
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 'uv' is not installed or not in PATH.
    echo         Install it from: https://docs.astral.sh/uv/getting-started/installation/
    echo         Or run: pip install uv
    pause
    exit /b 1
)
echo [OK] uv found.
echo.

echo [2/5] Syncing backend dependencies with uv...
cd /d "%~dp0backend"
uv sync
if %errorlevel% neq 0 (
    echo [ERROR] uv sync failed. Check the output above for details.
    pause
    exit /b 1
)
echo [OK] Dependencies ready.
echo.

echo [3/5] Starting backend server (FastAPI via uv run)...
start "NexLib Backend" cmd /k "cd /d "%~dp0backend" && uv run uvicorn main:app --reload --port 8000"
echo.

echo [4/5] Starting frontend server...
start "NexLib Frontend" cmd /k "uv run python -m http.server 3001 --directory "%~dp0frontend""
echo.

echo [5/5] Waiting for servers to initialize...
timeout /t 3 /nobreak > NUL
echo.

echo Opening NexLib in your default browser...
start http://localhost:3001

echo.
echo ==================================================
echo  NexLib is running!
echo  Backend API  : http://127.0.0.1:8000/docs
echo  Frontend UI  : http://localhost:3001
echo  Admin Login  : admin@library.com / admin123
echo  Leave these terminal windows open to keep
echo  the servers running. To stop, close them.
echo ==================================================
pause
