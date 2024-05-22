import pygame
import math
import random
from spark import SparkManager

'''
Audio bar class. Each instance is 1 singular bar
 Args:
        screen: screen to draw/render on
        screen_w, screen_h: width and height of screen
        x, y: cooridinates on screen
        freq: sound frequency that the bar represents
        ...
        shrink_speed, grow_speed: rate at which the bar grows or shrinks
        angle: tilt angle for circle visual
        radius: radius of circle for circle visual
        color_cycle: whether or not to cycle through colors
        color_speed: rate at which color changes for color_cycle
'''
class AudioBar:
    def __init__(self, screen, screen_w, screen_h, x, y, freq, color=(255, 255, 255), width=3, min_height=1, max_height=200, 
    min_decibel=-80, max_decibel=0, shrink_speed=20, grow_speed=40, angle=0, radius=0, color_cycle=True, color_speed=50): 
        self.screen = screen 
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

        # Save original values if they need to be reset
        self.ring_size = 0.99
        self.original_width = width
        self.original_x = x
        self.original_y = y
        self.original_grow_speed = grow_speed
        self.original_shrink_speed = shrink_speed
        self.original_max_height = max_height
        self.origingal_min_height = min_height
        self.original_radius = self.radius
        self.ring_radius = self.radius

        self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel) 

        self.visual_type = "CIRCLE"

        self.spark_manager = SparkManager()
    
    def _update_color_cycle(self, delta_time):
        """
        Update the bar's color based on the time and color change speed.
        Cycle through the color hues and reset if it exceeds 360.
        """
        self.hue += abs(delta_time * self.color_speed)
        if self.hue >= 360: self.hue = 0
        hsva = (int(self.hue), 100, 100, 100)
        self.color.hsva = hsva

    def _get_spark_position_and_velocity(self):
        """
        Get the inital spark position and velocity based on the current visual type
        """

        # Make sparks fly outward
        if self.visual_type == "CIRCLE":
            spark_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius + self.height) * math.sin(self.angle)
            spark_velocity_x = self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = self.spark_manager.properties.velocity_rate * math.sin(self.angle)
        
        # Make sparks fly outward, audjust starting position for half height
        elif self.visual_type == "CIRCLE_MIDDLE":
            spark_x = (self.screen_w // 2) + (self.radius + self.height/2) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius + self.height/2) * math.sin(self.angle)
            spark_velocity_x = self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = self.spark_manager.properties.velocity_rate * math.sin(self.angle)

        # Make sparks fly inward, audjust starting position for half height
        elif self.visual_type == "CIRCLE_INNER":
            spark_x = (self.screen_w // 2) + (self.radius - self.height/2) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius - self.height/2) * math.sin(self.angle)
            spark_velocity_x = -self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = -self.spark_manager.properties.velocity_rate * math.sin(self.angle)

        else:
            spark_x, spark_y = self.x, self.y # Start at same position as bar by default
            spark_velocity_x = 0 # Only vertical movement
            spark_velocity_y = 1 * self.spark_manager.properties.velocity_rate # Falls by default

            # Spark starts at bottom of bar
            if self.visual_type == "TOP":
                spark_y += self.height

            # Spark randomly starts at top or bottom and falls or rises
            elif self.visual_type == "MIDDLE":
                spark_y += self.height
                if random.choice([True, False]):
                        spark_velocity_y = -spark_velocity_y
                        spark_y -=self.height

            # Spark starts at top of bar and rises
            if self.visual_type == "BOTTOM":
                spark_velocity_y = -spark_velocity_y
                
        return spark_x, spark_y, spark_velocity_x, spark_velocity_y
    
    def _limit(self):
        """
        Ensure the bar's height remains within the min and max height bounds.
        """
        if self.height < self.min_height:
            self.height = self.min_height
        if self.height > self.max_height:
            self.height = self.max_height

    def change_bar_properties(self, option, value):
        """
        Change properties on button press
        """
        if "WIDTH" in option:
            self.width = max(0, self.width + value)
        elif "MAX" in option:
            self.max_height = max(0, self.max_height + value)
        elif "MIN" in option:
            self.min_height = max(0, self.min_height + value)
        elif "GROW" in option:
            self.grow_speed = max(1, self.grow_speed + value)
        elif "SHRINK" in option:
            self.shrink_speed = max(1, self.shrink_speed + value)
        elif "RESET BARS" in option:
            self.width = self.original_width
            self.max_height = self.original_max_height
            self.min_height = self.origingal_min_height
            self.grow_speed = self.original_grow_speed
            self.shrink_speed = self.original_shrink_speed
        elif "RING SIZE" in option:
            self.ring_size = min(1, self.ring_size + value)
        elif "RING RADIUS" in option:
            self.ring_radius = max(0, self.ring_radius + value)
        elif "RADIUS" in option:
            self.radius = max(0, self.radius + value)
        elif "RESET CIRCLE" in option:
            self.radius = self.original_radius
            self.ring_radius = self.original_radius
            self.ring_size = 0.99

              
    def set_type(self, visual_type): self.visual_type = visual_type

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
        
        if self.spark_manager.gen_sparks:
            self.spark_manager.update_sparks(delta_time, self.screen_w, self.screen_h)

            # If current spark amount is less than spark_limit and the bar is growing the music is not paused:
            if len(self.spark_manager.sparks) < self.spark_manager.properties.limit and self.height > old_height and delta_time > 0:
                # If ms ticks since last spark creation is greater than the spawn rate, reset the ticks, and create spark
                if self.spark_manager.spark_ticks > self.spark_manager.properties.spawn_rate:
                    self.spark_manager.spark_ticks = 0
                    spark_x, spark_y, spark_velocity_x, spark_velocity_y = self._get_spark_position_and_velocity()
                    self.spark_manager.create_spark(spark_x, spark_y, spark_velocity_x, spark_velocity_y, self.color)
            self.spark_manager.spark_ticks += 1
        
        self.render()

    def render(self):
        """
        Render the bar on the screen based on the selected render type.
        Render the spark if it is active.
        """
        # Bottom of bar alligned with botttom of screen
        if self.visual_type == "BOTTOM":
            self.y = self.screen_h - self.height
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Top of bar alligned with top of screen
        elif self.visual_type == "TOP":
            self.y = 0
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Middle of bar alligned with midle of screen
        elif self.visual_type == "MIDDLE":
            self.y = (self.screen_h - self.height) / 2
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Bottom of bar alligned with point on circumference of circle and points outwards
        elif self.visual_type == "CIRCLE":
            end_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius + self.height) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)

            # Draw the ring only if the angle is 0. This makes sure only 1 of the bars is rendering it
            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))

        # Bottom of bar alligned with point on circumference of circle and points inwards. Adjust bar size
        elif self.visual_type == "CIRCLE_INNER":
            
            # Divide height by 2 because bigger bars for this option look bad
            end_x = (self.screen_w // 2) + (self.radius - self.height/2) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius - self.height/2) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)

            # Draw the ring only if the angle is 0. This makes sure only 1 of the bars is rendering it
            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width * 0.85))

        # Middle of bar alligned with point on circumference of circle
        elif self.visual_type == "CIRCLE_MIDDLE":

            # Divide height by 2 because bigger bars for this option look bad
            end_x = (self.screen_w // 2) + (self.radius + self.height/2) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius + self.height/2) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + (self.radius - self.height/2) * math.cos(self.angle)
            start_y = (self.screen_h // 2) + (self.radius - self.height/2) * math.sin(self.angle)

            # Draw the ring only if the angle is 0. This makes sure only 1 of the bars is rendering it
            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))
        
        if self.spark_manager.gen_sparks:
            self.spark_manager.render_sparks(self.screen)