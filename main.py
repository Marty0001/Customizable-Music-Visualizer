import numpy as np
import pygame
import math
import os
from music_player import MusicPlayer
from audio_bar import AudioBar

PLAYLIST = 'playlist' # Folder containing .mp3 and .wav files

# Create array of AudioBars, each representing a different frequency
def create_audio_bars(screen_w, screen_h):
    bars = []
    radius = min(screen_w, screen_h) // 4  # Radius from center of display for circular display
    freq_range = np.arange(200, 8000,50) # Determines number of bars
    bar_width = (screen_w / len(freq_range)) / 2 # Make sure all bars can fit on screen horizontaly
    angle_step = 2 * math.pi / len(freq_range)  # Change in angle between each bar
    x = 0 # X position for horizontal bars

    for i, freq in enumerate(freq_range):
        angle = i * angle_step
        bars.append(AudioBar(screen_w, screen_h, x, screen_h//2, freq, max_height=100, width=bar_width, angle=angle, radius=radius, color_cycle=True, color_speed=10, gen_sparks=True))
        x += bar_width * 2

    return bars

def handle_key_presses(event, music_player):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_SHIFT: # SHIFT + R ARROW KEY
            music_player.next()
        elif event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_SHIFT: # SHIFT + L ARROW KEY
            music_player.prev()
        elif event.key == pygame.K_RIGHT:
            music_player.fast_forward(5)
        elif event.key == pygame.K_LEFT:
            music_player.rewind(5)
        elif event.key == pygame.K_SPACE:
            music_player.pause()

def main(playlist):
   
    # Set up the screen
    pygame.init()
    pygame.display.set_caption("Audio Visualizer")
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 2.5)
    screen_h = screen_w
    screen = pygame.display.set_mode([screen_w, screen_h])

    # Create audio bars
    bars = create_audio_bars(screen_w, screen_h)

    # Create MusicPlayer object which contains entire playlist of songs
    music_player = MusicPlayer(playlist)
    music_player.play()
    
    # Initialize timing
    last_frame_ticks = music_player.get_current_time()

    running = True
    while running:

        # If the current song time is within 100ms of the length, go to next song to avoid OOB error
        if((music_player.get_current_time()) >= music_player.get_length() - 100):
            music_player.next()
            last_frame_ticks = 0

        # Calculate time difference
        current_ticks = music_player.get_current_time()
        delta_time = (current_ticks - last_frame_ticks) / 1000.0
        last_frame_ticks = current_ticks

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
            handle_key_presses(event, music_player)

        screen.fill('Black')

        # Display bars
        for bar in bars:
            bar.update(delta_time, music_player.get_decibel(current_ticks / 1000.0, bar.freq))
            bar.render(screen, "circle")
       
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    # Create the full path for each song/audio file
    songs = os.listdir(PLAYLIST)
    playlist = [os.path.join(PLAYLIST, song) for song in songs 
                if os.path.isfile(os.path.join(PLAYLIST, song)) and song.lower().endswith(('.mp3', '.wav'))]
    main(playlist)