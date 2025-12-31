"""
Jarvis Background Service
Runs Jarvis in the background and waits for the wake word "jarvis"
"""
import os
import sys
import subprocess
import threading
import time
import pvporcupine
import pyaudio
import tkinter as tk
from tkinter import font as tk_font

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))
main_py_path = os.path.join(script_dir, 'templates', 'main.py')
python_exe = sys.executable

# Global variables
jarvis_process = None
porcupine = None
pa = None
gui_window = None
status_label = None

def create_notification_window():
    """Create a floating notification window"""
    global gui_window, status_label
    
    try:
        gui_window = tk.Tk()
        gui_window.title("Jarvis")
        gui_window.geometry("500x180")
        gui_window.configure(bg='#2a2a2a')
        
        # Make window always on top
        gui_window.attributes('-topmost', True)
        
        # Move to top-right corner of screen
        try:
            screen_width = gui_window.winfo_screenwidth()
            screen_height = gui_window.winfo_screenheight()
            x_pos = max(0, screen_width - 520)
            y_pos = 20
            gui_window.geometry(f"+{x_pos}+{y_pos}")
        except Exception as e:
            print(f"Warning: Could not position window: {e}")
        
        # Create main frame with border
        main_frame = tk.Frame(gui_window, bg='#2a2a2a', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_font = tk_font.Font(family="Segoe UI", size=20, weight="bold")
        title_label = tk.Label(
            main_frame,
            text="🎤 Jarvis",
            font=title_font,
            fg='#667eea',
            bg='#2a2a2a'
        )
        title_label.pack(pady=(0, 15))
        
        # Status label
        status_font = tk_font.Font(family="Segoe UI", size=14)
        status_label = tk.Label(
            main_frame,
            text="Say 'Jarvis' to activate your bot",
            font=status_font,
            fg='#ffffff',
            bg='#2a2a2a',
            wraplength=450
        )
        status_label.pack(pady=10)
        
        # Footer
        footer_font = tk_font.Font(family="Segoe UI", size=10)
        footer_label = tk.Label(
            main_frame,
            text="Listening...",
            font=footer_font,
            fg='#888888',
            bg='#2a2a2a'
        )
        footer_label.pack(pady=(10, 0))
        
        print("Notification window created successfully")
        return gui_window
    except Exception as e:
        print(f"ERROR: Failed to create notification window: {e}", file=sys.stderr)
        gui_window = None
        return None

def update_status(message, duration=2000):
    """Update status message in GUI"""
    global status_label
    if status_label:
        original_text = "Say 'Jarvis' to activate your bot"
        status_label.config(text=message, fg='#4ade80')
        gui_window.after(duration, lambda: status_label.config(text=original_text, fg='#ffffff'))

def initialize_wake_word_detector():
    """Initialize Porcupine wake word detector"""
    global porcupine
    try:
        # Initialize Porcupine for wake word detection
        porcupine = pvporcupine.create(
            keywords=['jarvis'],  # Wake word is "jarvis"
            access_key='e7StJWo1e6HSiXW8mzN4dTVE2KWkBSpfrtsVvLN617BYwafQL6SilA=='
        )
        return True
    except Exception as e:
        print(f"Error initializing wake word detector: {e}")
        print("Make sure you have a Porcupine access key from https://console.picovoice.ai/")
        return False

def start_jarvis():
    """Start the main Jarvis process"""
    global jarvis_process
    try:
        # Use pythonw.exe to run without console window
        python_exe_no_window = python_exe.replace('python.exe', 'pythonw.exe')
        if not os.path.exists(python_exe_no_window):
            python_exe_no_window = python_exe
        
        jarvis_process = subprocess.Popen(
            [python_exe_no_window, main_py_path],
            cwd=script_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Jarvis started with PID: {jarvis_process.pid}")
        return True
    except Exception as e:
        print(f"Error starting Jarvis: {e}")
        return False

def stop_jarvis():
    """Stop the Jarvis process"""
    global jarvis_process
    if jarvis_process and jarvis_process.poll() is None:
        try:
            jarvis_process.terminate()
            time.sleep(2)
            if jarvis_process.poll() is None:
                jarvis_process.kill()
            print("Jarvis stopped")
        except Exception as e:
            print(f"Error stopping Jarvis: {e}")
        jarvis_process = None

def listen_for_wake_word():
    """Listen for the wake word "jarvis" continuously"""
    global porcupine, pa
    
    if not initialize_wake_word_detector():
        return
    
    try:
        pa = pyaudio.PyAudio()
        stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        print("Listening for 'jarvis' wake word...")
        jarvis_active = False
        
        while True:
            try:
                pcm = stream.read(porcupine.frame_length)
                pcm = tuple(int.from_bytes(pcm[i:i+2], byteorder='little', signed=True) 
                           for i in range(0, len(pcm), 2))
                
                keyword_index = porcupine.process(pcm)
                
                if keyword_index >= 0:
                    print("Wake word 'jarvis' detected!")
                    update_status("✓ Wake word detected! Initializing...", 3000)
                    
                    if not jarvis_active:
                        start_jarvis()
                        jarvis_active = True
                    else:
                        print("Jarvis is already running")
                    
                    # Wait before listening again to avoid multiple triggers
                    time.sleep(2)
                
            except Exception as e:
                print(f"Error in listening loop: {e}")
                time.sleep(1)
                
    except Exception as e:
        print(f"Fatal error in wake word listener: {e}")
    finally:
        if stream:
            stream.stop_stream()
            stream.close()
        if pa:
            pa.terminate()
        if porcupine:
            porcupine.delete()

def main():
    """Main entry point"""
    global gui_window
    
    print("Jarvis Background Service Started")
    print("=" * 50)
    
    # Create GUI window
    try:
        create_notification_window()
        if not gui_window:
            print("WARNING: GUI window failed to create; continuing without it")
    except Exception as e:
        print(f"ERROR creating GUI: {e}")
    
    # Start wake word listening in a separate thread
    listen_thread = threading.Thread(target=listen_for_wake_word, daemon=True)
    listen_thread.start()
    
    try:
        # Keep GUI running (if it exists) or keep the service alive
        if gui_window:
            gui_window.mainloop()
        else:
            # If no GUI, keep listening in main thread
            listen_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down Jarvis Background Service...")
        stop_jarvis()
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        stop_jarvis()
        sys.exit(1)

if __name__ == "__main__":
    main()
