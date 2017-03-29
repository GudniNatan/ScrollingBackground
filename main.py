import pygame
from pygame.locals import *
import sys
import os
from Constants import *
from Objects import *
from Character_sprites import Player
from Methods import *


def main():
    pygame.init()
    screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Scrolling background demo')
    pygame.time.set_timer(genericTimerEvent, 120)

    # You can customize the background by replacing the background.png file. The image should be larger than the window.
    background_image = pygame.image.load(os.path.join('images', 'background.png')).convert_alpha()
    background = SimpleSprite((0, 0), background_image)

    charset = pygame.image.load(os.path.join('images', 'charset_small.png')).convert_alpha()

    running = True

    # Game surface, here is where we will be blit-ing the game environment
    gameSurface = pygame.Surface(background_image.get_size())

    # Creating the camera. We need to make sure it does not go out-of-bounds.
    camera = pygame.Rect(0, 0, min(window_width, gameSurface.get_width()), min(window_height, gameSurface.get_height()))

    # We give the camera some leeway so that the player can move around a little bit before it starts moving
    cameraLeeway = pygame.Rect(0, 0, camera.width / 8, camera.height / 7)

    # Create the player character
    playerRect = pygame.Rect(0, 0, drawSize, drawSize * 3 / 5)
    character_sprite_size = (charset.get_width() / 3, charset.get_height() / 4, drawSize)
    player = Player(playerRect, charset, character_sprite_size)
    player.set_position((window_width / 2, window_height / 2))

    cameraLeeway.center = player.rect.center  # Cameraleeway is set to center on the player

    while running:
        # Update
        player.update_position(clock.get_time())

        # Updating the camera:
        # What we want to happen is for the camera to follow the player while giving some leeway and never going out-of-bounds.
        # We move the leeway rect according to where the player is
        if not cameraLeeway.contains(player.rect):
            if player.rect.left <= cameraLeeway.left:
                cameraLeeway.left = player.rect.left
            elif player.rect.right >= cameraLeeway.right:
                cameraLeeway.right = player.rect.right
            if player.rect.top <= cameraLeeway.top:
                cameraLeeway.top = player.rect.top
            elif player.rect.bottom >= cameraLeeway.bottom:
                cameraLeeway.bottom = player.rect.bottom

        camera.center = cameraLeeway.center  # The camera follows the camera leeway rect

        camera.clamp_ip(gameSurface.get_rect())  # Make sure camera does not leave the game area

        # Render

        # We blit everything to the game surface
        gameSurface.blit(background.image.subsurface(camera), camera)  # We only need to blit what will be inside the camera
        gameSurface.blit(player.image, player.rect)

        # Also draw some rectangles to the gameSurface to visualize the camera
        pygame.draw.rect(gameSurface, GREEN, cameraLeeway, 4)
        pygame.draw.rect(gameSurface, ORANGE, camera, 6)

        # Then we blit the part of the game surface that is within the camera to the screen
        screen.blit(gameSurface.subsurface(camera), (0, 0))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                running = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                player.update_speed()
            if event.type == genericTimerEvent:
                if player.moving:
                    player.walking_phase += 1
                    player.update_sprite()

        pygame.display.update()
        clock.tick(1000)  # It is good game design to try to limit the fps as little as possible.
    pygame.quit()


if __name__ == '__main__':
    main()
