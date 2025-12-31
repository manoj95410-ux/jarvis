# Create a Scheduled Task for Jarvis at Login (more reliable than Startup shortcuts)
# Run this script from the project folder with Administrator privileges

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetBatch = Join-Path $scriptDir "launch_jarvis_silent.bat"

if (-not (Test-Path $targetBatch)){
    Write-Host "ERROR: launch_jarvis_silent.bat not found in project folder"
    exit 1
}

# Define task details
$taskName = "Jarvis Background Service"
$taskDesc = "Runs Jarvis AI assistant at user login"

# Check if task already exists and remove it
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing){
    Write-Host "Removing existing task..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create trigger (at login)
$trigger = New-ScheduledTaskTrigger -AtLogOn -RandomDelay (New-TimeSpan -Seconds 5)

# Create action (run batch file)
$action = New-ScheduledTaskAction -Execute $targetBatch -WorkingDirectory $scriptDir

# Create settings (allow task to run even if user is not logged in, restart if it fails)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 2)

# Register the task (run with highest privilege)
try{
    Register-ScheduledTask -TaskName $taskName `
                          -Trigger $trigger `
                          -Action $action `
                          -Settings $settings `
                          -Description $taskDesc `
                          -Force | Out-Null
    
    Write-Host "✓ Successfully created Scheduled Task: $taskName"
    Write-Host "  - Runs at login with 5-second delay"
    Write-Host "  - Batch file: $targetBatch"
    Write-Host ""
    Write-Host "To manage the task:"
    Write-Host "  - Press Win+R, type 'taskschd.msc', press Enter"
    Write-Host "  - Find '$taskName' in Task Scheduler Library"
    Write-Host ""
}catch{
    Write-Host "ERROR: Failed to create task: $_"
    exit 1
}