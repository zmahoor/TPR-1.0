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
        
        #get size of newList that populates table (if not empty or None)
        try:
            size = len(new)
        except TypeError as e:
            size = 0

        #define BLACK in RGB
        BLACK = 0,0,0

        #set window 
        window = self.WINDOW

        #set screen
        screen = self.SCREEN
	
	
	
        #draw lines that define the table
        
        
        pygame.draw.line(screen, BLACK, (0, self.HEIGHT/12.0), (self.WIDTH, self.HEIGHT/12.0), 3)
        
        top_rect = self.HEIGHT/12.0
        height_rect = ((11.0/12.0) * self.HEIGHT) / (self.USERS+2)
        
        for i in range (0, self.USERS):

            #add ranks for 1-10
            if i%2 == 0:
                col = 'LIGHTBLUE'
            else:
                col = 'TAN'
            window.Draw_Rect(0, top_rect, self.WIDTH, height_rect, color = col)
            window.Draw_Text(str(i+1), x = 4, y = top_rect + (.4*height_rect))
            
            #name is the command name or username, depending on input
            name = new[i][0]

            #score is the learnability or user score
            score = new[i][1]

            #capitalize name if exists to enhance readability
            if name != None:
                
                name = name.upper()

            #draw name and score to the table
            if score != None and name != None:
                window.Draw_Text(name, x = self.WIDTH*.15, y = top_rect + (.4*height_rect))
                window.Draw_Text(str(int(score)), x = self.WIDTH*.7, y = top_rect + (.4*height_rect))
            
            
            
            top_rect = top_rect + height_rect
        
        pygame.draw.line(screen, BLACK, (0, (11*self.HEIGHT/(self.USERS+3))), (self.WIDTH, (11*self.HEIGHT/(self.USERS+3))), 2)

        pygame.draw.line(screen, BLACK, (0, (12*self.HEIGHT/(self.USERS+3))), (self.WIDTH, (12*self.HEIGHT/(self.USERS+3))), 2)


        
        

            

        #get name of recent for bottom row
        bt = bottom[0]

        #capitalize the name if exists
        if bt != None:
            
            bt = bt.upper()

        #draw the name and score to the screen in the bottom row 
        window.Draw_Text(bt, x = self.WIDTH*.13, y = 11.5*self.HEIGHT/13.0)  
        window.Draw_Text(str(int(bottom[1])), x = self.WIDTH*.635, y = 11.5*self.HEIGHT/13.0) 
