import pygame
import math
import random

class AudioBar:
    def __init__(self, screen_w, screen_h, x, y, freq, color=(255, 255, 255), width=3, min_height=1, max_height=100, min_decibel=-80, max_decibel=0,
    shrink_speed=20, grow_speed=40, angle=0, radius=0, color_cycle=False, color_speed=100, sparks=False):  

        self.screen_w, self.screen_h = screen_w, screen_h
        self.x, self.y = x, y
        self.freq = freq
        self.color = pygame.Color(color)
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

        self.render_type = {"default" : False, "bottom" : False, "middle" : False, "circle" : 0} # All render types. Only 1 can be active at a time
        #Future ideas: rain, balls, top, left, right, double side, top and bottom, wave(differnt class maybe?)

        # Spark attributes
        self.sparks = sparks # Decide to render sparks or not
        self.spark_active = False
        self.spark_size = 1.5 # size in pixels
        self.spark_spawn_rate = 1 # % chance to spawn spark. Must be 0-1
        self.spark_fade_rate = 0.001 # ~ 0.001-1
        self.spark_velocity_rate = 0.5 # ~ 0.1-5
        self.spark_gravity = 0.001 # ~ 0.001-0.01
        self.spark_color = pygame.Color(color)

    def _create_spark(self):
        """
        Create the spark at the end of the bar based on the render type.
        Initialize spark position and velocity according to render type.
        Set the spark to be active and match its color to the bar's color.
        """

        # Create the spark at the end of the bar, depending on the render type
        if self.render_type["circle"]:
            self.spark_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            self.spark_y = (self.screen_w // 2) + (self.radius + self.height) * math.sin(self.angle)
            
            # Velocity based on the angle
            self.spark_velocity_x = self.spark_velocity_rate * math.cos(self.angle)
            self.spark_velocity_y = self.spark_velocity_rate * math.sin(self.angle)

        else:
            self.spark_x = self.x
            self.spark_y = self.y

            if self.render_type["default"] or self.render_type["middle"]:
                self.spark_y = self.y + self.height

            self.spark_velocity_x = 0
            self.spark_velocity_y = 1 * self.spark_velocity_rate
            if self.render_type["bottom"] or self.render_type["middle"]: # Make spark rise instead of fall for different render types
                self.spark_velocity_y = -self.spark_velocity_y

        self.spark_fade_rate_sum = 0
        self.spark_color = self.color
        self.spark_active = True

    def _update_spark(self, delta_time):
        """
        Update the spark's position and color over time.
        Apply gravity and fade the spark's color towards black.
        Deactivate the spark if it goes out of bounds or fades to black.
        """

        # Apply gravity to the spark
        self.spark_velocity_y += self.spark_gravity

        # Update the spark position
        self.spark_x += self.spark_velocity_x
        self.spark_y += self.spark_velocity_y

        self.spark_fade_rate_sum +=self.spark_fade_rate

        # Fade towards black
        r, g, b, a = self.spark_color
        r = max(0, r - self.spark_fade_rate_sum)
        g = max(0, g - self.spark_fade_rate_sum)
        b = max(0, b - self.spark_fade_rate_sum)
        self.spark_color = pygame.Color(math.ceil(r), math.ceil(g), math.ceil(b), math.ceil(a))

        # Deactivate the spark if it is fully black or outside of the display
        if ((self.spark_y < 0 or self.spark_y > self.screen_h or self.spark_x < 0 or self.spark_x > self.screen_w) or 
        (self.spark_color.r == 0 and self.spark_color.g == 0 and self.spark_color.b == 0)):
            self.spark_active = False

    def _render_spark(self, screen):
        pygame.draw.circle(screen, self.spark_color, (int(self.spark_x), int(self.spark_y)), self.spark_size)

    def _update_color_cycle(self, delta_time):
        """
        Update the bar's color based on the time and color change speed.
        Cycle through the color hues and reset if it exceeds 360.
        """
        self.hue += abs(delta_time * self.color_speed)
        if self.hue >= 360: self.hue = 0
        hsva = (int(self.hue), 100, 100, 100)
        self.color.hsva = hsva
    
    def _limit(self):
        """
        Ensure the bar's height remains within the min and max height bounds.
        """
        if self.height < self.min_height:
            self.height = self.min_height
        if self.height > self.max_height:
            self.height = self.max_height

    def update(self, delta_time, decibel):
        """
        Update the bar's height and color based on the time and decibel.
        Create sparks when bar grows or update spark if already active.
        """
        old_height = self.height
        desired_height = decibel * self.__decibel_height_ratio + self.max_height
        speed = (desired_height - self.height) * self.grow_speed if desired_height > self.height else (desired_height - self.height) * self.shrink_speed
        self.height += speed * delta_time
        self._limit()
        
        if self.color_cycle:
            self._update_color_cycle(delta_time)

        if self.sparks:

            if self.spark_active:
                self._update_spark(delta_time)

            # chance to create a spark when bar grows. Dont create spark if time is 0 (music is paused)
            elif self.height > old_height*1.02 and delta_time > 0:
                if random.random() <= self.spark_spawn_rate:
                    self._create_spark()

    def render(self, screen, selected_type : str = "default"):
        """
        Render the bar on the screen based on the selected render type.
        Render the spark if it is active.
        """

        # If invalid selected type, use defualt
        if selected_type not in self.render_type: selected_type = "default"

        # Set all other types to False
        if not self.render_type[selected_type]:
            for item in self.render_type:
                item = False
            self.render_type[selected_type] = True
        
        # Middle of bar alligned with middle of screen
        if self.render_type["default"]:
            self.y = (self.screen_h - self.height) / 2
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
        # Bottom of bar alligned with botttom of screen
        elif self.render_type["bottom"]:
            self.y = self.screen_h - self.height
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Bottom of bar alligned with midle of screen
        elif self.render_type["middle"]:
            self.y = (self.screen_h/2) - self.height
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        # Bottom of bar alligned with point on circumference of circle
        elif self.render_type["circle"]:
            end_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius + self.height) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)
            pygame.draw.line(screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width * 2))

        if self.spark_active:
            self._render_spark(screen)