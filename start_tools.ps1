# Start from the folder where this script is located
Set-Location $PSScriptRoot

Write-Host "Starting Job Application Tracker web app..." -ForegroundColor Green

# Start Flask in the background instead of opening a new PowerShell window
$flaskJob = Start-Job -ScriptBlock {
    Set-Location $using:PSScriptRoot
    py .\web_job_tracker.py
}

Write-Host "Waiting for Flask to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 6

# Open the web app in a separate Chrome app-style window
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"

if (Test-Path $chromePath) {
    Write-Host "Opening Application Tracker in Chrome..." -ForegroundColor Green

    $browser = Start-Process $chromePath `
        -ArgumentList "--app=http://127.0.0.1:5000" `
        -PassThru

    Write-Host "Starting autofill helper..." -ForegroundColor Cyan
    Write-Host "Close the Application Tracker browser window when you are done." -ForegroundColor Yellow

    py .\autofill_job_application.py

    Write-Host "Waiting for Application Tracker browser window to close..." -ForegroundColor Yellow
    Wait-Process -Id $browser.Id -ErrorAction SilentlyContinue
}
else {
    Write-Host "Chrome was not found at the expected location." -ForegroundColor Red
    Write-Host "Opening in default browser instead. You will need to stop Flask manually." -ForegroundColor Yellow
    Start-Process "http://127.0.0.1:5000"

    py .\autofill_job_application.py
}

Write-Host "Stopping Flask web app..." -ForegroundColor Yellow

Stop-Job $flaskJob -ErrorAction SilentlyContinue
Remove-Job $flaskJob -ErrorAction SilentlyContinue

Write-Host "Done. Web app closed." -ForegroundColor Green