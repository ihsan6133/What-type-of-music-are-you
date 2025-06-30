import pygame 

def draw(screen, rect, progress, bg, fg):
    pygame.draw.rect(screen, bg, rect)
    pygame.draw.rect(screen, fg, (rect.x, rect.y, rect.width * progress, rect.height))
