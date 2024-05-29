import pygame
import visuals

'''
Button Super Class
 Args:
        screen: screen to draw/render on
        x, y: cooridinates on screen
        width, height: size of button
        text: text of button
        toggled: whether or not the button is clicked
        value: the value that will be sent to the vizualizer class to change a property
'''
class Button:
    def __init__(self, screen, x, y, width, height, text, toggled = False, value = 0):
        self. x, self.y = x, y
        self.width, self.height = width, height
        self.screen = screen
        self.text = text
        self.toggled = toggled
        self.clicked = False
        self.value = value

        self.font = pygame.font.Font(size = 16)

    # Draw the button and check for mouse click
    def update(self):
        self.render()
        self.check_clicked()
    
    def render(self):
        
        self.button_text = self.font.render(self.text, True, 'Black')

        pygame.draw.rect(self.screen, 'darkgrey', (self.x, self.y, self.width, self.height))

        # Darken when clicked for responsiveness
        if self.clicked:
            pygame.draw.rect(self.screen, 'grey', (self.x + 1, self.y + 1, self.width -3, self.height-3))
        else:
            pygame.draw.rect(self.screen, 'white', (self.x + 1, self.y + 1, self.width -3, self.height-3))

        self.screen.blit(self.button_text, (self.x + 1, self.y + (self.height * 0.2)))

    # Makes sure to count only single click, not every milisecond during the click
    def check_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        button_pos = pygame.rect.Rect((self.x,self.y), (self.width, self.height))
     
        # If not clicked before, and the mouse is clicking on it:
        if not self.clicked and pygame.mouse.get_pressed()[0] and button_pos.collidepoint(mouse_pos):
            self.clicked = True

        # If is clicked and the mouse is no longer clicking:
        if self.clicked and not pygame.mouse.get_pressed()[0]:
            self.clicked = False
            self. toggled = not self.toggled

'''
Contains the main buttons that contain sub-buttons
'''
class ButtonMenu():
    def __init__(self, screen, visualizer, x=0, y=0, width=140, height=18):
        self.screen = screen
        self.x, self.y , = x, y
        self.width, self.height, = width, height
        self.font = pygame.font.Font(size = 18)
        self.visualizer = visualizer
        self.main_buttons = [] # Holds main buttons which themselves contain sub-buttons
        self.main_buttons.append(TypeButton(self.screen, self.x, self.height*4, self.width, self.height, "VISUAL TYPE", self.visualizer))
        self.main_buttons.append(BarButton(self.screen, self.x, self.height*5.5, self.width, self.height, "BAR PROPERTIES", self.visualizer))
        self.main_buttons.append(CircleButton(self.screen, self.x, self.height*7, self.width, self.height, "CIRCLE PROPERTIES", self.visualizer))
        self.main_buttons.append(SparkButton(self.screen, self.x, self.height*8.5, self.width, self.height, "SPARK PROPERTIES", self.visualizer))
        self.main_buttons.append(ColorButton(self.screen, self.x, self.height*10, self.width, self.height, "COLOR PROPERTIES", self.visualizer))
        self.main_buttons.append(SpecialButton(self.screen, self.x, self.height*11.5, self.width, self.height, "SPECIAL PROPERTIES", self.visualizer))
        self.main_buttons.append(PresetsButton(self.screen, self.x, self.height*13, self.width, self.height, "PRESETS", self.visualizer))
    
    def update(self):
        self.render()

        # If one of the main buttons is toggled, only update that one button
        if any(button.toggled for button in self.main_buttons):
            for button in self.main_buttons:
                if button.toggled:
                    button.update()

        # Update all buttons
        else:
            for button in self.main_buttons:
                button.update()

    # Display info for key bindings
    def render(self):
        text = self.font.render("TAB = HIDE MENU", True, 'White')
        pygame.draw.rect(self.screen, 'Black', (0, 0, text.get_width() + 4, self.height))
        self.screen.blit(text, (1, 1))

        text = self.font.render("ARROW KEYS = FAST FORWARD / REWIND", True, 'White')
        pygame.draw.rect(self.screen, 'Black', (0, self.height, text.get_width() + 4, self.height))
        self.screen.blit(text, (1, self.height*1.15))

        text = self.font.render("SHIFT + ARROW KEYS = CHANGE SONG", True, 'White')
        pygame.draw.rect(self.screen, 'Black', (0, self.height*2, text.get_width() + 4, self.height))
        self.screen.blit(text, (1, self.height*2.15))

        text = self.font.render("SPACE = PAUSE", True, 'White')
        pygame.draw.rect(self.screen, 'Black', (0, self.height*3, text.get_width() + 4, self.height))
        self.screen.blit(text, (1, self.height*3.15))

