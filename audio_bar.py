import pygame

class AudioBar:

    def __init__(self, x, y, freq, color = 'Green', width=50, min_height=1, max_height=100, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def _limit(self):
        if self.height < self.min_height:
            self.height = self.min_height
            
        if self.height > self.max_height:
            self.height = self.max_height

    def update(self, delta_time, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.01 if desired_height > self.max_height else (desired_height - self.height)/0.1 # Bigger bars move faster
        self.height += speed * delta_time

        self._limit()

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, (screen.get_height()- self.height) / 2, self.width, self.height))

    def render_bottom(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, (screen.get_height() - self.height), self.width, self.height))

    def render_middle(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, (self.y - self.height), self.width, self.height))