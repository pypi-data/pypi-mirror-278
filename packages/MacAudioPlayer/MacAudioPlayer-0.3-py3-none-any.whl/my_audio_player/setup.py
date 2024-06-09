from setuptools import setup, find_packages

setup(
    name='MacAudioPlayer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'playsound',
    ],
    entry_points={
        'console_scripts': [
            'play=my_audio_player.player:play',
        ],
    },
)
