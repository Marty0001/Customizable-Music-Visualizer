import pygame
import numpy as np
import math

class SoundWave:
    def __init__(self, screen, screen_w, screen_h, freq_range, color):
        self.__screen = screen
        self.__screen_w = screen_w
        self.__screen_h = screen_h
        self.__freq_range = freq_range
        self.__num_points = len(freq_range)
        self.__wave_points = [(x, screen_h // 2) for x in np.linspace(0, screen_w, self.__num_points)]
        self.__color = color
        self.__radius = min(self.__screen_w, self.__screen_h) // 2
        self.__width = 2
    
    def change_wave_property(self, option, value):
        if "WIDTH" in option:
            self.__width = min(1, self.__width + value)
        elif "RADIUS" in option:
            self.__radius = max(0, self.__radius + value)
        elif "RESET CIRCLE" in option:
            self.__radius = min(self.__screen_w, self.__screen_h) // 2
            self.__width = 2

    def update(self, decibel_level, index, color):
        amplitude_factor = self.__screen_h // 4

        # Update the specific point based on the decibel level
        x = np.linspace(0, self.__screen_w, self.__num_points)[index]
        y = self.__screen_h // 2 - amplitude_factor * (decibel_level / self.__num_points)
        self.__wave_points[index] = (x, y//2)

        self.__color = color

        if index == len(self.__freq_range) - 1:
            self.render()

    def render(self):
        angle_step = 2 * math.pi / self.__num_points
        center = (self.__screen_w // 2, self.__screen_h // 2)
        circle_points = [
            (
                center[0] - (self.__radius*2 * (y - self.__radius) / (self.__radius)) * math.cos(i * angle_step),
                center[1] - (self.__radius*2  * (y - self.__radius) / (self.__radius)) * math.sin(i * angle_step),
            )
            for i, (x, y) in enumerate(self.__wave_points)
        ]
        pygame.draw.lines(self.__screen, self.__color, True, circle_points, self.__width)
