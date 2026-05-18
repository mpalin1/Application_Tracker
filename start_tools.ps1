# Start from the folder where this script is located
Set-Location $PSScriptRoot

Write-Host "Starting Job Application Tracker web app..." -ForegroundColor Green

# Start Flask web app in a new PowerShell window
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$PSScriptRoot'; py .\web_job_tracker.py"
)

Write-Host "Waiting for Flask to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# Open web app in the default browser
Start-Process "http://127.0.0.1:5000"

Write-Host "Web app should be open at http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Starting autofill helper..." -ForegroundColor Cyan

# Run autofill helper in the current PowerShell window
py .\autofill_job_application.py