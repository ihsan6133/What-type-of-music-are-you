import pygame
import color
import random
from utils import scale_contain, scale_cover

class Button: #
    def __init__(self, rect):
        self.rect = rect
        self.is_hovered = False
        self.is_clicked = False
        self.first_click = False
        self.press_cb = None  # Callback function to be called on click
        self.release_cb = None  # Callback function to be called on release
        self.disabled = False

    def register_mouse_events(self, mouse):

        if self.disabled:
            return False

        is_collide = self.rect.collidepoint(mouse.get_pos())
        if is_collide:
            self.is_hovered = True
        else:
            self.is_hovered = False
        if is_collide or self.is_clicked:
            self.is_hovered = True
            if mouse.get_pressed()[0]:
                if not self.is_clicked:
                    self.is_clicked = True
                    if not self.first_click and self.press_cb:
                        self.press_cb()
                    self.first_click = True
            else:
                if self.is_clicked:
                    self.is_clicked = False
                    if self.release_cb:
                        self.release_cb()
                self.first_click = False

        return is_collide
    
    def on_click(self, cb):
        self.release_cb = cb

    def on_press(self, cb):
        self.press_cb = cb

    def is_pressed(self):
        return self.is_clicked
    
    def set_disabled(self, disabled):
        self.disabled = disabled
        if disabled:
            self.is_clicked = False
            self.is_hovered = False
            self.first_click = False
 
class SpriteButton:

    click_sound = None

    def __init__(self, rect, img, img_click = None, img_hover = None, img_disabled = None):
        if SpriteButton.click_sound is None:
            SpriteButton.click_sound = pygame.mixer.Sound("sounds/buttons/Wood Block1.ogg")
            SpriteButton.click_sound.set_volume(0.3)

        self.img_og = img
        self.img_click_og = img_click
        self.img_hover_og = img_hover
        self.img_disabled_og = img_disabled

        self.image = scale_contain(rect, img, False)
        self.image_clicked = scale_contain(rect, img_click, False) if img_click else None
        self.image_hover = scale_contain(rect, img_hover, False) if img_hover else None
        self.image_disabled = scale_contain(rect, img_disabled, False) if img_disabled else None
        self.rect = rect
        self.button = Button(self.rect)
        self.press_cb = None
    
        def press(bt):
            if SpriteButton.click_sound:
                SpriteButton.click_sound.play()
            if bt.press_cb:
                bt.press_cb()

        self.button.on_press(lambda: press(self))

    def set_disabled(self, disabled):
        self.button.set_disabled(disabled)

    def draw(self, surface):
        if self.button.disabled and self.image_disabled:
            surface.blit(self.image_disabled, self.rect.topleft)
        elif self.button.is_pressed() and self.image_clicked:
            surface.blit(self.image_clicked, self.rect.topleft)
        elif self.button.is_hovered and self.image_hover:
            surface.blit(self.image_hover, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def set_pos(self, pos):
        self.rect.topleft = pos

    def set_rect(self, rect):
        self.rect = rect
        self.image = scale_contain(self.rect, self.img_og, False)
        if self.image_clicked:
            self.image_clicked = scale_contain(self.rect, self.img_click_og, False)
        if self.image_hover:
            self.image_hover = scale_contain(self.rect, self.img_hover_og, False)
        if self.image_disabled:
            self.image_disabled = scale_contain(self.rect, self.img_disabled_og, False)
        self.button.rect = self.rect

    def on_press(self, cb):
        self.press_cb = cb
        

    def on_release(self, cb):
        self.button.on_click(cb)

    def register_mouse_events(self, mouse):
        return self.button.register_mouse_events(mouse)

class ChoiceButton:
    def __init__(self, text, rect, img_path):
        self.text = text
        self.rect = rect
        try:
            self.original_image = pygame.image.load(img_path).convert_alpha()
        except:
            self.original_image = pygame.Surface((rect.width, rect.height))
            self.original_image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))  # Fallback to a red square if image loading fails
        self.image = scale_cover(self.rect, self.original_image)
        self.button = Button(self.rect)
        self.is_selected = False
        self.font = pygame.font.Font("fonts/RetroGaming.ttf", 17)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        text_surface = self.font.render(self.text, True, (255, 255, 255), color.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        text_rect.bottom = self.rect.bottom -2.5  # Adjust text position to be above the bottom edge

        pygame.draw.rect(surface, color.BLACK, pygame.Rect(self.rect.x, self.rect.bottom - text_rect.height - 5, self.rect.width, text_rect.height + 5))
        surface.blit(text_surface, text_rect)
        if self.is_selected:
            # draw translucent rectangle
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 100))  # Semi-transparent
            surface.blit(overlay, self.rect.topleft)

        elif self.button.is_clicked:
            pygame.draw.rect(surface, color.PRIMARY, self.rect, 4)
        
    def set_rect(self, rect):
        self.rect = rect
        self.image = scale_cover(self.rect, self.original_image)
        self.button.rect = self.rect

    def register_mouse_events(self, mouse):
        return self.button.register_mouse_events(mouse) and not self.is_selected 
    
    def on_click(self, cb):
        self.button.on_click(cb)

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False


