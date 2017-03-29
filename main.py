import pygame
from pygame.locals import *
import sys
import os
from Constants import *
from Objects import *
from Character_sprites import Player


def main():
    pygame.init()
    print pygame.version.ver
    screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF)
    clock = pygame.time.Clock()
    pygame.display.set_caption('Scrolling background demo')
    pygame.time.set_timer(genericTimerEvent, 60)

    # You can customize the background by replacing the background.png file. The image should be larger than the window.
    background_image = pygame.image.load(os.path.join('images', 'background.jpg')).convert_alpha()
    background = SimpleSprite((0, 0), background_image)

    charset = pygame.image.load(os.path.join('images', 'charset.png')).convert_alpha()
    charsetRect = charset.get_rect()

    running = True

    #Game surface, here is where we will be bliting all our resources
    gameSurface = pygame.Surface(background.rect.size)

    #Creating the camera. We need to make sure it does not go out-of-bounds.
    camera = pygame.Rect(0, 0, min(window_width, gameSurface.get_width()), min(window_height, gameSurface.get_height()))

    #We give the camera some leeway so that the player can move around a little bit before it starts moving
    cameraLeeway = pygame.Rect(0, 0, camera.width / 8, camera.height / 8)

    #Create the player character
    playerRect = pygame.Rect(0, 0, drawSize, drawSize * 3 / 5)
    playerSurface = charset.subsurface(pygame.Rect(0, charsetRect.bottom - (charsetRect.height / 8 * 4), charset.get_width() / 18 * 3, charsetRect.height / 8 * 4))
    character_sprite_size = (charset.get_width() / 18, charset.get_height() / 8, drawSize)
    player = Player(playerRect, playerSurface, character_sprite_size)
    player.set_position((window_width / 2, window_height / 2))

    cameraLeeway.center = player.rect.center #Cameraleeway is set properly to the player

    while running:
        # Update
        player.update_position(clock.get_time())

        #Updating the camera:
        #What we want to happen is for the camera to follow the player while giving some leeway and never going out-of-bounds.
        #We move the leeway rect according to where the player is
        if player.rect.left <= cameraLeeway.left and player.vx < 0:
            cameraLeeway.left = player.rect.left
        elif player.rect.right >= cameraLeeway.right and player.vx > 0:
            cameraLeeway.right = player.rect.right
        if player.rect.top <= cameraLeeway.top and player.vy < 0:
            cameraLeeway.top = player.rect.top
        if player.rect.bottom >= cameraLeeway.bottom and player.vy > 0:
            cameraLeeway.bottom = player.rect.bottom

        camera.center = cameraLeeway.center  # The camera follows the camera leeway rect

        if camera.x < 0:   # Make sure camera does not leave the game area
            camera.x = 0
        elif camera.right > gameSurface.get_width():
            camera.right = gameSurface.get_width()
        if camera.y < 0:
            camera.y = 0
        elif camera.bottom > gameSurface.get_height():
            camera.bottom = gameSurface.get_height()

        # Render

        #We blit everything to the game surface
        gameSurface.blit(background.image, (0, 0))
        gameSurface.blit(player.image, player.rect)

        #Also draw the camera rects to the gamesurface to visualize camera
        pygame.draw.rect(gameSurface, GREEN, cameraLeeway, 4)
        pygame.draw.rect(gameSurface, ORANGE, camera, 5)


        #Then we blit the part of the game surface that is within the camera to the screen
        screen.blit(gameSurface, (0 - camera.left, 0 - camera.top)) #Make sure to take the negative of the camera

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
                    player.walking_phase += 0.5
                    player.update_sprite()


        pygame.display.update()
        clock.tick(1000)
    pygame.quit()



if __name__ == '__main__':
    main()