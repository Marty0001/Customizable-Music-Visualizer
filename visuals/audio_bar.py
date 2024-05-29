import pygame
import math
import random
from visuals.spark import SparkManager
from visuals.visual_type import VisualType

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
    def __init__(self, screen, screen_w, screen_h, x, y, freq, width, angle=0, radius=0, visual_type = VisualType.CIRCLE): 
        self.__visual_type = visual_type
        self.screen = screen 
        self.screen_w, self.screen_h = screen_w, screen_h
        self.x, self.y = x, y
        self.freq = freq
        self.width = width
        self.angle = angle
        self.radius = radius
        self.min_height = 1
        self.max_height = 200
        self.height = self.min_height
        self.min_decibel = -80
        self.max_decibel = 0
        self.shrink_speed = 0.05
        self.grow_speed = 0.05
        self.color = pygame.Color((255,255,255))
        self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel) 
    
        # Save original values if they need to be reset
        self.ring_size = 0.99
        self.ring_radius = self.radius
        self.__original_width = width
        self.__original_x = x
        self.__original_y = y
        self.__original_grow_speed = self.grow_speed
        self.__original_shrink_speed = self.shrink_speed
        self.__original_max_height = self.max_height
        self.__origingal_min_height = self.min_height
        self.__original_radius = self.radius

        # Glow properties
        self.glow_enabled = False
        self.glow_intensity = 0.5
        self.glow_length = 0.2

        self.smooth_enabled = False

        self.spark_manager = SparkManager()
    
    def __get_spark_position_and_velocity(self):
        """
        Get the inital spark position and velocity based on the current visual type
        """

        # Make sparks fly outward
        if self.__visual_type == VisualType.CIRCLE:
            spark_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius + self.height) * math.sin(self.angle)
            spark_velocity_x = self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = self.spark_manager.properties.velocity_rate * math.sin(self.angle)
        
        # Make sparks fly outward, audjust starting position for half height and bigger radius
        elif self.__visual_type == VisualType.CIRCLE_MIDDLE:
            spark_x = (self.screen_w // 2) + (self.radius*1.5 + self.height/2) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius*1.5 + self.height/2) * math.sin(self.angle)
            spark_velocity_x = self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = self.spark_manager.properties.velocity_rate * math.sin(self.angle)

        # Make sparks fly inward, audjust starting position for bigger radius
        elif self.__visual_type == VisualType.CIRCLE_INNER:
            spark_x = (self.screen_w // 2) + (self.radius*1.5 - self.height) * math.cos(self.angle)
            spark_y = (self.screen_w // 2) + (self.radius*1.5 - self.height) * math.sin(self.angle)
            spark_velocity_x = -self.spark_manager.properties.velocity_rate * math.cos(self.angle)
            spark_velocity_y = -self.spark_manager.properties.velocity_rate * math.sin(self.angle)

        else:
            spark_x, spark_y = self.x, self.y # Start at same position as bar by default
            spark_velocity_x = 0 # Only vertical movement
            spark_velocity_y = 1 * self.spark_manager.properties.velocity_rate # Falls by default

            # Spark starts at bottom of bar
            if self.__visual_type == VisualType.TOP:
                spark_y += self.height

            # Spark randomly starts at top or bottom and falls or rises
            elif self.__visual_type == VisualType.MIDDLE:
                spark_y += self.height
                if random.choice([True, False]):
                        spark_velocity_y = -spark_velocity_y
                        spark_y -=self.height

            # Spark starts at top of bar and rises
            if self.__visual_type == VisualType.BOTTOM:
                spark_velocity_y = -spark_velocity_y
                
        return spark_x, spark_y, spark_velocity_x, spark_velocity_y
    
    def __limit(self):
        if self.height < self.min_height:
            self.height = self.min_height
        if self.height > self.max_height:
            self.height = self.max_height

    def __render_glow(self, start_pos=None):
        initial_color = self.color
        alpha = 32
        
        def fade_color(color, alpha = 0, rate = 1):
            r, g, b, a = color
            r *= rate 
            g *= rate
            b *= rate
            a = alpha
            return pygame.Color(math.ceil(r), math.ceil(g), math.ceil(b), math.ceil(a))
            
        # All non circular types use pygame surface with SRCALPHA for transparencey because it looks better
        # Circular types can't use it because of preformance issues with the draw.line on a surface
        if self.__visual_type not in {VisualType.CIRCLE, VisualType.CIRCLE_INNER, VisualType.CIRCLE_MIDDLE, VisualType.CIRCLE_WAVE}:
        
            for i in range(1, 5):
                color = fade_color(initial_color, alpha = alpha)
                alpha *= self.glow_intensity  # glow_intensity is 0.1 - 0.9 so alpha is basically reduced by a percentage

                fading_surface = pygame.Surface((self.width, self.height * self.glow_length), pygame.SRCALPHA)
                fading_surface.fill(color)
                
                if self.__visual_type == VisualType.BOTTOM:
                    self.screen.blit(fading_surface, (self.x, self.y - self.height * (self.glow_length * i)))
                elif self.__visual_type == VisualType.TOP:
                    self.screen.blit(fading_surface, (self.x, self.y + self.height * (self.glow_length * i + (1 - self.glow_length))))
                elif self.__visual_type == VisualType.MIDDLE:
                    self.screen.blit(fading_surface, (self.x, self.y - self.height * (self.glow_length * i)))
                    self.screen.blit(fading_surface, (self.x, self.y + self.height * (self.glow_length * i + (1 - self.glow_length))))
                initial_color = color   

        else:
            # Initialize the start cooridinates to the same start coordinates as the bar
            end_x = start_pos[0]
            end_y = start_pos[1]
            for i in range(1, 5):
                
                color = fade_color(initial_color, rate = self.glow_intensity)

                if self.__visual_type == VisualType.CIRCLE or self.__visual_type == VisualType.CIRCLE_MIDDLE:
                    # Increment the end coordinates by a percentage of the bar height
                    end_x += self.height * self.glow_length * math.cos(self.angle)
                    end_y += self.height * self.glow_length * math.sin(self.angle)
                    pygame.draw.line(self.screen, color, start_pos, (int(end_x), int(end_y)), int(self.width))

                elif self.__visual_type == VisualType.CIRCLE_INNER:
                    end_x -= self.height * self.glow_length * math.cos(self.angle)
                    end_y -= self.height * self.glow_length * math.sin(self.angle)
                    pygame.draw.line(self.screen, color, start_pos, (int(end_x), int(end_y)), int(self.width))
                
                # Start coordinates are now the end coordinates of the last glow bar
                start_pos = (int(end_x), int(end_y))
                initial_color = color

    def change_bar_properties(self, option, value):
        """
        Change properties on button press
        Make sure to update the decible height ratio when max or min height is changed
        """
        if "BAR WIDTH" in option:
            self.width = max(0, self.width + value)
        elif "MAX" in option:
            self.max_height = max(0, self.max_height + value)
            self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel) 
        elif "MIN" in option:
            self.min_height = max(0, self.min_height + value)
            self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel) 
        elif "GROW" in option:
            self.grow_speed = max(0.01, self.grow_speed + value)
        elif "SHRINK" in option:
            self.shrink_speed = max(0.01, self.shrink_speed + value)
        elif "RESET BARS" in option:
            self.width = self.__original_width
            self.max_height = self.__original_max_height
            self.min_height = self.__origingal_min_height
            self.grow_speed = self.__original_grow_speed
            self.shrink_speed = self.__original_shrink_speed
            self.__decibel_height_ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel) 
        elif "RING WIDTH" in option:
            self.ring_size = min(1, self.ring_size + value)
        elif "RING RADIUS" in option:
            self.ring_radius = max(0, self.ring_radius + value)
        elif "RADIUS" in option:
            self.radius = max(0, self.radius + value)
        elif "RESET CIRCLE" in option:
            self.radius = self.__original_radius
            self.ring_radius = self.__original_radius
            self.ring_size = 0.99
              
    def set_type(self, visual_type): self.__visual_type = visual_type

    def update(self, delta_time, decibel, color):
        """
        Update the bar's height and color based on the time and decibel.
        Create sparks when bar grows or update spark if already active.
        """
        
        old_height = self.height
        desired_height = (decibel * self.__decibel_height_ratio + self.max_height) 
        speed = (desired_height - self.height)/self.grow_speed if desired_height > self.height else (desired_height - self.height)/self.shrink_speed
       
        self.height = self.height + speed * delta_time 

        self.__limit()

        self.color = color
        
        if self.spark_manager.gen_sparks:
            self.spark_manager.update_sparks(delta_time, self.screen_w, self.screen_h)

            # If current spark amount is less than spark_limit and the bar is growing and the height is above the threshold and the music is not paused:
            if ((len(self.spark_manager.sparks) < self.spark_manager.properties.limit) and (desired_height > old_height) and 
            (self.height > self.max_height*self.spark_manager.properties.threshold) and (delta_time > 0)):
                # If ms ticks since last spark creation is greater than the spawn rate, reset the ticks, and create spark
                if self.spark_manager.spark_ticks > self.spark_manager.properties.spawn_rate:
                    self.spark_manager.spark_ticks = 0
                    spark_x, spark_y, spark_velocity_x, spark_velocity_y = self.__get_spark_position_and_velocity()
                    self.spark_manager.create_spark(spark_x, spark_y, spark_velocity_x, spark_velocity_y, self.color)
            self.spark_manager.spark_ticks += 1

        # If smooth is enabled, let the visualizer class render indstead after the new heights have been assigned
        if not self.smooth_enabled:
            self.render()

    def render(self):
        end_x, end_y = 0,0
        # Bottom of bar alligned with botttom of screen
        if self.__visual_type == VisualType.BOTTOM:
            self.y = self.screen_h - self.height
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Top of bar alligned with top of screen
        elif self.__visual_type == VisualType.TOP:
            self.y = 0
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Middle of bar alligned with midle of screen
        elif self.__visual_type == VisualType.MIDDLE:
            self.y = (self.screen_h - self.height) / 2
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

        # Bottom of bar alligned with point on circumference of circle and points outwards
        elif self.__visual_type == VisualType.CIRCLE:
            end_x = (self.screen_w // 2) + (self.radius + self.height) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius + self.height) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius * math.sin(self.angle)

            # Draw the ring only if the angle is 0. This makes sure only 1 of the bars is rendering it
            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))

        # Bottom of bar alligned with point on circumference of circle and points inwards. Adjust radius otherwise default size bars overlap
        elif self.__visual_type == VisualType.CIRCLE_INNER:
            
            # Divide height by 2 because bigger bars for this option look bad
            end_x = (self.screen_w // 2) + (self.radius*1.5 - self.height) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius*1.5 - self.height) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + self.radius*1.5 * math.cos(self.angle)
            start_y = (self.screen_h // 2) + self.radius*1.5 * math.sin(self.angle)

            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius*1.5)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius*1.5 * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width * 0.85))

        # Middle of bar alligned with point on circumference of circle. Audjust height and radius otherwise default size bars overlap
        elif self.__visual_type == VisualType.CIRCLE_MIDDLE:

            # Divide height by 2 because bigger bars for this option look bad
            end_x = (self.screen_w // 2) + (self.radius*1.5 + self.height/2) * math.cos(self.angle)
            end_y = (self.screen_h // 2) + (self.radius*1.5 + self.height/2) * math.sin(self.angle)
            start_x = (self.screen_w // 2) + (self.radius*1.5 - self.height/2) * math.cos(self.angle)
            start_y = (self.screen_h // 2) + (self.radius*1.5 - self.height/2) * math.sin(self.angle)

            if self.angle == 0:
                pygame.draw.circle(self.screen, self.color, (self.screen_w//2, self.screen_h//2), self.ring_radius)
                pygame.draw.circle(self.screen, 'Black', (self.screen_w//2, self.screen_h//2), self.ring_radius * self.ring_size)

            pygame.draw.line(self.screen, self.color, (int(start_x), int(start_y)), (int(end_x), int(end_y)), int(self.width))
        
        if self.glow_enabled: self.__render_glow(start_pos=(int(end_x), int(end_y)))

        if self.spark_manager.gen_sparks: self.spark_manager.render_sparks(self.screen)