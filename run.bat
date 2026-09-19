@echo off
REM ==============================================================================
REM BetterComfort Development Server Launcher (Root)
REM ==============================================================================

cd /d "%~dp0"

IF EXIST ".venv\Scripts\python.exe" (
    SET "PY_EXE=.venv\Scripts\python.exe"
) ELSE (
    SET "PY_EXE=python"
)

cd BetterComfort
echo Starting BetterComfort Development Server...
"..\%PY_EXE%" manage.py runserver %*
