import pygame
import numpy as np
import math
from audio_bar import AudioBar
from enum import Enum

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

    def create_audio_bars(self):
        bars = []
        radius = min(self.screen_w, self.screen_h) // 4  # Radius from center of display for circular display
        bar_width = (self.screen_w / len(self.freq_range)) # Make sure all bars can fit on screen horizontaly
        angle_step = 2 * math.pi / len(self.freq_range)  # Change in angle between each bar
        x = 0 # X position for horizontal bars

        for i, freq in enumerate(self.freq_range):
            angle = i * angle_step # Update angle
            bars.append(AudioBar(self.screen, self.screen_w, self.screen_h, x, self.screen_h//2, freq, width=bar_width, angle=angle, radius=radius))
            x += bar_width

        return bars
    
    # Change the current visual type and update every bar
    def change_visual_type(self, visual_type): 
        self.visual_type = visual_type
        for bar in self.bars:
                bar.set_type(self.visual_type.value)

    # Change a property of every audio bar
    def change_property(self, option, name):
        if self.visual_type in [VisualType.BOTTOM, VisualType.TOP, VisualType.MIDDLE, VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE]:
            for bar in self.bars:
                bar.change_bar_properties(option, name)
    
    # Change a property of every spark
    def change_spark_property(self, option, name):
        for bar in self.bars:
                bar.spark_manager.change_spark_property(option, name)

    # Update every bar
    def update(self, delta_time, decibel, i):
        if self.visual_type in [VisualType.BOTTOM, VisualType.TOP, VisualType.MIDDLE, VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE]:
            self.bars[i].update(delta_time, decibel)
        