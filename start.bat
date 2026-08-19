@echo off
setlocal

set HTTP_PROXY=http://127.0.0.1:7890
set HTTPS_PROXY=http://127.0.0.1:7890

:: Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 'uv' is not installed or not in PATH. Please install uv from https://github.com/astral-sh/uv
    exit /b 1
)

:: Create venv if it doesn't exist
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment...
    uv venv .venv --python 3.11
)

:: Install/update dependencies
echo [INFO] Installing dependencies...
uv pip install --quiet -e .

:: Check if config.json exists
if not exist "config.json" (
    if exist "config.example.json" (
        echo [INFO] config.json not found, copying from config.example.json...
        copy config.example.json config.json
        echo [WARN] Please edit config.json to add your telegram bot token before running again.
        exit /b 1
    )
)

:: Run the daemon
echo [INFO] Starting the antigravity-telegram-bridge daemon...
.venv\Scripts\python.exe -m src.daemon

endlocal
