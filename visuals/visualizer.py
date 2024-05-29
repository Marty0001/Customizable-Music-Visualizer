import pygame
import numpy as np
import math
from visuals.audio_bar import AudioBar
from visuals.sound_wave import SoundWave
from visuals.visual_type import VisualType

'''
Visualizer class creates audio bars and tells the audio bars and sparks how to behave

Future visual types might need a differnt class than audio bars (like waves)

Args:
        screen: screen to draw/Visual on
        screen_w, screen_h: width and height of screen
'''
class Visualizer:
    def __init__(self, screen, screen_w, screen_h):
        self.__screen = screen
        self.__screen_w = screen_w
        self.__screen_h = screen_h
        self.__visual_type=VisualType.BOTTOM
        self.__color = pygame.Color((255,255,255))
        self.__hue = 0
        self.__color_cycle = False
        self.__color_speed = 0.5
        self.__smooth_enabled = False
        self.__rotation_enabled = False
        self.__rotate_ticks = 0
        self.__smoothing_factor = 1.5
        self.__rotate_speed = 10

        self.freq_range = np.arange(200, 8000, 50) # Determines number of bars
        self.bars = self.__create_audio_bars()
        self.sound_wave = SoundWave(screen, screen_w, screen_h, self.freq_range,  self.__color)
    
    # Getters for displaying info in button menu
    def get_color_speed(self): return self.__color_speed
    def get_smoothing_factor(self): return self.__smoothing_factor
    def get_rotate_speed(self): return self.__rotate_speed
    def get_bar_info(self): return self.bars[0]

    def __create_audio_bars(self):
        bars = []
        radius = min(self.__screen_w, self.__screen_h) // 4  # Radius from center of display
        bar_width = (self.__screen_w / len(self.freq_range)) # Make sure all bars can fit on screen horizontaly
        angle_step = 2 * math.pi / len(self.freq_range)  # Change in angle between each bar
        x = 0 # X position for horizontal bars

        for i, freq in enumerate(self.freq_range):
            angle = i * angle_step # Update angle
            bars.append(AudioBar(self.__screen, self.__screen_w, self.__screen_h, x, self.__screen_h//2, freq, width=bar_width, angle=angle, radius=radius, visual_type=self.__visual_type))
            x += bar_width

        return bars

    def __update_color_cycle(self, delta_time):
        """
        Update the bar's __color based on the time and __color change speed.
        Cycle through the __color hues and reset if it exceeds 360.
        """
        self.__hue += abs(delta_time * self.__color_speed)
        if self.__hue >= 360: self.__hue = 0
        hsva = (int(self.__hue), 100, 100, 100)
        self.__color.hsva = hsva

    # Shift bars array by 1 and resest tick counter
    def __rotate_bars(self):
        self.__rotate_ticks = 0
        n = len(self.bars)
        self.bars = self.bars[-1 % n:] + self.bars[:-1 % n]

    # Adjusts the bar heights based on the max hieght of its neighbors
    def __smooth_bars(self):
        
        n = len(self.bars)
        new_heights = np.array([bar.height for bar in self.bars])

        for i in range(n):
            
            # Get the index and height of previous, current, and next bar
            neighbor_indices = [(i - 1) % n, i, (i + 1) % n]
            neighbor_heights = [self.bars[j].height for j in neighbor_indices]

            average_height = sum(neighbor_heights) / len(neighbor_heights)

            max_height = max(neighbor_heights)
            
            new_heights[i] = abs(max_height  * (1 - self.__smoothing_factor) + average_height * self.__smoothing_factor)

        for i in range(n):
            self.bars[i].height = new_heights[i]
            self.bars[i].render()
    
    def change_visual_type(self, visual_type): 
        self.__visual_type = visual_type
        for bar in self.bars:
                bar.set_type(self.__visual_type)

    def change_property(self, option, value):
        if self.__visual_type in [VisualType.BOTTOM, VisualType.TOP, VisualType.MIDDLE, VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE]:
            for bar in self.bars:
                bar.change_bar_properties(option, value)
        else:
            self.sound_wave.change_wave_property(option, value)
    
    def change_spark_property(self, option, value):
        for bar in self.bars:
                bar.spark_manager.change_spark_property(option, value)
    
    # Change special property which requires the bars to share info with eachother
    def change_special_property(self, option, value):
        if "ROTATION" in option:
            if value == 0:
                self.__rotation_enabled = not self.__rotation_enabled
            else:
                self.__rotate_speed = max (1, self.__rotate_speed + value)
        elif "SMOOTH" in option:
            if value == 0:
                self.__smooth_enabled = not self.__smooth_enabled
                for bar in self.bars:
                    bar.__smooth_enabled = self.__smooth_enabled
            else:
                self.__smoothing_factor = max (0.1, min(2, self.__smoothing_factor + value))
        elif "RESET" in option:
            self.__rotation_enabled = False
            self.__rotate_speed = 10
            self.__smooth_enabled = False
            self.__smoothing_factor = 1.5
            self.bars.sort(key=lambda bar: bar.freq) # Reset to original order if rotated
            for bar in self.bars:
                    bar.__smooth_enabled = False

    def change_color_property(self, option, value):
        if "CYCLE ON/OFF" in option:
            self.__color_cycle = not self.__color_cycle
        elif "CYCLE SPEED" in option:
            self.__color_speed = max(0.1, self.__color_speed + value)
        elif "CHANGE COLOR" in option:
            self.__color = pygame.Color(value)
            for bar in self.bars:
                bar.__color = value
        elif "GLOW ON/OFF" in option:
            for bar in self.bars:
                bar.glow_enabled = not bar.glow_enabled
        elif "GLOW INTENSITY" in option:
            for bar in self.bars:
                bar.glow_intensity = (max(0.1, (min(0.9, bar.glow_intensity + value))))
        elif "GLOW LENGTH" in option:
            for bar in self.bars:
                bar.glow_length = (max(0.1, (min(0.9, bar.glow_length + value))))
        elif "RESET" in option:
            self.__color_cycle = False
            self.__color_speed = 0.5
            self.__color = pygame.Color(255,255,255)
            for bar in self.bars:
                bar.glow_length = 0.2
                bar.glow_intensity = 0.5
                bar.glow_enabled = False
            self.change_special_property("SMOOTHING", 0)
    
    def change_preset(self, option):
        
        for bar in self.bars:
            bar.change_bar_properties("RESET BARS", 0)
            bar.change_bar_properties("RESET CIRCLE", 0)
            bar.spark_manager.change_spark_property("RESET SPARKS", 0)
        self.change_color_property("RESET COLORS", 0)
        self.change_special_property("RESET", 0)
        self.__color = pygame.Color(255,255,255)
        self.change_visual_type(VisualType.BOTTOM)

        if "BLACK HOLE" in option:
            self.change_visual_type(VisualType.CIRCLE_INNER)
            for bar in self.bars:
                bar.change_bar_properties("BAR WIDTH", -1)
                bar.change_bar_properties("MAX HEIGHT", -40)
                bar.change_bar_properties("RING RADIUS", -175)
                bar.change_bar_properties("RING WIDTH",-0.05 )
                bar.spark_manager.change_spark_property("SPARK", 0)
                bar.spark_manager.change_spark_property("RANDOM LIMIT", 0)
                bar.spark_manager.change_spark_property("SPAWN RATE", 50)
                bar.spark_manager.change_spark_property("RANDOM SIZE", 0)
                bar.spark_manager.change_spark_property("FADE", -0.035)
                bar.spark_manager.change_spark_property("VELOCITY", 0.2)
            self.change_color_property("CHANGE COLOR", (230, 230, 230))

        elif "SPACE" in option:
            self.change_visual_type(VisualType.MIDDLE)
            for bar in self.bars:
                bar.change_bar_properties("BAR WIDTH", -1)
                bar.spark_manager.change_spark_property("SPARK", 0)
                bar.spark_manager.change_spark_property("RANDOM LIMIT", 0)
                bar.spark_manager.change_spark_property("RANDOM SPAWN", 0)
                bar.spark_manager.change_spark_property("RANDOM SIZE", 0)
                bar.spark_manager.change_spark_property("FADE", -0.04)
                bar.spark_manager.change_spark_property("RANDOM VELOCITY", 0)
                bar.spark_manager.change_spark_property("HEIGHT THRESHOLD", 0.1)
                bar.glow_intensity = 0.6
                bar.glow_length = 0.1
            self.change_special_property("SMOOTHING", 0)
            self.change_special_property("SMOOTHING", 0.5)
            self.change_color_property("GLOW ON/OFF", 0)
            
        elif "FIRE" in option:
            self.change_visual_type(VisualType.BOTTOM)
            for bar in self.bars:
                bar.change_bar_properties("MAX HEIGHT", 50)
                bar.change_bar_properties("GROW SPEED", -0.01)
                bar.change_bar_properties("SHRINK SPEED", -0.01)
                bar.spark_manager.change_spark_property("SPARK", 0)
                bar.spark_manager.change_spark_property("RANDOM LIMIT", 0)
                bar.spark_manager.change_spark_property("SPAWN RATE", 50)
                bar.spark_manager.change_spark_property("RANDOM FADE", 0)
                bar.spark_manager.change_spark_property("RANDOM GRAVITY", 0)
                bar.spark_manager.change_spark_property("RANDOM VELOCITY", 0)
                bar.spark_manager.change_spark_property("SWADE", True)
                bar.glow_intensity = 0.6
                bar.glow_length = 0.3
            self.change_color_property("CHANGE COLOR", (255, 90, 0))
            self.change_color_property("GLOW ON/OFF", 0)
            self.change_special_property("SMOOTHING", 0)
            self.change_special_property("ROTATION", 0)
            self.change_special_property("ROTATION", -5)

        elif "LIGHT SHOW" in option:
            self.change_visual_type(VisualType.CIRCLE)
            for bar in self.bars:
                bar.change_bar_properties("MAX HEIGHT", -50)
                bar.change_bar_properties("GROW SPEED", -0.03)
                bar.change_bar_properties("SHRINK SPEED", -0.03)
                bar.spark_manager.change_spark_property("SPARK", 0)
                bar.spark_manager.change_spark_property("SPAWN RATE", 50)
                bar.spark_manager.change_spark_property("RANDOM SIZE", 0)
                bar.spark_manager.change_spark_property("FADE", -0.025)
                bar.spark_manager.change_spark_property("GRAVITY", 0.012)
                bar.spark_manager.change_spark_property("RANDOM VELOCITY", 0)
                bar.spark_manager.change_spark_property("HEIGHT THRESHOLD", 0.25)
                bar.glow_length = 0.2
            self.change_color_property("CYCLE ON/OFF", 0)
            self.change_color_property("GLOW ON/OFF", 0)
            self.change_special_property("ROTATION", 0)
            self.change_special_property("ROTATION", -7)

        elif "RAIN" in option:
            self.change_visual_type(VisualType.TOP)
            for bar in self.bars:
                bar.change_bar_properties("WIDTH", -1)
                bar.spark_manager.change_spark_property("SPARK", 0)
                bar.spark_manager.change_spark_property("RANDOM LIMIT", 0)
                bar.spark_manager.change_spark_property("RANDOM SIZE", 0)
                bar.spark_manager.change_spark_property("FADE", -0.45)
                bar.spark_manager.change_spark_property("GRAVITY", 0.015)
                bar.spark_manager.change_spark_property("RANDOM VELOCITY", 0)
            self.change_color_property("CHANGE COLOR", (0, 91, 227))
          
    def update(self, delta_time, decibel, i):

        if self.__color_cycle:
            self.__update_color_cycle(delta_time)

        if self.__visual_type not in [VisualType.CIRCLE_WAVE]:
            self.bars[i].update(delta_time, decibel, self.__color)

            # Only rotate and smooth after all bars have been updated
            if i == len(self.bars) - 1:
                if self.__rotation_enabled:
                    if self.__rotate_ticks > self.__rotate_speed:
                        self.__rotate_bars()
                    self.__rotate_ticks+=1
                if self.__smooth_enabled:
                    self.__smooth_bars()
        
        else:
            self.sound_wave.update(decibel, i, self.__color)
        
                        
        