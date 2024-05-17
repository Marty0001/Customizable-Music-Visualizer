import pygame
import math

class AudioBar:

    def __init__(self, x, y, freq, color=(255, 255, 255), width=50, min_height=1, max_height=100, min_decibel=-80, max_decibel=0, shrink_speed = 10, grow_speed = 40, angle = 0, radius = 0, color_cycle = False, color_speed = 100):
        self.x, self.y = x, y
        self.freq = freq
        self.color = pygame.Color(*color)
        self.width = width
        self.min_height = min_height
        self.max_height = max_height
        self.height = min_height
        self.min_decibel = min_decibel
        self.max_decibel = max_decibel
        self.shrink_speed = shrink_speed
        self.grow_speed = grow_speed
        self.angle = angle
        self.radius = radius
        self.color_cycle = color_cycle
        self.color_speed = color_speed
        self.hue = 0

        self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel)

    def _change_color(self, delta_time):

        self.hue += abs(delta_time * self.color_speed)

        # Reset the color cycle when completed
        if self.hue >= 360: self.hue = 0
    
        hsva = (self.hue, 100, 100, 100)
        self.color.hsva = hsva
        
    def _limit(self):
        if self.height < self.min_height:
            self.height = self.min_height
            
        if self.height > self.max_height:
            self.height = self.max_height

    def update(self, delta_time, decibel):
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height) * self.grow_speed if desired_height > self.height else (desired_height - self.height) * self.shrink_speed

        self.height += speed * delta_time
        self._limit()

        if self.color_cycle:
            self._change_color(delta_time)

    # Default horizontal line of vertical bars alligned in the middle of the display
    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, (screen.get_height()- self.height) / 2, self.width, self.height))

    # Bottom of vertical bars attatched to bottom of display
    def render_bottom(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, (screen.get_height() - self.height), self.width, self.height))

    # Similar to default but the bottom of all bars of alligned
    def render_middle(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, ((screen.get_height()/2) - self.height), self.width, self.height))

    # Bars are arranged in a circle
    def render_circle(self, screen):
        end_x = self.x + (self.radius + self.height) * math.cos(self.angle)
        end_y = self.y + (self.radius + self.height) * math.sin(self.angle)
        start_x = self.x + self.radius * math.cos(self.angle)
        start_y = self.y + self.radius * math.sin(self.angle)
        pygame.draw.line(screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))