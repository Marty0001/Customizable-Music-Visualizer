import librosa
import numpy as np
import pygame
from audio_bar import AudioBar

AUDIO_FILE = 'hope.mp3'

def load_audio_data(audio_file):
    # time_series: A NumPy array representing the audio signal (amplitude values over time).
    # sample_rate: The number of samples (data points) per second (Hz).
    time_series, sample_rate = librosa.load(audio_file)

    # Compute STFT to get amplitude values
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048))

    # Convert amplitude to decibels
    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

    # Get frequencies and times
    frequencies = librosa.fft_frequencies(n_fft=2048)
    times = librosa.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048)

    # Calculate index ratios
    time_index_ratio = len(times) / times[-1]
    freq_index_ratio = len(frequencies) / frequencies[-1]

    return spectrogram, time_index_ratio, freq_index_ratio

def create_audio_bars(screen_w, screen_h):
    # Create AudioBar for multiple frequencies
    bars = []
    freq_range = np.arange(0, 8000, 50)
    bar_width = screen_w / len(freq_range)
    x = (screen_w - bar_width * len(freq_range)) / 2

    for freq in freq_range:
        bars.append(AudioBar(x, screen_h / 2, freq, max_height=screen_h / 3, width=bar_width))
        x += bar_width

    return bars

def main(audio_file):
    # Load audio data
    spectrogram, time_index_ratio, freq_index_ratio = load_audio_data(audio_file)

    # Return the decibel level at the curent target_time
    def get_decibel(target_time, freq):
        return spectrogram[int(freq * freq_index_ratio)][int(target_time * time_index_ratio)]

    # Set up the screen
    pygame.init()
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 4)
    screen_h = screen_w
    screen = pygame.display.set_mode([screen_w, screen_h])

    # Create audio bars
    bars = create_audio_bars(screen_w, screen_h)

    # Initialize timing
    last_frame_ticks = pygame.time.get_ticks()

    # Load and play audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(0)
    change_time = 0

    running = True
    while running:
        # Calculate time difference
        
        current_ticks = pygame.mixer.music.get_pos() + change_time
        print(current_ticks)
        delta_time = (current_ticks - last_frame_ticks) / 1000.0
        last_frame_ticks = current_ticks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Fast forward by 5 seconds
                    
                    current_time = pygame.mixer.music.get_pos()
                    change_time +=5000
                    pygame.mixer.music.set_pos((current_time + change_time)/1000)
                   
                elif event.key == pygame.K_LEFT:
                    # Reverse by 5 seconds
                    
                    current_time = pygame.mixer.music.get_pos()
                    change_time -=5000
                    if(current_time + change_time < 0):
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play(0)
                        change_time = 0
                    else:
                        pygame.mixer.music.set_pos((current_time + change_time)/1000)

        screen.fill('Black')

        # Display bars
        skip = False # Makee gap between each bar
        for bar in bars:
            if not skip:
                bar.update(delta_time, get_decibel(current_ticks / 1000.0, bar.freq))
                bar.render(screen)
            skip = not skip

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main(AUDIO_FILE)
