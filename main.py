import pygame
import os
from music_player import MusicPlayer
from visualizer import Visualizer
from button import ButtonMenu

PLAYLIST = 'playlist' # Folder containing .mp3 and .wav files
HIDE_MENU = False

def handle_key_presses(event, music_player):
    global HIDE_MENU
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
        elif event.key == pygame.K_TAB:
            HIDE_MENU = not HIDE_MENU

def main(playlist):
   
    # Set up the screen
    pygame.init()
    pygame.display.set_caption("Audio Visualizer")
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 2)
    screen_h = screen_w
    screen = pygame.display.set_mode([screen_w, screen_h])

    # Create visualizer
    visualizer = Visualizer(screen, screen_w, screen_h)

    # Create buttons
    buttons = ButtonMenu(screen, visualizer)

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
        for i, freq in enumerate(visualizer.freq_range):
            visualizer.update(delta_time, music_player.get_decibel(current_ticks / 1000.0, freq), i)

        # Display buttons
        if not HIDE_MENU:
            buttons.update()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    # Create the full path for each song/audio file
    songs = os.listdir(PLAYLIST)
    playlist = [os.path.join(PLAYLIST, song) for song in songs 
                if os.path.isfile(os.path.join(PLAYLIST, song)) and song.lower().endswith(('.mp3', '.wav'))]
    main(playlist)