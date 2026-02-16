# MedConnect Setup Script for Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   MedConnect Setup Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
$projectPath = "c:\Users\aisha\OneDrive\Desktop\WISTORA\MedConnect"
Set-Location $projectPath
Write-Host "✓ Navigated to project directory" -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create necessary directories
Write-Host "Creating media directories..." -ForegroundColor Yellow
$directories = @(
    "media",
    "media\profiles",
    "media\qr_codes",
    "media\medical_records"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created $dir" -ForegroundColor Green
    }
}

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "✓ Database migrations completed" -ForegroundColor Green

# Collect static files
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput
Write-Host "✓ Static files collected" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create a superuser (admin):" -ForegroundColor White
Write-Host "   python manage.py createsuperuser" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Run the development server:" -ForegroundColor White
Write-Host "   python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Open your browser and visit:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Admin panel:" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host ""

# Prompt to create superuser
$createSuperuser = Read-Host "Would you like to create a superuser now? (Y/N)"
if ($createSuperuser -eq "Y" -or $createSuperuser -eq "y") {
    python manage.py createsuperuser
}

Write-Host ""
Write-Host "Thank you for using MedConnect! 🏥" -ForegroundColor Green
