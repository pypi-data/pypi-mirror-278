# my_audio_player/player.py

import os
import sys
import subprocess

def play():
    """
    Play an audio file located at the given file path passed as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: play <path_to_audio_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        subprocess.run(["afplay", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to play the file '{file_path}'.")
        print(e)
        sys.exit(1)

def stop():
    cmd = ["killall", "afplay"]
    subprocess.run(cmd)


if __name__ == "__main__":
    play()
