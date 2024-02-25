import pygame as pg

class Button():
    def __init__(self, x, y, image, state=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.state = state

    
    def draw(self, WINDOW):
        action = False

        # Get mouse position
        position = pg.mouse.get_pos()
        
        # Check mouseover and clicked
        if self.rect.collidepoint(position):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        #Check clicker released
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked == False

        # Draw the button
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))

        return action