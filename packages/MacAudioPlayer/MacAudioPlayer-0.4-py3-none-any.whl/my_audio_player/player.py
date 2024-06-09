import os
import subprocess

paused = False
process = None

def play(file_path):
    """
    Play an audio file located at the given file path.
    """
    global process
    global paused

    if os.path.exists(file_path):
        if process is not None:
            print("An audio file is already playing. Please pause or stop it before playing another.")
            return
        else:
            process = subprocess.Popen(["afplay", file_path])
            paused = False
    else:
        print("File not found.")

def pause():
    """
    Pause the currently playing audio.
    """
    global process
    global paused

    if process is not None and not paused:
        process.terminate()
        paused = True

def unpause():
    """
    Unpause the currently paused audio.
    """
    global process
    global paused

    if process is None:
        print("No audio is currently playing.")
    elif paused:
        process = subprocess.Popen(["afplay", "-i"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        paused = False
    else:
        print("Audio is not paused.")

def stop():
    """
    Stop the currently playing audio.
    """
    global process
    global paused

    if process is not None:
        process.terminate()
        process = None
        paused = False
    else:
        print("No audio is currently playing.")
