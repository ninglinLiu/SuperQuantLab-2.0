@echo off
REM Start backend server for Windows

echo Starting SuperQuantLab 2.0 Backend...
echo Make sure you have installed dependencies: poetry install or uv sync
echo.

REM Try poetry first
where poetry >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using Poetry...
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    goto :end
)

REM Try uv
where uv >nul 2>nul
if %ERRORLEVEL% == 0 (
    echo Using uv...
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    goto :end
)

echo Error: Neither poetry nor uv found. Please install dependencies first.
exit /b 1

:end

