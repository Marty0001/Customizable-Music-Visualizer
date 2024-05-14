from pydub import AudioSegment
from pydub.playback import play
import os

def main(audio_file):
   
    audio = AudioSegment.from_file(audio_file, format="mp3")
    play(audio)

if __name__ == "__main__":
    audio_file = "risk-of-rain.mp3"
    main(audio_file)