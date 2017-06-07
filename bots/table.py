import pygame
from pygameWrapper import PYGAMEWRAPPER

class TABLE:

    def __init__(self, window, width, height):

        #define screen to draw on
        self.screen = window.screen

        #get screen dimensions
        self.w = width
        self.h = height

        #set window
        self.window = window

    def Update(self, new, bottom):
        
        #get size of newList that populates table (if not empty or None)
        try:
            size = len(new)
        except TypeError as e:
            size = 0

        #define BLACK as RGB
        BLACK = 0,0,0

        #set window 
        window = self.window

        #set screen
        screen = self.screen

        #draw lines that define the table
        
        
        pygame.draw.line(screen, BLACK, (0, self.h/12.0), (self.w, self.h/12.0), 3)
        
        for i in range (2, 12):

            #add ranks for 1-10
            if i%2 == 0:
                col = 'LIGHTBLUE'
            else:
                col = 'TAN'
            window.Draw_Rect(0, (i-.9)*self.h/13.0, self.w, (i+.1)*self.h/13.0, color = col)
            window.Draw_Text(str(i-1), x = 5, y = ((i-.5)*self.h/13.0))
        
        pygame.draw.line(screen, BLACK, (0, (11*self.h/13.0)), (self.w, (11*self.h/13.0)), 2)

        pygame.draw.line(screen, BLACK, (0, (12*self.h/13.0)), (self.w, (12*self.h/13.0)), 2)


        
        for i in range(0,size):

            #name is the command name or username, depending on input
            name = new[i][0]

            #score is the learnability or user score
            score = new[i][1]

            #capitalize name if exists to enhance readability
            if name != None:
                
                name = name.upper()

            #draw name and score to the table
            if score != None and name != None:
                window.Draw_Text(name, x = self.w*.13, y = ((i+1.5)*self.h/13.0))
                window.Draw_Text(str(int(score)), x = self.w*.635, y = ((i+1.5)*self.h/13.0))

        #get name of recent for bottom row
        bt = bottom[0]

        #capitalize the name if exists
        if bt != None:
            
            bt = bt.upper()

        #draw the name and score to the screen in the bottom row 
        window.Draw_Text(bt, x = self.w*.13, y = 11.5*self.h/13.0)  
        window.Draw_Text(str(int(bottom[1])), x = self.w*.635, y = 11.5*self.h/13.0) 
