from pygame import USEREVENT

WHITE = (242, 242, 242)
BLACK = (25, 25, 25)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 102, 255)
ORANGE = (255, 153, 0)

drawSize = 35
halfDrawSize = drawSize / 2
window_size = window_width, window_height = 1280, 720   # Would like to make window size dynamic

#Custom Events
genericEvent = USEREVENT+1
delayedGenericEvent = USEREVENT+2
genericTimerEvent = USEREVENT+3