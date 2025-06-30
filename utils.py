import pygame

def scale(surface, size, smooth=True):
    if smooth:
        return pygame.transform.smoothscale(surface, size)
    else:
        return pygame.transform.scale(surface, size)


def scale_cover(rect, img, smooth=True):
    img_aspect = img.get_width() / img.get_height()
    screen_aspect = rect.width / rect.height
    if img_aspect > screen_aspect:
        w = int(rect.height * img_aspect)
        # return (w, rect.height, )
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.blit(scale(img, (w, rect.height), smooth), (int(rect.width / 2 - w / 2), 0))
        return s
 
    else:
        h = int(rect.width / img_aspect)
        # return (rect.width, h, (0, int(rect.height / 2 - h / 2)))
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.blit(scale(img, (rect.width, h), smooth), (0, int(rect.height / 2 - h / 2)))
        return s
    
def scale_contain(rect, img, smooth=True):
    img_aspect = img.get_width() / img.get_height()
    screen_aspect = rect.width / rect.height

    if img_aspect > screen_aspect:
        # Image is wider relative to rect -> scale by width
        w = rect.width
        h = int(rect.width / img_aspect)
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.blit(scale(img, (w, h), smooth), (0, int(rect.height / 2 - h / 2)))
        return s
    else:
        # Image is taller relative to rect -> scale by height
        h = rect.height
        w = int(rect.height * img_aspect)
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        s.blit(scale(img, (w, h), smooth), (int(rect.width / 2 - w / 2), 0))
        return s
