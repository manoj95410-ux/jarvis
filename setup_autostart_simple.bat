@echo off
REM Alternative Autostart Setup - Creates startup folder shortcut
REM This is a simpler alternative to scheduled tasks

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0
set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set BATCH_FILE=%SCRIPT_DIR%launch_jarvis_silent.bat
set SHORTCUT_PATH=%STARTUP_FOLDER%\Jarvis.lnk

echo Creating Jarvis autostart shortcut...

REM Create VBScript to create shortcut (more reliable than other methods)
set VBSCRIPT_PATH=%TEMP%\create_shortcut.vbs

(
    echo Set oWS = WScript.CreateObject("WScript.Shell"^)
    echo sLinkFile = "%SHORTCUT_PATH%"
    echo Set oLink = oWS.CreateShortcut(sLinkFile^)
    echo oLink.TargetPath = "%BATCH_FILE%"
    echo oLink.WorkingDirectory = "%SCRIPT_DIR%"
    echo oLink.WindowStyle = 7  REM 7 = Minimized
    echo oLink.Description = "Jarvis AI Assistant Background Service"
    echo oLink.Save
) > "%VBSCRIPT_PATH%"

REM Run the VBScript
cscript.exe //nologo "%VBSCRIPT_PATH%"

REM Clean up
del "%VBSCRIPT_PATH%"

echo.
echo Successfully created Jarvis autostart shortcut at:
echo %SHORTCUT_PATH%
echo.
echo Jarvis will start automatically when you log in.
echo.
pause
