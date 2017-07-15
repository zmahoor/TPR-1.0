from pygameWrapper import PYGAMEWRAPPER
import pygame
#-------Constants-------#
WIDTH 		= 920
HEIGHT 		= 250
FONT_SIZE	= 20

WINDOW 		= PYGAMEWRAPPER(width = WIDTH, height = HEIGHT, fontSize = FONT_SIZE)




while 1:

        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                        
			WINDOW.Quit()
                        
        WINDOW.Wipe()


        print WINDOW.myfont.render('M', 1, (0,0,0)).get_rect()
	WINDOW.Refresh()

