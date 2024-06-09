from setuptools import setup, find_packages

setup(
    name='MacAudioPlayer',
    version='0.3',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'play=my_audio_player.player:play',
        ],
    },
)
