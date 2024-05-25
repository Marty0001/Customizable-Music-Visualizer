import pygame
import numpy as np
import math
from enum import Enum
from visuals.audio_bar import AudioBar

# All visual types
class VisualType(Enum):
    BOTTOM = "BOTTOM"
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    CIRCLE = "CIRCLE"
    CIRCLE_INNER = "CIRCLE_INNER"
    CIRCLE_MIDDLE = "CIRCLE_MIDDLE"

'''
Visualizer class creates audio bars and tells the audio bars and sparks how to behave

Future visual types might need a differnt class than audio bars (like waves)

Args:
        screen: screen to draw/Visual on
        screen_w, screen_h: width and height of screen
'''
class Visualizer:
    def __init__(self, screen, screen_w, screen_h):
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.freq_range = np.arange(200, 8000, 50) # Determines number of bars
        self.bars = self.create_audio_bars()
        self.visual_type = VisualType.BOTTOM

        self.smooth_enabled = False
        self.smoothing_factor = 1.5
        self.rotation_enabled = False
        self.rotate_speed = 10
        self.rotate_ticks = 0


    def create_audio_bars(self):
        bars = []
        radius = min(self.screen_w, self.screen_h) // 4  # Radius from center of display
        bar_width = (self.screen_w / len(self.freq_range)) # Make sure all bars can fit on screen horizontaly
        angle_step = 2 * math.pi / len(self.freq_range)  # Change in angle between each bar
        x = 0 # X position for horizontal bars

        for i, freq in enumerate(self.freq_range):
            angle = i * angle_step # Update angle
            bars.append(AudioBar(self.screen, self.screen_w, self.screen_h, x, self.screen_h//2, freq, width=bar_width, angle=angle, radius=radius))
            x += bar_width

        return bars
    
    def change_visual_type(self, visual_type): 
        self.visual_type = visual_type
        for bar in self.bars:
                bar.set_type(self.visual_type.value)

    def change_property(self, option, name):
        if self.visual_type in [VisualType.BOTTOM, VisualType.TOP, VisualType.MIDDLE, VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE]:
            for bar in self.bars:
                bar.change_bar_properties(option, name)
    
    def change_spark_property(self, option, name):
        for bar in self.bars:
                bar.spark_manager.change_spark_property(option, name)
    
    # Change special property which requires the bars to share info with eachother
    def change_special_property(self, option, value):
        if "ROTATION" in option:
            if value == 0:
                self.rotation_enabled = not self.rotation_enabled
            else:
                self.rotate_speed = max (1, self.rotate_speed + value)
        elif "SMOOTH" in option:
            if value == 0:
                self.smooth_enabled = not self.smooth_enabled
                for bar in self.bars:
                    bar.smooth_enabled = self.smooth_enabled
            else:
                self.smoothing_factor = max (0.1, min(2, self.smoothing_factor + value))
        elif "RESET" in option:
            self.rotation_enabled = False
            self.rotate_speed = 10
            self.smooth_enabled = False
            self.smoothing_factor = 1.5
            self.bars.sort(key=lambda bar: bar.freq) # Reset to original order if rotated
            for bar in self.bars:
                    bar.smooth_enabled = False

    # Shift bars array by 1 and resest tick counter
    def rotate_bars(self):
        self.rotate_ticks = 0
        n = len(self.bars)
        self.bars = self.bars[-1 % n:] + self.bars[:-1 % n]

    # Adjusts the bar heights based on the max hieght of its neighbors
    def smooth_bars(self):
        
        n = len(self.bars)
        new_heights = np.array([bar.height for bar in self.bars])

        for i in range(n):
            
            # Get the index and height of previous, current, and next bar
            neighbor_indices = [(i - 1) % n, i, (i + 1) % n]
            neighbor_heights = [self.bars[j].height for j in neighbor_indices]

            average_height = sum(neighbor_heights) / len(neighbor_heights)

            max_height = max(neighbor_heights)
            
            new_heights[i] = abs(max_height  * (1 - self.smoothing_factor) + average_height * self.smoothing_factor)

        for i in range(n):
            self.bars[i].height = new_heights[i]
            self.bars[i].render()
          
    def update(self, delta_time, decibel, i):
        if self.visual_type in [VisualType.BOTTOM, VisualType.TOP, VisualType.MIDDLE, VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE]:
            self.bars[i].update(delta_time, decibel)

            # Only rotate and smooth after all bars have been updated
            if i == len(self.bars) - 1:
                if self.rotation_enabled:
                    if self.rotate_ticks > self.rotate_speed:
                        self.rotate_bars()
                    self.rotate_ticks+=1
                if self.smooth_enabled:
                    self.smooth_bars()
        
                        
        