@echo off
REM --- Start TUJ-Eats Backend locally (no typing needed) ---
REM Place this file in the project root folder (same level as the "app" directory).

setlocal
cd /d "%~dp0"

IF NOT EXIST ".venv\Scripts\activate.bat" (
  echo Virtual env not found: .venv\Scripts\activate.bat
  echo Please create it once with: py -m venv .venv
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
python -m pip show uvicorn >NUL 2>&1
IF ERRORLEVEL 1 (
  echo Installing uvicorn and fastapi the first time...
  python -m pip install "uvicorn[standard]" fastapi pydantic
)

echo.
echo Starting server at http://127.0.0.1:8000 ...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
echo.
echo Server stopped. Press any key to close.
pause >nul