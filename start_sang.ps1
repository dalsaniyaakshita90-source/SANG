$ProjectRoot = "C:\Users\LENOVO\Documents\SANG"

Write-Host ""
Write-Host "========================================"
Write-Host "        SANG DEVELOPMENT STARTUP"
Write-Host "========================================"
Write-Host ""

Set-Location $ProjectRoot

$backendRunning = Get-NetTCPConnection -State Listen -LocalPort 8000 -ErrorAction SilentlyContinue
$demoRunning = Get-NetTCPConnection -State Listen -LocalPort 5500 -ErrorAction SilentlyContinue

if ($backendRunning) {
    Write-Host "[1/2] SANG backend already running on port 8000."
}
else {
    Write-Host "[1/2] Starting SANG backend on port 8000..."

    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "Set-Location '$ProjectRoot'; .\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

    Start-Sleep -Seconds 2
}

if ($demoRunning) {
    Write-Host "[2/2] SANG demo already running on port 5500."
}
else {
    Write-Host "[2/2] Starting SANG demo on port 5500..."

    Start-Process powershell -ArgumentList `
        "-NoExit", `
        "-Command", `
        "Set-Location '$ProjectRoot'; .\.venv\Scripts\python.exe -m http.server 5500 --directory demo"

    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "========================================"
Write-Host "        SANG IS READY"
Write-Host "========================================"
Write-Host ""
Write-Host "Backend: http://127.0.0.1:8000"
Write-Host "Demo:    http://127.0.0.1:5500"
Write-Host ""
Write-Host "Open the demo in Chrome:"
Write-Host "http://127.0.0.1:5500"
Write-Host ""