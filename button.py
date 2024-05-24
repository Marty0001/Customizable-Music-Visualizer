import pygame
from visualizer import Visualizer, VisualType

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
        self.buttons = []
        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "BOTTOM", value=VisualType.BOTTOM))
        self.buttons.append(Button (screen, x, y + (height * 3), width, height, "TOP", value=VisualType.TOP))
        self.buttons.append(Button (screen, x, y + (height * 4.5), width, height, "MIDDLE", value=VisualType.MIDDLE))
        self.buttons.append(Button (screen, x, y + (height * 6), width, height, "CIRCLE", value=VisualType.CIRCLE))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "INNER CIRLCE", value=VisualType.CIRCLE_INNER))
        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "MIDDLE CIRLCE", value=VisualType.CIRCLE_MIDDLE))

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

        self.buttons.append(Button (screen, x, y + (height * 1.5), width, height, "WIDTH +", value=1))
        self.buttons.append(Button (screen, x, y + (height * 2.5), width, height, "WIDTH -", value=-1))

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
            show_info = self.visualizer.bars[0]
            info_text = (f"width: {round(show_info.width, 1)}, max height: {show_info.max_height}, " 
                f"min height: {show_info.min_height}, grow speed: {round(show_info.grow_speed, 3)}, "
                f"shrink speed: {round(show_info.shrink_speed, 3)}")
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
            show_info = self.visualizer.bars[0]
            info_text = (f"limit: {round(show_info.spark_manager.properties.limit)}, spawn: {round(show_info.spark_manager.properties.spawn_rate)}ms, " 
                f"size: {round(show_info.spark_manager.properties.size, 3)}, fade: {round(show_info.spark_manager.properties.fade_rate, 7)}, gravity: "
                f"{round(show_info.spark_manager.properties.gravity, 4)}, velocity: {round(show_info.spark_manager.properties.velocity_rate, 3)}, "
                f"height threshold: {round(show_info.spark_manager.properties.threshold, 2)}")
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

        self.buttons.append(Button (screen, x, y + (height * 6.5), width, height, "RING SIZE +", value=-0.02))
        self.buttons.append(Button (screen, x, y + (height * 7.5), width, height, "RING SIZE -", value=0.02))

        self.buttons.append(Button (screen, x, y + (height * 9), width, height, "RESET CIRCLE", value=True))

    
    def update(self):
        self.render()
        self.check_clicked()

        # If toggled, render sub-buttons and change text to 'BACK'
        if self.toggled:
            # Get info from first bar to display
            show_info = self.visualizer.bars[0]
            info_text = (f"radius: {show_info.radius}, ring radius: {show_info.ring_radius}, ring size: {round(show_info.ring_size, 3)}")
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

# Main button for changing color properties
class ColorButton(Button):
    def __init__(self, screen, x, y, width, height, text, visualizer, visible=False):
        super().__init__(screen, x, y, width, height, text, visible)
        self.primary_text = text

    def update(self):
        self.render()
        self.check_clicked()

        if self.toggled:
            self.text = "BACK"
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
            info_text = (f"rotation speed: {self.visualizer.rotate_speed}, smoothing factor: {round(self.visualizer.smoothing_factor, 3)}")
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