# Main button for changing visual type
class TypeButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.visual_type = visuals.VisualType
        self.buttons = []
        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "BOTTOM", value=self.visual_type.BOTTOM))
        self.buttons.append(Button (screen, x, y + (height * 3), width, height, "TOP", value=self.visual_type.TOP))
        self.buttons.append(Button (screen, x, y + (height * 4.5), width, height, "MIDDLE", value=self.visual_type.MIDDLE))
        self.buttons.append(Button (screen, x, y + (height * 6), width, height, "CIRCLE", value=self.visual_type.CIRCLE))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "INNER CIRLCE", value=self.visual_type.CIRCLE_INNER))
        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "MIDDLE CIRLCE", value=self.visual_type.CIRCLE_MIDDLE))
        self.buttons.append(Button (screen, x, y + (height * 10.5), width, height, "CIRCLE WAVE", value=self.visual_type.CIRCLE_WAVE))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    self.visualizer.change_visual_type(button.value)
                    button.toggled = False
                button.update()
        else:
            self.text = self.primary_text

# Main button for changing bar properties
class BarButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "BAR WIDTH +", value=1))
        self.buttons.append(Button (screen, x, y + (height * 2.5), width, height, "BAR WIDTH -", value=-1))

        self.buttons.append(Button (screen, x, y + (height * 4), width, height, "MAX HEIGHT +", value=5))
        self.buttons.append(Button (screen, x, y + (height * 5), width, height, "MAX HEIGHT -", value=-5))

        self.buttons.append(Button (screen, x, y + (height * 6.5), width, height, "MIN HEIGHT +", value=1))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "MIN HEIGHT -", value=-1))

        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "GROW SPEED +", value=-0.01))
        self.buttons.append(Button (screen, x, y + (height * 10), width, height, "GROW SPEED -", value=0.01))

        self.buttons.append(Button (screen, x, y + (height * 11.5), width, height, "SHRINK SPEED +", value=-0.01))
        self.buttons.append(Button (screen, x, y + (height * 12.5), width, height, "SHRINK SPEED -", value=0.01))

        self.buttons.append(Button (screen, x, y + (height * 14), width, height, "RESET BARS", value=True))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            # Get info from first bar to display
            bar_info = self.visualizer.bars[0]
            info_text = (f"width: {round(bar_info.width, 1)}, max height: {bar_info.max_height}, " 
                f"min height: {bar_info.min_height}, grow speed: {round(bar_info.grow_speed, 3)}, "
                f"shrink speed: {round(bar_info.shrink_speed, 3)}")
            text = self.font.render(info_text, True, 'White')
            pygame.draw.rect(self.screen, 'Black', (self.x, self.y - self.height, text.get_width() + 4, self.height))
            self.screen.blit(text, (self.x, self.y - self.height))
        
            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    button.toggled = False
                    self.visualizer.change_property(button.text, button.value)
                button.update()
        else:
            self.text = self.primary_text

