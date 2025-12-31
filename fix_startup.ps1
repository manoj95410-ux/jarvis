# Fix Startup Shortcut for Jarvis
# Run this script from the project folder (double-click or run in PowerShell)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$startup = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup"
$shortcut = Join-Path $startup "Jarvis.lnk"
$targetBatch = Join-Path $scriptDir "launch_jarvis_silent.bat"
$log = Join-Path $scriptDir "startup_fix.log"
$backupFolder = Join-Path $scriptDir "startup_backups"

function Log($msg){
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Add-Content -Path $log -Value $line
}

Log "Starting startup fix script"
Log "Script dir: $scriptDir"
Log "Startup folder: $startup"
Log "Desired target: $targetBatch"

if (-not (Test-Path $targetBatch)){
    Log "ERROR: target launcher not found: $targetBatch"
    Write-Host "ERROR: launch_jarvis_silent.bat not found in project folder: $scriptDir"
    exit 1
}

# Backup existing shortcut if present
if (Test-Path $shortcut){
    $bak = "$shortcut.bak"
    Copy-Item -Path $shortcut -Destination $bak -Force
    Log "Backed up existing shortcut to $bak"
}

# Create shortcut via COM
try{
    $ws = New-Object -ComObject WScript.Shell
    $link = $ws.CreateShortcut($shortcut)
    $link.TargetPath = $targetBatch
    $link.WorkingDirectory = $scriptDir
    $link.WindowStyle = 7
    $link.Description = "Jarvis AI Assistant Background Service"
    $link.Save()
    Log "Created/updated shortcut: $shortcut -> $targetBatch"
}catch{
    Log "ERROR: failed to create shortcut: $_"
    Write-Host "ERROR: failed to create shortcut. See $log"
}

# Move stray files out of Startup folder (non-destructive)
$toMove = @('launch_jarvis.bat','main.exe.py','main.pyw.py')
if (-not (Test-Path $backupFolder)){
    New-Item -Path $backupFolder -ItemType Directory | Out-Null
}
foreach($f in $toMove){
    $p = Join-Path $startup $f
    if (Test-Path $p){
        $dest = Join-Path $backupFolder $f
        Move-Item -Path $p -Destination $dest -Force
        Log "Moved stray startup file $p -> $dest"
    }
}

# Start the launcher once to test (runs silently)
try{
    Start-Process -FilePath "$targetBatch" -WindowStyle Hidden
    Log "Started launcher for testing: $targetBatch"
}catch{
    Log "ERROR: failed to start launcher: $_"
}

Log "Startup fix script completed"
Write-Host "Done. Check startup_fix.log in the project folder for details."