#!/bin/bash

# FastAPI Task Management Project Setup Script

echo "Setting up FastAPI Task Management Project..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run tests to verify setup
echo "Running tests to verify installation..."
pytest tests/ -v

echo "Setup complete! 🎉"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Then visit http://localhost:8000/docs to see the API documentation"
