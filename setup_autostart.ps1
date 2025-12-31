# Create Windows Startup Task for Jarvis
# Run this script with Administrator privileges

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$batchFilePath = Join-Path $scriptDir "launch_jarvis_silent.bat"

# Verify batch file exists
if (-not (Test-Path $batchFilePath)) {
    Write-Host "Error: launch_jarvis_silent.bat not found at $batchFilePath"
    exit 1
}

# Create a scheduled task to run at user login
$taskName = "Jarvis Background Service"
$taskDescription = "Runs Jarvis AI assistant in the background at user login"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Scheduled task '$taskName' already exists. Updating..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create task trigger (at user login)
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Create task action (run the batch file)
$action = New-ScheduledTaskAction -Execute $batchFilePath

# Create task principal (run with current user)
$principal = New-ScheduledTaskPrincipal -RunLevel Highest

# Create and register the task
try {
    Register-ScheduledTask -TaskName $taskName `
                          -Trigger $trigger `
                          -Action $action `
                          -Principal $principal `
                          -Description $taskDescription `
                          -Force | Out-Null
    
    Write-Host "Successfully created scheduled task '$taskName'"
    Write-Host "Jarvis will now start automatically when you log in"
    Write-Host ""
    Write-Host "Task Details:"
    Write-Host "  Task Name: $taskName"
    Write-Host "  Description: $taskDescription"
    Write-Host "  Trigger: At user login"
    Write-Host "  Run Level: Highest (Administrator)"
    Write-Host ""
    Write-Host "To manage this task:"
    Write-Host "  - Open Task Scheduler (press Win+R, type 'taskschd.msc', press Enter)"
    Write-Host "  - Navigate to 'Task Scheduler Library'"
    Write-Host "  - Find '$taskName' in the task list"
    
} catch {
    Write-Host "Error creating scheduled task: $_"
    exit 1
}
