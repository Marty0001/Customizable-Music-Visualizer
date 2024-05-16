import pygame
import librosa
import numpy as np

class MusicPlayer:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.change_time = 0 # Cumulative count of seconds fast forwarded or reveresed
        self.is_paused = False
        pygame.mixer.music.load(audio_file)
    
    def load_audio_data(self):
        # time_series: A NumPy array representing the audio signal (amplitude values over time).
        # sample_rate: The number of samples (data points) per second (Hz).
        time_series, sample_rate = librosa.load(self.audio_file)

        # Compute STFT to get amplitude values
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048))

        # Convert amplitude to decibels
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        # Get frequencies and times
        frequencies = librosa.fft_frequencies(n_fft=2048)
        times = librosa.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048)

        # Calculate index ratios
        self.time_index_ratio = len(times) / times[-1]
        self.freq_index_ratio = len(frequencies) / frequencies[-1]
    
    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq * self.freq_index_ratio)][int(target_time * self.time_index_ratio)]

    def fast_forward(self, seconds=5):
        current_time = pygame.mixer.music.get_pos()
        self.change_time += seconds * 1000
        pygame.mixer.music.set_pos((current_time + self.change_time) / 1000)

    def reverse(self, seconds=5):
        current_time = pygame.mixer.music.get_pos()
        self.change_time -= seconds * 1000
        if current_time + self.change_time < 0: # If rewinded below 0, reload the song
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play(0)
            self.change_time = 0
        else:
            pygame.mixer.music.set_pos((current_time + self.change_time) / 1000)

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def get_current_time(self):
        return pygame.mixer.music.get_pos() + self.change_time # Time passed since song was played + cumulative change in time (fast forward or rewind)