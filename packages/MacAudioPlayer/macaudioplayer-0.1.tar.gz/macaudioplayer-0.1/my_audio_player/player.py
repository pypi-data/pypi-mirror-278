# my_audio_player/player.py

from playsound import playsound
import sys

def play():
    """
    Play an audio file located at the given file path passed as a command-line argument.
    """
    if len(sys.argv) != 2:
        print("Usage: play <path_to_audio_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    playsound(file_path)
