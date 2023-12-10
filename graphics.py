import os
import pygame as pg
from fastfont import Fastfont

# Some colours in RGB values
black = (0,0,0)
white= (255,255,255)
blue = (91,155,213) #RGB value from display panel image

pg.init()

# Clock function
def clock():
    '''
    Uses pygame ticks to get time units.
    Because physics use time, not ticks.
    '''
    time = pg.time.get_ticks()*0.001
    return time

#Class
class Arrowimg():
    '''
    Most of the arrow graphics. This class handles the image and the "Rect".
    Needs the imglist so it can quickly update to correct angle.
    '''
    def __init__(self,posx,posy,imglist):
        self.imglist = imglist
        fname = os.path.join('bitmaps','arrow.png')
        img_source = pg.image.load(fname).convert_alpha()
        self.img = img_source.copy()
        rectarrow = pg.Rect(posx,posy,10,10)
        img_rect = img_source.get_rect(center=rectarrow.center)
        self.rect = self.img.get_rect(center=img_rect.center)

    def update(self, theta):
        '''
        Takes in any float theta and
        Loads the nearest integer angle,
        as imglist contains 360 images.
        '''
        angle = int(theta+.5)%360
        self.img = self.imglist[angle]
        self.rect = self.img.get_rect(center=self.rect.center)


