#!/bin/bash
# Start backend server

echo "Starting SuperQuantLab 2.0 Backend..."
echo "Make sure you have installed dependencies: poetry install or uv sync"
echo ""

# Check if poetry is available
if command -v poetry &> /dev/null; then
    echo "Using Poetry..."
    poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
elif command -v uv &> /dev/null; then
    echo "Using uv..."
    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "Error: Neither poetry nor uv found. Please install dependencies first."
    exit 1
fi