# Main button for changing spark properties
class SparkButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "SPARK ON / OFF"))

        self.buttons.append(Button (screen, x, y + (height * 3), width, height, "LIMIT +", value=1))
        self.buttons.append(Button (screen, x, y + (height * 4), width, height, "RANDOM LIMIT", value=0))
        self.buttons.append(Button (screen, x, y + (height * 5), width, height, "LIMIT -", value=-1))

        self.buttons.append(Button (screen, x, y + (height * 6.5), width, height, "SPAWN RATE +", value=-50))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "RANDOM SPAWN", value=0))
        self.buttons.append(Button (screen, x, y + (height * 8.5), width, height, "SPAWN RATE -", value=50))

        self.buttons.append(Button (screen, x, y + (height * 10), width, height, "SIZE +", value=1))
        self.buttons.append(Button (screen, x, y + (height * 11), width, height, "RANDOM SIZE", value=0))
        self.buttons.append(Button (screen, x, y + (height * 12), width, height, "SIZE -", value=-1))

        self.buttons.append(Button (screen, x, y + (height * 13.5), width, height, "FADE +", value=0.005))
        self.buttons.append(Button (screen, x, y + (height * 14.5), width, height, "RANDOM FADE", value=0))
        self.buttons.append(Button (screen, x, y + (height * 15.5), width, height, "FADE -", value=-0.005))

        self.buttons.append(Button (screen, x, y + (height * 17), width, height, "GRAVITY +", value=0.001))
        self.buttons.append(Button (screen, x, y + (height * 18), width, height, "RADNOM GRAVITY", value=0))
        self.buttons.append(Button (screen, x, y + (height * 19), width, height, "GRAVITY -", value=-0.001))

        self.buttons.append(Button (screen, x, y + (height * 20.5), width, height, "VELOCITY +", value=0.1))
        self.buttons.append(Button (screen, x, y + (height * 21.5), width, height, "RANDOM VELOCITY", value=0))
        self.buttons.append(Button (screen, x, y + (height * 22.5), width, height, "VELOCITY -", value=-0.1))

        self.buttons.append(Button (screen, x, y + (height * 24), width, height, "SWADE ON / OFF", value=False))
        self.buttons.append(Button (screen, x, y + (height * 25), width, height, "RANDOM SWADE", value=True))

        self.buttons.append(Button (screen, x, y + (height * 26.5), width, height, "HEIGHT THRESHOLD +", value=0.05))
        self.buttons.append(Button (screen, x, y + (height * 27.5), width, height, "HEIGHT THRESHOLD -", value=-0.05))

        self.buttons.append(Button (screen, x, y + (height * 29), width, height, "RESET SPARKS", value=True))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            # Get info from first bar to display
            bar_info = self.visualizer.bars[0]
            info_text = (f"limit: {round(bar_info.spark_manager.properties.limit)}, spawn: {round(bar_info.spark_manager.properties.spawn_rate)}ms, " 
                f"size: {round(bar_info.spark_manager.properties.size, 3)}, fade: {round(bar_info.spark_manager.properties.fade_rate, 7)}, gravity: "
                f"{round(bar_info.spark_manager.properties.gravity, 4)}, velocity: {round(bar_info.spark_manager.properties.velocity_rate, 3)}, "
                f"height threshold: {round(bar_info.spark_manager.properties.threshold, 2)}")
            text = self.font.render(info_text, True, 'White')
            pygame.draw.rect(self.screen, 'Black', (self.x, self.y - self.height, text.get_width() + 4, self.height))
            self.screen.blit(text, (self.x, self.y - self.height))

            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    button.toggled = False
                    self.visualizer.change_spark_property(button.text, button.value)
        
                button.update()
        else:
            self.text = self.primary_text

# Main button for changing circle properties
class CircleButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "RADIUS +", value=5))
        self.buttons.append(Button (screen, x, y + (height * 2.5), width, height, "RADIUS -", value=-5))

        self.buttons.append(Button (screen, x, y + (height * 4), width, height, "RING RADIUS +", value=5))
        self.buttons.append(Button (screen, x, y + (height * 5), width, height, "RING RADIUS -", value=-5))

        self.buttons.append(Button (screen, x, y + (height * 6.5), width, height, "RING WIDTH +", value=-0.02))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "RING WIDTH -", value=0.02))

        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "RESET CIRCLE", value=True))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            # Get info from first bar to display
            bar_info = self.visualizer.bars[0]
            info_text = (f"radius: {bar_info.radius}, ring radius: {bar_info.ring_radius}, ring size: {round(bar_info.ring_size, 3)}")
            text = self.font.render(info_text, True, 'White')
            pygame.draw.rect(self.screen, 'Black', (self.x, self.y - self.height, text.get_width() + 4, self.height))
            self.screen.blit(text, (self.x, self.y - self.height))

            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    button.toggled = False
                    self.visualizer.change_property(button.text, button.value) 
                button.update()
        else:
            self.text = self.primary_text

class PresetsButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "DEFAULT"))
        self.buttons.append(Button (screen, x, y + (height * 3), width, height, "BLACK HOLE"))
        self.buttons.append(Button (screen, x, y + (height * 4.5), width, height, "SPACE"))
        self.buttons.append(Button (screen, x, y + (height * 6), width, height, "LIGHT SHOW"))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "FIRE"))
        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "RAIN"))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
        
            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    button.toggled = False
                    self.visualizer.change_preset(button.text)
                button.update()
        else:
            self.text = self.primary_text

# Special properties that reqire bars to share information are handled in visualizer class
class SpecialButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "ROTATION SPEED +", value=-1))
        self.buttons.append(Button (screen, x, y + (height * 2.5), width, height, "ROTATION ON/OFF", value=0))
        self.buttons.append(Button (screen, x, y + (height * 3.5), width, height, "ROTATION SPEED -", value=1))

        self.buttons.append(Button (screen, x, y + (height * 5), width, height, "SMOOTHING +", value=-0.1))
        self.buttons.append(Button (screen, x, y + (height * 6), width, height, "SMOOTHING ON/OFF", value=0))
        self.buttons.append(Button (screen, x, y + (height * 7), width, height, "SMOOTHING -", value=0.1))

        self.buttons.append(Button (screen, x, y + (height * 8.5), width, height, "RESET", value=1))

    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            # Get info to display
            info_text = (f"rotation speed: {self.visualizer.get_rotate_speed()}, smoothing factor: {round(self.visualizer.get_smoothing_factor(), 3)}")
            text = self.font.render(info_text, True, 'White')
            pygame.draw.rect(self.screen, 'Black', (self.x, self.y - self.height, text.get_width() + 4, self.height))
            self.screen.blit(text, (self.x, self.y - self.height))
        
            self.text = self.secondary_text

            # Scan the sub-buttons to see if they were clicked and send the value to visualizer
            for button in self.buttons:
                if button.toggled:
                    button.toggled = False
                    self.visualizer.change_special_property(button.text, button.value)
                button.update()
        else:
            self.text = self.primary_text

