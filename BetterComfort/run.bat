@echo off
REM ==============================================================================
REM BetterComfort Development Server Launcher
REM ==============================================================================

cd /d "%~dp0"

IF EXIST "..\.venv\Scripts\python.exe" (
    SET "PY_EXE=..\.venv\Scripts\python.exe"
) ELSE IF EXIST ".venv\Scripts\python.exe" (
    SET "PY_EXE=.venv\Scripts\python.exe"
) ELSE (
    SET "PY_EXE=python"
)

echo Starting BetterComfort Development Server...
"%PY_EXE%" manage.py runserver %*
