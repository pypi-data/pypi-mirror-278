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