# Main button for changing color properties
class ColorButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text
        self.secondary_text = "BACK"
        self.visualizer = visualizer
        self.buttons = []

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "CHANGE COLOR"))

        self.buttons.append(Button (screen, x, y + (height * 3), width, height, "COLOR CYCLE SPEED +", value=0.1))
        self.buttons.append(Button (screen, x, y + (height * 4), width, height, "COLOR CYCLE ON/OFF", value=True))
        self.buttons.append(Button (screen, x, y + (height * 5), width, height, "COLOR CYCLE SPEED -", value=-0.1))

        self.buttons.append(Button (screen, x, y + (height * 6.5), width, height, "GLOW INTENSITY +", value=0.05))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "GLOW ON/OFF", value=True))
        self.buttons.append(Button (screen, x, y + (height * 8.5), width, height, "GLOW INTENSITY -", value=-0.05))

        self.buttons.append(Button (screen, x, y + (height * 10), width, height, "GLOW LENGTH +", value=0.05))
        self.buttons.append(Button (screen, x, y + (height * 11), width, height, "GLOW LENGTH -", value=-0.05))

        self.buttons.append(Button (screen, x, y + (height * 12.5), width, height, "RESET COLORS"))

        self.r_slider = Slider(screen, x+10, y + height * 14, width, 20, 0, 255, 255, lambda v: (v, 0, 0))
        self.g_slider = Slider(screen, x+10, y + height * 15, width, 20, 0, 255, 255, lambda v: (0, v, 0))
        self.b_slider = Slider(screen, x+10, y + height * 16, width, 20, 0, 255, 255, lambda v: (0, 0, v))

    def update(self):
        self.render()
        self.check_clicked()

        if self.toggled:
            bar_info = self.visualizer.get_bar_info()
            info_text = (f"RGB: {int(self.r_slider.value), int(self.g_slider.value), int(self.b_slider.value)}, "
                f"color cycle speed: {round(self.visualizer.get_color_speed(), 3)}, "
                f"glow: {bar_info.glow_enabled}, glow intensity: {round(bar_info.glow_intensity, 3)}, glow length: "
                f"{round(bar_info.glow_length, 3)}")

            text = self.font.render(info_text, True, 'White')
            pygame.draw.rect(self.screen, 'Black', (self.x, self.y - self.height, text.get_width() + 4, self.height))
            self.screen.blit(text, (self.x, self.y - self.height))

            self.text = self.secondary_text

            for button in self.buttons:
                button.update()
                if button.toggled:
                    if button.text == "CHANGE COLOR":
                            self.r_slider.update()
                            self.g_slider.update()
                            self.b_slider.update()
                            self.visualizer.change_color_property(button.text, (self.r_slider.value, self.g_slider.value, self.b_slider.value))
                    else:
                        button.toggled = False
                        self.visualizer.change_color_property(button.text, button.value)         
        else:
            self.text = self.primary_text

class Slider:
    def __init__(self, screen, x, y, width, height, min_val, max_val, initial_val, color_func):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_x = self.x + (self.width * (self.value - self.min_val) / (self.max_val - self.min_val))
        self.color_func = color_func

        self.font = pygame.font.Font(None, 24)
        self.dragging = False

    def handle_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # If mouse is pressed on the handle
        if mouse_pressed and not self.dragging:
            if pygame.Rect(self.handle_x, self.y, 10, self.height).collidepoint(mouse_pos):
                self.dragging = True

        if not mouse_pressed:
            self.dragging = False

        # Make sure handle is within bounds and get the value
        if self.dragging:
            self.handle_x = max(self.x, min(mouse_pos[0], self.x + self.width))
            self.value = self.min_val + (self.handle_x - self.x) * (self.max_val - self.min_val) / self.width

    def update(self):
        self.handle_drag()
        self.render()

    def render(self):
        # Gradient background
        for i in range(self.width):
            color = self.color_func(self.min_val + (self.max_val - self.min_val) * (i / self.width))
            pygame.draw.line(self.screen, color, (self.x + i, self.y), (self.x + i, self.y + self.height))
        
        # Handle
        pygame.draw.rect(self.screen, 'white', (self.handle_x, self.y, 10, self.height))