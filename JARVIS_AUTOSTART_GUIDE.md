# Jarvis Background Service Setup Guide

## Overview
This guide will help you set up Jarvis to:
1. Run silently in the background
2. Respond to voice activation (say "jarvis")
3. Start automatically when you log in

---

## Prerequisites

You need to install the Porcupine wake word detection library:

```powershell
pip install pvporcupine
```

You also need a FREE Porcupine access key:
1. Go to https://console.picovoice.ai/
2. Sign up for a free account
3. Create an access key
4. Copy your access key

---

## Setup Steps

### Step 1: Get Your Porcupine Access Key

1. Visit https://console.picovoice.ai/
2. Create a free account
3. Go to "Access Keys" section
4. Copy your access key

### Step 2: Configure the Access Key

Edit the `jarvis_background.py` file and replace:
```python
access_key='YOUR_PORCUPINE_ACCESS_KEY'
```

With your actual access key:
```python
access_key='YOUR_ACTUAL_ACCESS_KEY_HERE'
```

### Step 3: Set Up Autostart (Choose ONE method)

#### METHOD 1: Using PowerShell Scheduled Task (Recommended)

1. Open PowerShell as Administrator
2. Navigate to the Jarvis directory:
   ```powershell
   cd "C:\Users\swade_t\OneDrive\Desktop\jarvis_web"
   ```
3. Run the setup script:
   ```powershell
   .\setup_autostart.ps1
   ```

#### METHOD 2: Using Simple Batch File

1. Double-click `setup_autostart_simple.bat`
2. This will create a shortcut in your Startup folder

### Step 4: Test the Setup

1. **Manual Start (for testing):**
   ```powershell
   .\launch_jarvis_silent.bat
   ```

2. **Voice Test:**
   - Say "jarvis" clearly into your microphone
   - You should hear a response from Jarvis
   - Watch for the Jarvis application to open

3. **Auto-Start Test:**
   - Log out and log back in
   - Jarvis should start automatically

---

## How It Works

### Main Components:

1. **jarvis_background.py**
   - Listens continuously for the "jarvis" wake word
   - When detected, starts the main Jarvis application
   - Runs silently in the background

2. **launch_jarvis_silent.bat**
   - Launches the background service silently
   - Uses pythonw.exe (no console window)

3. **setup_autostart.ps1 OR setup_autostart_simple.bat**
   - Registers Jarvis to start at user login
   - Ensures it runs automatically

---

## Troubleshooting

### Issue: "Access key error" when starting

**Solution:** Make sure you've replaced `YOUR_PORCUPINE_ACCESS_KEY` with your actual key from https://console.picovoice.ai/

### Issue: Microphone not working

**Solution:** 
- Check Windows Settings > Privacy > Microphone
- Ensure Python has microphone permission
- Test with: `python -c "import pyaudio; print('Microphone OK')"`

### Issue: Jarvis not starting at login

**Solution:**
- Verify the scheduled task exists:
  - Press `Win+R`, type `taskschd.msc`, press Enter
  - Look for "Jarvis Background Service" in the task list
- Check that the batch file path is correct

### Issue: Autostart task not working

**Solution:** Run setup_autostart.ps1 again as Administrator

### Issue: Wake word not detected

**Solution:**
- Speak "jarvis" clearly and distinctly
- Check your microphone volume
- Ensure your microphone is not muted
- Test with: `python -c "import pyaudio; import speech_recognition as sr"`

---

## Manual Management

### To Remove Autostart:

**PowerShell (as Administrator):**
```powershell
Unregister-ScheduledTask -TaskName "Jarvis Background Service" -Confirm:$false
```

**Or via GUI:**
1. Press `Win+R`, type `taskschd.msc`
2. Find "Jarvis Background Service"
3. Right-click and delete

### To Stop Jarvis Manually:

**PowerShell:**
```powershell
Get-Process | Where-Object {$_.Name -like "*python*"} | Stop-Process
```

**Or:**
1. Press `Ctrl+Shift+Esc` to open Task Manager
2. Find Python processes and end them

---

## Additional Notes

- The background service uses very minimal CPU when idle
- Porcupine wake word detection works offline (no internet required)
- The service will restart Jarvis if it crashes
- You can customize the wake word by changing `keywords=['jarvis']` to other words

---

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed: `pip list`
3. Make sure your access key is valid
4. Check Windows Event Viewer for any errors

---

Last Updated: 2025-12-31
