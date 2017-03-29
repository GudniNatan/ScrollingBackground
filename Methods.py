import pygame


def aspect_scale(image, (bx, by)):
    scale_rect = pygame.Rect(0, 0, bx, by)
    image_rect = image.get_rect()
    return pygame.transform.scale(image, image_rect.fit(scale_rect).size)


def reverse_clamp(smaller_rect, larger_rect):
    if not larger_rect.contains(smaller_rect):
        new_rect = larger_rect.copy()
        if smaller_rect.left <= larger_rect.left:
            new_rect.left = smaller_rect.left
        elif smaller_rect.right >= larger_rect.right:
            new_rect.right = smaller_rect.right
        if smaller_rect.top <= larger_rect.top:
            new_rect.top = smaller_rect.top
        elif smaller_rect.bottom >= larger_rect.bottom:
            new_rect.bottom = smaller_rect.bottom
        return new_rect


def reverse_clamp_ip(smaller_rect, larger_rect):
    if not larger_rect.contains(smaller_rect):
        if smaller_rect.left <= larger_rect.left:
            larger_rect.left = smaller_rect.left
        elif smaller_rect.right >= larger_rect.right:
            larger_rect.right = smaller_rect.right
        if smaller_rect.top <= larger_rect.top:
            larger_rect.top = smaller_rect.top
        elif smaller_rect.bottom >= larger_rect.bottom:
            larger_rect.bottom = smaller_rect.bottom