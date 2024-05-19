import pygame
import math
import random

class AudioBar:
    def __init__(self, screen_w, screen_h, x, y, freq, color=(255, 255, 255), width=3, min_height=0, max_height=100, min_decibel=-80, max_decibel=0,
    shrink_speed=20, grow_speed=40, angle=0, radius=0, color_cycle=False, color_speed=100, gen_sparks=False):  
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

        self.render_type = {"default" : False, "default2" : False, "top" : False, "bottom" : False, "middle" : False, "circle" : 0, "circle_inner" : False, "ring" : False} # All render types. Only 1 can be active at a time
        #Future ideas: rain, balls, top, left, right, double side, top and bottom, wave(differnt class maybe?)

        # Spark attributes
        self.sparks = []
        self.gen_sparks = gen_sparks # Decide to render sparks or not
        self.set_spark_limt(5) # Amount of active sparks per bar
        self.set_spark_spawn_rate(randomize=True) # Miliseconds between each spark creation
        self.set_spark_velocity_rate()
        self.set_spark_gravity(0.001)

        self.spark_ticks = self.spark_spawn_rate 

    def _create_spark(self):
        """
        Create the spark at the end of the bar based on the render type.
        Initialize spark position and velocity according to render type.
        Set the spark to be active and match its color to the bar's color.
        """

        # remove these once buttons are added
        self.set_spark_size(randomize=True)
        self.set_spark_spawn_rate(100)
        self.set_spark_swade()
        self.set_spark_fade_rate(0)

        # *add direction attribute for inner/outer or rise/fall

        # Create the spark at the end of the bar, depending on the render type
        if self.render_type["circle"] or self.render_type["ring"]:
            spark_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius + self.height) * math.sin(self.angle)
            
            # Velocity based on the angle
            spark_velocity_x = self.spark_velocity_rate * math.cos(self.angle)
            spark_velocity_y = self.spark_velocity_rate * math.sin(self.angle)

        elif self.render_type["circle_inner"]:
            spark_x = (self.screen_w // 2) + (self.radius - self.height) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius - self.height) * math.sin(self.angle)
            
    
            spark_velocity_x = -self.spark_velocity_rate * math.cos(self.angle)
            spark_velocity_y = -self.spark_velocity_rate * math.sin(self.angle)

        else:
            spark_x = self.x
            spark_y = self.y

            if self.render_type["default"] or self.render_type["default2"] or self.render_type["top"]:
                spark_y = self.y + self.height # Start from bottom of bar

            spark_velocity_x = 0
            spark_velocity_y = 1 * self.spark_velocity_rate
            if self.render_type["bottom"] or self.render_type["middle"]:
                spark_velocity_y = -spark_velocity_y # Make spark rise instead of fall

        self.sparks.append(Spark(spark_x, spark_y, spark_velocity_x, spark_velocity_y, 
            self.spark_size, self.spark_fade_rate, self.spark_velocity_rate, self.spark_gravity, self.color, self.spark_swade))

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

    def set_spark_limt(self, limit = 1): self.spark_limit = limit
    def set_spark_spawn_rate(self, spawn_rate = 100, randomize = False): self.spark_spawn_rate = spawn_rate if not randomize else random.uniform(100, 1000)
    def set_spark_velocity_rate(self, velocity_rate = 0.5, randomize = False): self.spark_velocity_rate = velocity_rate if not random else random.uniform(0.1, 2)
    def set_spark_gravity(self, gravity = 0.01, randomize = False): self.spark_gravity = gravity if not randomize else random.uniform(0, 0.01)
    def set_spark_size(self, size = 2, randomize = False): self.spark_size = size if not randomize else random.uniform(self.width/3, self.width/1.5)
    def set_spark_fade_rate(self, fade_rate = 0.01, randomize = False): self.spark_fade_rate = fade_rate if not randomize else random.uniform(0, 0.1)
    def set_spark_swade(self, swade = False, randomize = False): self.spark_swade = swade if not randomize else (True if random.random() <= 0.5 else False)

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

        if self.gen_sparks:
            for spark in self.sparks:
                spark.update(delta_time, self.screen_w, self.screen_h)
                if not spark.is_active():
                    self.sparks.remove(spark)

            # chance to create a spark when bar grows. Dont create spark if time is 0 (music is paused)
            if len(self.sparks) < self.spark_limit and self.height > old_height and delta_time > 0:
                if self.spark_ticks > self.spark_spawn_rate:
                    self.spark_ticks = 0
                    self._create_spark()
            self.spark_ticks +=1

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

        elif self.render_type["default2"]:
            self.y = (self.screen_h - self.height) / 2
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width // 2, self.height))

        # Top of bar alligned with top of screen
        elif self.render_type["top"]:
            self.y = 0
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
            pygame.draw.line(screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))

        elif self.render_type["circle_inner"]:
            end_x = (self.screen_w // 2) + (self.radius - self.height/1.5) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius - self.height/1.5) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)
            pygame.draw.line(screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))
        
        elif self.render_type["ring"]:
            end_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius + self.height) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)
            #This makes sure only 1 of the Audio bars draws the ring, because they all have unique angles
            if self.angle == 0:
                pygame.draw.circle(screen, self.color, (self.screen_w//2, self.screen_h//2), self.radius)
                pygame.draw.circle(screen, 'Black', (self.screen_w//2, self.screen_h//2), self.radius * 0.99)
            pygame.draw.line(screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))

        for spark in self.sparks:
            spark.render(screen)

            
class Spark:
    def __init__(self, x, y, velocity_x, velocity_y, size=2, fade_rate=0.01, velocity_rate=0.5, gravity=0.001, color=(255, 255, 255), swade = False, shape = "circle"):
        self.x, self.y = x, y
        self.velocity_x, self.velocity_y = velocity_x, velocity_y
        self.size = size 
        self.fade_rate = fade_rate
        self.velocity_rate = velocity_rate
        self.gravity = gravity
        self.color = pygame.Color(color)
        self.swade = swade
        self.shape = shape
        self.fade_rate_sum = 0
        self.swade_direction = True if random.random() <= 0.5 else False
        self.swade_sum = 0
        self.active = True

    def update(self, delta_time, screen_w, screen_h):
        """
        Update the spark's position and color over time.
        Apply gravity and fade the spark's color towards black.
        Deactivate the spark if it goes out of bounds or fades to black.
        """
        # Apply gravity to the spark
        self.velocity_y += self.gravity

        # Update the spark position
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.swade:
            if self.swade_direction:
                self.swade_sum += random.uniform(0, 0.01)
            else:
                self.swade_sum -= random.uniform(0, 0.01)
            if random.random() <= 0.05:
                self.swade_direction = not self.swade_direction
                self.swade_sum = 0
        
        self.x += self.swade_sum
        self.y += self.swade_sum

        self.fade_rate_sum += self.fade_rate

        # Fade towards black
        r, g, b, a = self.color
        r = max(0, r - self.fade_rate_sum)
        g = max(0, g - self.fade_rate_sum)
        b = max(0, b - self.fade_rate_sum)
        self.color = pygame.Color(math.ceil(r), math.ceil(g), math.ceil(b), math.ceil(a))

        # Deactivate the spark if it is fully black or outside of the display
        if ((self.y < 0 or self.y > screen_h or self.x < 0 or self.x > screen_w) or 
            (self.color.r == 0 and self.color.g == 0 and self.color.b == 0)):
            self.active = False

    def is_active(self):
        return self.active

    def render(self, screen):
        if self.shape == "rect":
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
