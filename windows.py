from button import SpriteButton, ChoiceButton
import color
import pygame
import questions
from utils import scale_cover
from questions import QUESTIONS
import random
import progressbar

def compute_image_size_cover(w, h, img_w, img_h):
    img_aspect = img_w / img_h
    screen_aspect = w / h
    if img_aspect > screen_aspect:
        new_width = int(h * img_aspect)
        return (new_width, h, (int(w / 2 - new_width / 2), 0))
    else:
        new_height = int(w / img_aspect)
        return (w, new_height, (0, int(h / 2 - new_height / 2)))


def divide_rect_into_quarters(rect, gap=0, padding=0):
    """
    Divides a rectangle into four equal parts and returns their rectangles.
    """
    w, h = rect.width, rect.height
    gap = gap / 2

    rw = w // 2 - (padding + gap)
    rh = h // 2 - (padding + gap)

    return [
        pygame.Rect(rect.x + padding, rect.y + padding, rw, rh),  # Top-left
        pygame.Rect(rect.x + w // 2 + gap, rect.y + padding, rw, rh),  # Top-right
        pygame.Rect(rect.x + padding, rect.y + h // 2 + gap, rw, rh),  # Bottom-left
        pygame.Rect(rect.x + w // 2 + gap, rect.y + h // 2 + gap, rw, rh)   # Bottom-right
    ]


class TitleWindow:
    def __init__(self, width, height ):
        
        font = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0)  # Default font and size

        (text, text_rect) = font.render("What type of music are you?", color.BLACK, None)  # White text
        text_rect = text.get_rect()  # Center the text

        text_rect.center = (width // 2, height // 5)  # Center the text on the screen
        self.text = text
        self.text_rect = text_rect

        (self.subtitle, _) = font.render("Personality Quiz!", color.BLACK, None)  # White subtitle

        self.subtitle = pygame.transform.scale(self.subtitle, (self.subtitle.get_width() * 0.7, self.subtitle.get_height() * 0.7))  # Scale the subtitle to half its size
        self.subtitle_rect = self.subtitle.get_rect()  # Get the rect of the subtitle
        self.subtitle_rect.center = (width // 2, height // 3.3)  #
        
        img = pygame.image.load("sprites/PlayBtn.png").convert_alpha()  # Load the icon image
        img = pygame.transform.scale(img, (img.get_width() // 3.5, img.get_height() // 3.5))  # Scale the image to half its size

        img_clicked = pygame.image.load("sprites/PlayClick.png").convert_alpha()  # Load the clicked image
        img_clicked = pygame.transform.scale(img_clicked, (img_clicked.get_width() // 3.5, img_clicked.get_height() // 3.5))  # Scale the clicked image
        
        img_aligned = pygame.surface.Surface((img.get_width(), img.get_height()), pygame.SRCALPHA)  # Create a new surface with the same size as the image
        img_aligned.blit(img_clicked, (0, (img.get_height() - img_clicked.get_height())))  # Align the image to the bottom of the surface

        start_btn_rect = pygame.Rect(0, 0, img.get_width(), img.get_height())  # Create a rectangle for the button
        start_btn_rect.center = (width // 2, height // 2)  # Center the button on the screen
        self.start_btn = SpriteButton(start_btn_rect, img, img_aligned)  # Create a button with the image


        sound = pygame.mixer.Sound("sounds/buttons/Wood Block1.ogg")  # Load the sound
        sound.set_volume(0.3)        
        self.start_cb = None
        def on_button():
            pygame.mixer.Channel(0).play(sound)

        def start():
            
            if self.start_cb:
                self.start_cb()

        self.start_btn.on_press(on_button)  # Play the intro sound on channel 0
        self.start_btn.on_release(start)

        self.bg_img_og = pygame.image.load("sprites/bg.png").convert()

        (w, h, self.bg_pos) = compute_image_size_cover(width, height, self.bg_img_og.get_width(), self.bg_img_og.get_height())
        self.bg_img = pygame.transform.smoothscale(self.bg_img_og, (w, h))  # Scale the background image to fit the screen
    
        # self.front_btn = SpriteButton(pygame.image.load("sprites/FrontBtn.png").convert_alpha(), pygame.image.load("sprites/FrontClick.png").convert_alpha(), pos=(width // 2 - img.get_width() // 2, height // 2 - img.get_height() // 2 + 100))  # Create a front button

    def show(self, screen):
        screen.fill(color.WHITE)  # Fill the screen with primary color
        screen.blit(self.bg_img, self.bg_pos)  # Draw the background image
        screen.blit(self.text, self.text_rect)  # Draw the text
        screen.blit(self.subtitle, self.subtitle_rect)  # Draw the subtitle
        self.start_btn.draw(screen)

    def on_start(self, cb):
        self.start_cb = cb

    def resize(self, w, h):
        self.text_rect.center = (w // 2, h // 5)
        self.subtitle_rect.center = (w // 2, h // 3.3)
        
        self.start_btn.set_pos((w // 2 - self.start_btn.image.get_width() // 2, h // 2 - self.start_btn.image.get_height() // 2))
        (new_w, new_h, self.bg_pos) = compute_image_size_cover(w, h, self.bg_img.get_width(), self.bg_img.get_height())
        self.bg_img = pygame.transform.smoothscale(self.bg_img_og, (new_w, new_h))

    def register_mouse_events(self, mouse):
        return self.start_btn.register_mouse_events(mouse)

class QuizWindow:
    def __init__(self, width, height, question, q_index):

        (self.question, self.choices) = question  # Unpack the question and choices

        self.q_index = q_index  # Store the question index
        self.width = width
        self.height = height
        self.selected_choice = None  # Initialize the selected choice to None
        font = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0)  # Default font and size

        (text, text_rect) = font.render(self.question, color.BLACK, None)  # White text
        text_rect = text.get_rect()  # Center the text

        text_rect.center = (width // 2, height // 7)  # Center the text on the screen
        self.text = text
        self.text_rect = text_rect
        self.choice_rects = divide_rect_into_quarters(pygame.Rect(0, height * 0.2, width, height * 0.75), 10, 10)  # Divide the screen into four equal parts for choices
        
        self.choice_buttons = [
            ChoiceButton(choice, self.choice_rects[i], f"sprites/choices/{q_index+1}{'abcd'[i]}.jpg") for i, choice in enumerate(self.choices)  # Create choice buttons for each choice
        ]

        self.randomized_indices = [0, 1, 2, 3]
        random.seed(q_index)
        random.shuffle(self.randomized_indices)
        for i, button in enumerate(self.choice_buttons):
            button.set_rect(self.choice_rects[self.randomized_indices[i]])


            # Here you can add logic to handle the choice click, like moving to the next question or processing the answer
        def on_choice_click(btn):
            btn.select()  # Mark the button as selected

            self.selected_choice = btn.text
            for other_button in self.choice_buttons:
                if other_button != btn:
                    other_button.deselect()
            self.front_btn.set_disabled(False)  # Enable the front button when a choice is selected

        for button in self.choice_buttons:
            button.on_click(lambda btn=button: on_choice_click(btn))  # Register the click event for each button

        # Front Button
        front_btn_rect = pygame.Rect(0, 0, 50, 50)
        front_btn_rect.center = (width * 0.95, 0.1 * height)  # Position the front button at the bottom left

        self.front_btn = SpriteButton(front_btn_rect,  pygame.image.load("sprites/FrontBtn.png").convert_alpha() , pygame.image.load("sprites/FrontClick.png").convert_alpha(),  pygame.image.load("sprites/FrontHover.png").convert_alpha(), pygame.Surface(front_btn_rect.size, pygame.SRCALPHA))  # Create a front button
        self.front_btn.set_disabled(True)  # Initially disable the front button

        # Back button
        back_btn_rect = pygame.Rect(0, 0, 50, 50)
        back_btn_rect.center = (width * 0.05, 0.1 * height)  # Position the back button at the bottom right

        self.back_btn = SpriteButton(back_btn_rect,  pygame.image.load("sprites/BackBtn.png").convert_alpha() , pygame.image.load("sprites/BackClick.png").convert_alpha(),  pygame.image.load("sprites/BackHover.png").convert_alpha(), pygame.Surface(back_btn_rect.size, pygame.SRCALPHA))  # Create a back button
        if self.q_index == 0:  # Disable the back button if
            self.back_btn.set_disabled(True)


    def on_next(self, cb):
        self.front_btn.on_release(cb)
        
    def on_prev(self, cb):
        self.back_btn.on_release(cb)

    def show(self, screen):

        screen.fill(color.WHITE)  # Fill the screen with primary color
        screen.blit(self.text, self.text_rect)

        for button in self.choice_buttons:
            button.draw(screen)

        # progress bar
        pb_rect = pygame.Rect(0, 0, self.width * 0.2, 5)
        pb_rect.centerx = self.width // 2
        pb_rect.centery = self.height * 0.965
        progressbar.draw(screen, pb_rect, (self.q_index) / len(QUESTIONS), color.PRIMARY_DARK, color.PRIMARY)

        # front and back buttons
        self.front_btn.draw(screen)
        self.back_btn.draw(screen)

    def register_mouse_events(self, mouse):
        for button in self.choice_buttons:
            if button.register_mouse_events(mouse):
                return True

        if self.front_btn.register_mouse_events(mouse):
            return True
        
        if self.back_btn.register_mouse_events(mouse):
            return True
        
        return False

    def resize(self, w, h):
        
        self.width = w
        self.height = h
        (text, self.text_rect) = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0).render(self.question, color.BLACK, None)
        
        self.text_rect.center = (w // 2, h // 7)
        self.text = text

        self.choice_rects = divide_rect_into_quarters(pygame.Rect(0, h * 0.2, w, h * 0.75), 10, 10)
        for i, button in enumerate(self.choice_buttons):
            button.set_rect(self.choice_rects[self.randomized_indices[i]])

        front_btn_rect = pygame.Rect(0, 0, 50, 50)
        front_btn_rect.center = (w * 0.95, 0.1 * h)  # Position the front button at the bottom left
        self.front_btn.set_rect(front_btn_rect)

        back_btn_rect = pygame.Rect(0, 0, 50, 50)
        back_btn_rect.center = (w * 0.05, 0.1 * h)
        self.back_btn.set_rect(back_btn_rect)


class ResultWindow:

    def __init__ (self, width, height, result):
        self.width = width
        self.height = height
        self.has_shown = False
        self.has_revealed = False  # Flag to check if the result has been revealed
        self.time_since_start = None
        self.music = pygame.mixer.Sound(questions.music_sample(result[0]))  # Load the result music
        self.music.set_volume(0.5)  # Set the volume of the music
        # if jazz set louder
        if result[0] == "Jazz":
            self.music.set_volume(0.7)

        (self.result, self.description) = result  # Unpack the result and description

        font = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0)  # Default font and size
        (text, text_rect) = font.render(f"You are...", color.WHITE, None)
        text_rect = text.get_rect()  # Center the text
        text_rect.center = (width // 2, height * 0.45)
        self.text = text        
        self.text_rect = text_rect

        self.bg_og = pygame.image.load(f"sprites/results/{self.result}.jpg").convert()
        self.bg_img = scale_cover(pygame.Rect(0, 0, self.width, self.height), self.bg_og)  # Scale the background image to fit the screen

        self.drumroll = pygame.mixer.Sound("sounds/drumroll.mp3")
        self.drumroll.set_volume(0.5)

        restart = pygame.image.load("sprites/RestartBtn.png").convert_alpha()

        restart_rect = pygame.Rect(0, 0, restart.get_width(), restart.get_height())  # Get the rectangle of the restart button
        restart_rect.center = (width // 2, height * 0.55)  # Position the restart button at the bottom center
        restart_rect = restart_rect.scale_by(2)  # Set the size of the restart button
        # Restart Button
        self.restart_btn = SpriteButton(
            restart_rect,
            restart,
            pygame.image.load("sprites/RestartClick.png").convert_alpha(),
            pygame.image.load("sprites/RestartHover.png").convert_alpha(),
            None
        )
        self.restart_btn.set_disabled(True)
        

    def show(self, screen):
        if not self.has_shown:
            pygame.mixer.music.stop()
            pygame.mixer.Channel(0).play(self.drumroll)
            self.has_shown = True
            self.time_since_start = pygame.time.get_ticks()
        
        screen.fill(color.BLACK)
        
        elapsed_time = pygame.time.get_ticks() - self.time_since_start
        if elapsed_time > 2300:
            if not self.has_revealed:
                (text, self.text_rect) = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0).render(f"You are {self.result} music!", color.WHITE, None)
                self.text_rect.center = (self.width // 2, self.height * 0.45)
                self.text = text
                self.has_revealed = True

            n = 1000 # milliseconds
            self.bg_img.set_alpha((elapsed_time - 3200) / n * 255) 
            screen.blit(self.bg_img, (0, 0))
        
        if elapsed_time > 3200:
            if not pygame.mixer.Channel(1).get_busy():
                pygame.mixer.Channel(1).play(self.music, 0, 0, 100)

        if elapsed_time > 5500:
            if self.restart_btn.button.disabled:
                self.restart_btn.set_disabled(False)
            self.restart_btn.draw(screen)
        

        
        screen.blit(self.text, self.text_rect)

    def on_restart(self, cb):
        self.restart_btn.on_release(cb)

    def resize(self, w, h):
        self.width = w
        self.height = h
        (text, self.text_rect) = pygame.freetype.Font("fonts/RetroGaming.ttf", 27, 0, 0).render(f"You are {self.result} music!", color.WHITE, None)
        self.text_rect.center = (w // 2, h * 0.45)
        self.text = text

        self.bg_img = scale_cover(pygame.Rect(0, 0, w, h), self.bg_og)

        restart_rect = pygame.Rect(0, 0, self.restart_btn.img_og.get_width(), self.restart_btn.img_og.get_height())
        restart_rect.center = (w // 2, h * 0.55)
        restart_rect = restart_rect.scale_by(2)  # Set the size of the restart button
        self.restart_btn.set_rect(restart_rect)

    def register_mouse_events(self, mouse):
        return self.restart_btn.register_mouse_events(mouse)