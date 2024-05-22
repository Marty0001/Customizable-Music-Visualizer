import pygame
import random
import math

'''
Spark class responsible for rendering and updating the spark
'''
class Spark:
    def __init__(self, x, y, velocity_x, velocity_y, size, fade_rate, velocity_rate, gravity, color, swade, shape = "circle"):
        self.x, self.y = x, y
        self.velocity_x, self.velocity_y = velocity_x, velocity_y
        self.size = size 
        self.fade_rate = fade_rate
        self.velocity_rate = velocity_rate
        self.gravity = gravity
        self.color = pygame.Color(color)
        self.swade = swade
        self.shape = shape

        self.swade_direction = random.choice([True, False])
        self.fade_rate_sum = 0
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

        # Make spark randomly swade back and fourth smoothly
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

'''
SparkProperties class responsible for holding behavior properties of spark
'''
class SparkProperties:
    def __init__(self, limit=2, spawn_rate=50, velocity_rate=1, gravity=0.01, size=1.5, fade_rate=0.05, swade=False):
        self.limit = limit
        self.spawn_rate = spawn_rate
        self.velocity_rate = velocity_rate
        self.gravity = gravity
        self.size = size
        self.fade_rate = fade_rate
        self.swade = swade

        self.random_limit = False
        self.random_spawn = False
        self.random_velocity = False
        self.random_gravity = False
        self.random_size = False
        self.random_fade = False
        self.random_swade = False

    def randomize_properties(self):
        if self.random_limit: self.limit = random.uniform(1, 10)
        if self.random_spawn: self.spawn_rate = random.uniform(0, 500)
        if self.random_velocity: self.velocity_rate = random.uniform(0.1, 2)
        if self.random_gravity: self.gravity = random.uniform(0, 0.01)
        if self.random_size: self.size = random.uniform(1, 4)
        if self.random_fade: self.fade_rate = random.uniform(0, 0.1)
        if self.random_swade: self.swade = random.choice([True, False])


'''
SparkManager Class responsible for cerating, holding, and deleting multiple sparks at a time
'''
class SparkManager:
    def __init__(self):
        self.properties = SparkProperties()
        self.sparks = []
        self.spark_ticks = self.properties.spawn_rate # Time between each spark creation
        self.gen_sparks = True

    def create_spark(self, x, y, velocity_x, velocity_y, color):
        self.properties.randomize_properties() # Will randomize any properties that have their random value as true
        self.sparks.append(Spark(
            x, y, velocity_x, velocity_y,
            self.properties.size, self.properties.fade_rate,
            self.properties.velocity_rate, self.properties.gravity,
            color, self.properties.swade
        ))

    def update_sparks(self, delta_time, screen_w, screen_h):
        if self.gen_sparks:
            for spark in self.sparks:
                spark.update(delta_time, screen_w, screen_h)
                if not spark.is_active():
                    self.sparks.remove(spark)

    def render_sparks(self, screen):
        if self.gen_sparks:
            for spark in self.sparks:
                spark.render(screen)
    
    # Update spark property based on option selected
    def change_spark_property(self, option, value):
        
        if "LIMIT" in option:
            if value == 0: self.properties.random_limit = True
            else: 
                self.properties.limit = max(0, self.properties.limit + value)
                self.properties.random_limit = False

        elif "SPAWN" in option:
            if value == 0: self.properties.random_spawn = True
            else: 
                self.properties.spawn_rate = max(0, self.properties.spawn_rate + value)
                self.properties.random_spawn = False

        elif "VELOCITY" in option:
            if value == 0: self.properties.random_velocity = True
            else: 
                self.properties.velocity_rate = max(0, self.properties.velocity_rate + value)
                self.properties.random_velocity = False

        elif "GRAVITY" in option:
            if value == 0: self.properties.random_gravity = True
            else: 
                self.properties.gravity = max(0, self.properties.gravity + value)
                self.properties.random_gravity = False

        elif "SIZE" in option:
            if value == 0:self.properties.random_size = True
            else: 
                self.properties.size = max(1, self.properties.size + value)
                self.properties.random_size = False

        elif "FADE" in option: 
            if value == 0: self.properties.random_fade = True
            else: 
                self.properties.fade_rate = max(0, self.properties.fade_rate + value)
                self.properties.random_fade = False

        elif "SWADE" in option: 
            if value: self.properties.random_swade = True
            else: 
                if self.properties.random_swade:
                    self.properties.swade = False
                else:
                    self.properties.swade = not self.properties.swade
                self.properties.random_swade = False
        elif "RESET" in option:
            self.properties.__init__()
            self.sparks = []
            
        elif "SPARK" in option:
            self.gen_sparks = not self.gen_sparks 