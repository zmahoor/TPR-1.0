import pygame

class PYGAMEWRAPPER:

    def __init__(self,width=800,height=240):

        pygame.init()

        size = width,height

        self.screen = pygame.display.set_mode(size)

        self.myfont = pygame.font.Font("RobotoCondensed-Regular.ttf",26)

    def Get_Color(self, color='black'):

        if color=='black': return (0, 0, 0)
        if color=='green': return (0, 128, 0)
        if color=='red': return (255, 0, 0)
        if color=='blue': return (0, 0, 255)
        if color=='yellow': return (255, 255, 0)
        if color=='orange': return (255, 165, 0)
        if color=='purple': return (255, 0, 255)
        if color=='cyan': return (0, 255, 255)
        if color=='brown': return (102, 51, 0)

    def Draw_Text(self, textString , x = 10 , y = 10, color ='black' ):
        
        label = self.myfont.render(textString, 1, self.Get_Color(color))

        textrect = label.get_rect()

        textrect.left = self.screen.get_rect().left + x

        textrect.top = self.screen.get_rect().top + y

        self.screen.blit(label, textrect)

    def Refresh(self):

        pygame.display.flip()

    def Wipe(self):

        backgroundColor = 255, 255, 255

        self.screen.fill(backgroundColor)
    
