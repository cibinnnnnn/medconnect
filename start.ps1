# Quick Start Script
# Run this after setup to start the server

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   Starting MedConnect Server" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Run server
Write-Host ""
Write-Host "Starting development server..." -ForegroundColor Yellow
Write-Host "Server will be available at: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
