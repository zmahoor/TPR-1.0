import pygame
from pygameWrapper import PYGAMEWRAPPER

class TABLE:

    def __init__(self, window, width, height):

        #define screen to draw on
        self.SCREEN = window.screen

        #get screen dimensions
        self.WIDTH = width
        self.HEIGHT = height

        #set window
        self.WINDOW = window
        
        self.USERS = 5

    def Update(self, new, bottom):
        
        FONT_SIZE = 23
        #get size of newList that populates table (if not empty or None)
        try:
            size = len(new)
        except TypeError as e:
            size = 0

        #define BLACK in RGB
        BLACK = 0,0,0

        #set window 
        window = self.WINDOW
        screen = self.SCREEN
	
        #draw lines that define the table        
        pygame.draw.line(screen, BLACK, (0, 40+0.5*self.HEIGHT/12.0), (self.WIDTH, 40+0.5*self.HEIGHT/12.0), 3)
        
        top_rect = 40+0.5*self.HEIGHT/12.0
        height_rect = ((11.0/12.0) * self.HEIGHT) / (self.USERS+2)
        
        display = []

        for i in range (0, min(self.USERS, size)):

            #add ranks for 1-10
            if i%2 == 0:
                col = 'LIGHTBLUE'
            else:
                col = 'TAN'
            window.Draw_Rect(0, top_rect, self.WIDTH, height_rect, color = col)
            window.Draw_Text(str(i+1), x = 4, y = top_rect + (.3*height_rect),fontSize=FONT_SIZE)
            
            #name is the command name or username, depending on input
            name = new[i][0]

            #score is the learnability or user score
            score = new[i][1]

            #capitalize name if exists to enhance readability
            if name != None:
                
                # name = name.upper()
                display.append(name)
            #draw name and score to the table
            if score != None and name != None:

                if len(name) > 23 : name = name[0:23]

                window.Draw_Text(name, x = self.WIDTH*.15, y = top_rect + (.3*height_rect), fontSize=FONT_SIZE)
                window.Draw_Text(str(int(score)), x = self.WIDTH*.7, y = top_rect + (.3*height_rect), fontSize=FONT_SIZE)
                        
            top_rect = top_rect + height_rect
        
        pygame.draw.line(screen, BLACK, (0, (11*self.HEIGHT/(self.USERS+3))), (self.WIDTH, (11*self.HEIGHT/(self.USERS+3))), 2)
        pygame.draw.line(screen, BLACK, (0, (12*self.HEIGHT/(self.USERS+3))), (self.WIDTH, (12*self.HEIGHT/(self.USERS+3))), 2)

        #get name of recent for bottom row
        # print ('bottom' , bottom)

        
        if bottom != None:
            
            name   = bottom['cmd'] if bottom.has_key('cmd') else bottom['userName']
            score  = bottom['score']
            rank   = bottom['rank']
            
            #capitalize the name if exists
            if name not in display:
                if len(name) > 23: 
                    name = name[0:23]

                #draw the name and score to the screen in the bottom row 
                window.Draw_Text(str(rank), x = 4, y = top_rect + (.25*height_rect), fontSize=FONT_SIZE)
                window.Draw_Text(name, x = self.WIDTH*.15, y = top_rect + (.25*height_rect), fontSize=FONT_SIZE)  
                window.Draw_Text(str(int(score)), x = self.WIDTH*.7, y = top_rect + (.25*height_rect), fontSize=FONT_SIZE)

