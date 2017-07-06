import pygame

class PYGAMEWRAPPER:
                
    def __init__(self,width=800,height=240, fontSize=17):

        #initialize pygame modules
        pygame.init()

        #set size
        size = width,height
        
        self.size = width, height

        #set screen
        self.screen = pygame.display.set_mode(size)

        #define font to be used
        self.myfont = pygame.font.Font("RobotoCondensed-Regular.ttf", fontSize)

    def Draw_Text(self, textString , x = 10 , y = 10, color = 'BLACK' ):

        #get color
        col = self.Get_Color(color)

        #set area for text to be drawn on
        label = self.myfont.render(textString, 1, col)

        #get where the text is
        self.textrect = label.get_rect()

        self.textrect.left = self.screen.get_rect().left + x

        self.textrect.top = self.screen.get_rect().top + y

        self.text_width = self.textrect[2]
        self.text_x = self.textrect[0]
        #draw text
        self.screen.blit(label, self.textrect)

    def Refresh(self):

        #refresh screen
        pygame.display.flip()

    def Wipe(self):

        #set background
        backgroundColor = 255, 255, 255

        self.screen.fill(backgroundColor)
    
    def Draw_Line(self, x1, y1, x2, y2, color = 'BLACK', thickness = 1):

        #get color
        col = self.Get_Color(color)

        #draw line
        line = pygame.draw.line(self.screen, col, (x1,y1), (x2,y2), thickness)

    def Draw_Rect(self, x1, y1, w, h, color = 'RED'):

        #get color
        col = self.Get_Color(color)

        #set rectangle dimensions
        rect = (x1, y1, w, h)

        #draw rect
        shape = pygame.draw.rect(self.screen, col, rect, 0)

    def Get_Color(self, color):

        #define RGB values for common colors
        colors = {'BLACK'       : (  0,   0,   0),
                  'WHITE'       : (255, 255, 255),
                  'RED'         : (255,   0,   0),
                  'GREEN'       : (  0, 255,   0),
                  'BLUE'        : (  0,   0, 255),
                  'GRAY'        : (123, 123, 123),
                  'LIGHTGRAY'   : (150, 150, 150),
                  'DARKGRAY'    : ( 75,  75,  75),
                  'PINK'        : (255,  10, 190),
                  'LIGHTBLUE'   : (173, 216, 230),
                  'LIGHTGREEN'  : (100, 255,   0),
                  'DARKGREEN'   : ( 11, 128,  11),
                  'VIOLET'      : ( 70,   0, 130),
                  'GOLD'        : (255, 192,   0),
                  'ORANGE'      : (255, 165,   0),
                  'PURPLE'      : (255, 0  , 255),
                  'CYAN'        : (0, 255  , 255),
                  'BROWN'       : (102, 51 ,   0),
                  'YELLOW'      : (255, 255,   0),
                  'TAN'         : (241, 232, 220)}

        #get color
        if color in colors:
                return colors.get(color)
        #return BLACK if name is not found
        else:
                return colors.get('BLACK')
        

    def Quit(self):

        #quits out of pygame and window
        pygame.quit()

        exit()
                

                
