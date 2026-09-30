$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot
$pythonPath = Join-Path $projectRoot 'venv\Scripts\python.exe'
$healthUrl = 'http://127.0.0.1:8000/api/health'
$dashboardUrl = 'http://127.0.0.1:8000/'
$health = $null

try {
    $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2
} catch {
    if (-not (Test-Path $pythonPath)) {
        throw "Project Python environment not found at $pythonPath."
    }

    $server = Start-Process -FilePath $pythonPath `
        -ArgumentList @('-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000') `
        -WorkingDirectory $projectRoot `
        -PassThru

    $deadline = [DateTime]::UtcNow.AddSeconds(30)
    while ([DateTime]::UtcNow -lt $deadline) {
        if ($server.HasExited) {
            throw 'Uvicorn exited before the app became ready. Check the terminal output and port 8000.'
        }

        try {
            $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2
            break
        } catch {
            [System.Threading.Thread]::Sleep(250)
        }
    }

    if (-not $health) {
        throw 'The app did not become ready within 30 seconds.'
    }
}

if ($health.status -ne 'API is running') {
    throw 'Port 8000 is responding, but it does not appear to be this app.'
}

Start-Process -FilePath 'chrome.exe' -ArgumentList $dashboardUrl
Write-Output "Dashboard opened in Chrome: $dashboardUrl"