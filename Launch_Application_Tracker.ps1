$project = "$env:USERPROFILE\Documents\Projects\Application_Tracker"
$python  = "$project\.venv\Scripts\python.exe"
$app     = "$project\web_job_tracker.py"
$url     = "http://127.0.0.1:5000"

# Start the Flask/Python app in its own PowerShell window
Start-Process powershell.exe -WindowStyle Minimized -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "cd `"$project`"; & `"$python`" `"$app`""
)

# Wait a few seconds for the server to start
Start-Sleep -Seconds 3

# Open in Chrome.
# If Chrome is already open, this opens a new tab.
# If Chrome is closed, this opens a new Chrome window.
$chrome1 = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$chrome2 = "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"

if (Test-Path $chrome1) {
    Start-Process $chrome1 $url
}
elseif (Test-Path $chrome2) {
    Start-Process $chrome2 $url
}
else {
    Start-Process $url
}
