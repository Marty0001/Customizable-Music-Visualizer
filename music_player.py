import pygame
import librosa
import numpy as np

class MusicPlayer:
    def __init__(self, playlist):
        self.track_num = 0
        self.playlist = playlist # List of paths to audio files.
        self.current_song = self.playlist[self.track_num]
        self.change_time = 0 # Cumulative count of seconds fast forwarded or reveresed
        self.is_paused = False
    
    def _load_audio_data(self):
        """
        Load and process audio data for the current song for vizualization.

        Computes the Short-Time Fourier Transform (STFT) of the audio signal, 
        converts it to decibels, and calculates index ratios for time and frequency.
        """
        # time_series: A NumPy array representing the audio signal (amplitude values over time).
        # sample_rate: The number of samples (data points) per second (Hz).
        time_series, sample_rate = librosa.load(self.current_song)

        # Compute STFT to get amplitude values
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048))

        # Convert amplitude to decibels
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        # Get frequencies and times
        frequencies = librosa.fft_frequencies(n_fft=2048)
        times = librosa.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048)
        self.length = round(times[-1], 2) * 1000

        # Calculate index ratios
        self.time_index_ratio = len(times) / times[-1]
        self.freq_index_ratio = len(frequencies) / frequencies[-1]
    
    def get_decibel(self, target_time, freq):
        """
        Get the decibel level at a specific time and frequency.

        Args:
            target_time (float): The time in seconds.
            freq (float): The frequency in Hz.

        Returns:
            float: The decibel level at the specified time and frequency.
        """
        return self.spectrogram[int(freq * self.freq_index_ratio)][int(target_time * self.time_index_ratio)]

    def get_length(self):
        """
        Return the length of the current song in miliseconds
        """
        return self.length

    def fast_forward(self, seconds=5):
        """
        Fast forward the current song by a specified number of seconds.
        Play the next song if fast forward is beyond length to avoid error.
        """
        
        current_time = pygame.mixer.music.get_pos()
        if current_time + (seconds * 1000) < self.get_length():
            self.change_time += seconds * 1000
            pygame.mixer.music.set_pos((current_time + self.change_time) / 1000)
        else:
            self.next()

    def rewind(self, seconds=5):
        """
        Rewind the current song by a specified number of seconds.
        """
        current_time = pygame.mixer.music.get_pos()
        self.change_time -= seconds * 1000

        # If rewinded below 0, reload the song because change_time will no longer work. 
        # Not using self.play() to avoid reloading audio data again
        if current_time + self.change_time < 0:
            self.stop()
            pygame.mixer.music.load(self.current_song)
            self.change_time = 0
            pygame.mixer.music.play()
            if self.is_paused:
                pygame.mixer.music.pause()
        else:
            pygame.mixer.music.set_pos((current_time + self.change_time) / 1000)

    def play(self):
        """
        Get the audio data for current song, reset the change_time, and play it.
        """
        self._load_audio_data()
        self.change_time = 0
        pygame.mixer.music.load(self.current_song)
        pygame.mixer.music.play()

    def pause(self):
        """
        Pause current song
        """
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        """
        Stop playing current song
        """
        pygame.mixer.music.unload()

    def next(self):
        """
        Play the next song in the playlist.
        If the current song is the last one in the playlist, loop back to the first song.
        """
        self.stop()
        self.track_num = 0 if self.track_num == len(self.playlist) - 1 else self.track_num + 1
        self.current_song = self.playlist[self.track_num]
        self.play()
    
    def prev(self):
        """
        Play the previous song in the playlist.
        If the current song is the first one in the playlist, loop back to the last song.
        """
        self.stop()
        self.track_num = len(self.playlist) - 1 if self.track_num == 0 else self.track_num - 1
        self.current_song = self.playlist[self.track_num]
        self.play()

    def get_current_time(self):
        """
        Get the current playback position of the song in milliseconds,
        including any fast forward or rewind adjustments.
        """
        return pygame.mixer.music.get_pos() + self.change_time