class GUI():
    '''
    Graphical User Interface class,
    set up, clear update and draw screen.
    '''
    def __init__(self,caption,xmax,ymax):

        # Initialize pygame
        pg.init()

        # Set up screen
        self.xmax = xmax
        self.ymax = ymax
        self.screen = pg.display.set_mode((xmax,ymax))
        pg.display.set_caption(caption)
        pg.display.set_icon(pg.image.load("icon.gif"))

        # Load rotated images into imagelist for all angle 0-359 deg
        self.imglist = []
        print("Loading rotated arrow images",end="")

        # Load original arrow image, for if rotation is necessary
        fname = os.path.join('bitmaps','arrow.png')
        img_source = pg.image.load(fname).convert_alpha()

        
        # Loading all rotated images, if not exist, rotate and save
        for i in range(360):

            # Show progress bar with points
            if i%30==0:
                print(".",end="")

            # Load from (or save in) sprites folder
            spritename = os.path.join('sprites', 'arrow' + str(i) + '.png') 

            if os.path.exists(spritename):
                img = pg.image.load(spritename).convert_alpha()
            else:
                img = pg.transform.rotate(img_source, i).convert_alpha()
                pg.image.save(img, spritename)

            # Add to rotated arrow img to imglist
            self.imglist.append(img)
                
        print()

        # Display panel bitmap
        self.panelimg = pg.image.load(os.path.join('bitmaps','displays-h130.png'))
        self.panelrect = self.panelimg.get_rect()

        # Light button images, same size, so we can use same rect object)
        self.imgb0on  = pg.transform.scale(pg.image.load(os.path.join('bitmaps','B0on.png')),(50,40))
        self.imgb0off = pg.transform.scale(pg.image.load(os.path.join('bitmaps','B0off.png')),(50,40))
        self.imgb1on  = pg.transform.scale(pg.image.load(os.path.join('bitmaps','B1on.png')),(50,40))
        self.imgb1off = pg.transform.scale(pg.image.load(os.path.join('bitmaps','B1off.png')),(50,40))
        self.imgreset = pg.transform.scale(pg.image.load(os.path.join('bitmaps', 'RESET.png')), (50, 40))
        self.imgbrect = self.imgb0on.get_rect()

        # Button positions
        self.B0xy = self.xmax-50,26
        self.B1xy = self.xmax-50,76
        self.RESETxy = self.xmax-50,126

        # Calculate where panel starts
        self.panelx0  = int(self.xmax/2)-int(self.panelrect.width/2)+100
        self.panely0  = 20

        # Create font objects
        self.font = Fastfont(self.screen,'Arial',17,white,True,False)
        self.dispfont = Fastfont(self.screen,'Arial',25,white,True,0,0) # 0,0 = center this font in x and y
        #       (pygame screen, font,size,   colour RGB,bold,italic)



    def textpanel(self,b0mag,b1mag,b1freq,b0on,b1on):
        '''
        Displays the text panel listing the key controls on the left,
        the B0/B1 on/off buttons and the RESET button on the right.
        (NOT the increase/decrease buttons for B0/B1 magnitude and B1 freq)
        '''

        # Blit background image for display panel, center of screen
        self.panelrect.centerx = int(self.xmax / 2) + 100
        self.panelrect.y = self.panely0
        self.screen.blit(self.panelimg, self.panelrect)

        # Text

        # Render text at x,y-position
        xtxt = 6
        y = 5
        dy = 15

        self.font.printat(self.screen,xtxt,y,"===  KEY CONTROLS  ===")
        y += dy
        self.font.printat(self.screen,xtxt,y,"B0 = Left/Right keys")
        y += dy
        self.font.printat(self.screen,xtxt,y,"B1 = Down/Up keys ")
        y += dy
        self.font.printat(self.screen,xtxt,y,"B1freq = Minus/Plus keys")
        y += dy
        self.font.printat(self.screen,xtxt,y,"Quit = ESC key")
        y += dy
        #self.font.printat(screen,xtxt,y,"Reset vel: v")

        # Positon of values in displays

        # Use display panel x-coordinate to set text x-coordinate
        yb0 = self.panely0 + 26
        xb0 = self.panelx0 + 99
        xb1  = self.panelx0 + 307
        xb1f = self.panelx0 + 521
        self.dispfont.printat(self.screen, xb0, yb0, str(round(b0mag, 3)))
        self.dispfont.printat(self.screen, xb1, yb0, str(round(b1mag, 3)))
        self.dispfont.printat(self.screen, xb1f, yb0, str(round(b1freq, 3)) + " Hz")

        # Button for B0 on/off
        self.imgbrect.center = self.B0xy
        if b0on:
            self.screen.blit(self.imgb0on,self.imgbrect)
        else:
            self.screen.blit(self.imgb0off,self.imgbrect)

        # Button for B1 on/off
        self.imgbrect.center = self.B1xy
        if b1on:
            self.screen.blit(self.imgb1on,self.imgbrect)
        else:
            self.screen.blit(self.imgb1off,self.imgbrect)

        # RESET button
        self.imgbrect.center = self.RESETxy
        self.screen.blit(self.imgreset, self.imgbrect)

    def drawarrows(self,arrowlist,m,n):
        '''
        Goes through the nested list (to represent the two dimensions) with
        Arrowimg objects and displays each one at the correct position and angle.
        '''
        for i in range(m):
            for j in range(n):
                # Slicing looks weird because it's a nested list
                # To put the image on the screen, we blit the image and Rect
                self.screen.blit(arrowlist[i][j].img, arrowlist[i][j].rect)

    def clearscreen(self):
        '''
        Pygame doesn't get rid of the previous frame by itself, so a
        function is needed to clear the screen unless. Done here by simply
        drawing a black rectangle over everything.
        '''
        self.screen.fill(black)
        rect = self.screen.get_rect()


        # Draw a border
        dx = 4
        pg.draw.rect(self.screen,blue,rect,dx)


    def updatescreen(self):
        '''
        Display all the prepared elements of a frame.
        '''
        pg.display.flip()

    def getkeys(self):
        '''
        Regulates every functionality that has an optional key control.
        Buttons for increasing or decreasing B0/B1 magnitude and B1 frequency
        are also part of this, since they require the same limits on how much
        they should change between frames when held down.
        '''
        # Use keynames to report which keys have been pressed
        # This dictionary translates key code in key names
        keynames = { pg.K_RIGHT:'RIGHT',
                     pg.K_LEFT:'LEFT',
                     pg.K_UP:'UP',
                     pg.K_DOWN:'DOWN',
                     pg.K_EQUALS:'PLUS',
                     pg.K_MINUS:'MINUS',
                     pg.K_v: 'V',
                     pg.K_b: 'B',
                     pg.K_ESCAPE:'ESC',
                     pg.K_HOME: 'RESET',
                     }

        # Keys list to return
        activekeys = []

        # Check events
        for event in pg.event.get():
            # Quit event (closing window) is same ESCAPE key
            if event.type==pg.QUIT:
                activekeys.append(keynames[pg.K_ESCAPE])

            # Mouse clicked on buttons
            elif event.type == pg.MOUSEBUTTONUP:
                mousex,mousey = event.pos
                butnr = event.button
                # Check on buttons B0 and B1, size 50,40 with x,y-distance to center of button
                if abs(mousex-self.B0xy[0])<25 and abs(mousey-self.B0xy[1])<20:
                    activekeys.append("B0")
                elif abs(mousex-self.B1xy[0])<25 and abs(mousey-self.B1xy[1])<20:
                    activekeys.append("B1")
                elif abs(mousex - self.RESETxy[0]) < 25 and abs(mousey - self.RESETxy[1]) < 20:
                    activekeys.append("RESET")

        # Check mouse buttons status and position for buttons
        # Translate to corresponding keyname
        buttons = ["LEFT","RIGHT","DOWN","UP","MINUS","PLUS"]
        leftmousebutton = pg.mouse.get_pressed()[0]
        if leftmousebutton:
            # Mouse positions in panel coordinates
            xmouse = pg.mouse.get_pos()[0] - self.panelx0
            ymouse = pg.mouse.get_pos()[1] - self.panely0

            # Positions of 6 buttons: size
            ybuttons = 74
            dybuttons = 50
            xbuttons = list(range(5,5+5*106+1,106)) # start coordinates of + and - buttons
            dxbuttons = 80


            if ybuttons < ymouse < ybuttons+dybuttons:
                for i in range(6):
                    if xbuttons[i]<= xmouse <=xbuttons[i]+dxbuttons:
                        activekeys.append(buttons[i])

        # Check keys
        pg.event.pump()
        keyboard = pg.key.get_pressed()
        for code in keynames.keys():
            if keyboard[code]:
                activekeys.append(keynames[code])

        return activekeys


    def __del__(self):
        pg.display.quit()
        pg.quit()

