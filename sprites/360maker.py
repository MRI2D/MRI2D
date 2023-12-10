import pygame

"""
360 rotating images maker
"""


#setup screen
surface = pygame.display.set_mode( (512,512) )


img_source = pygame.image.load('arrow.png')
img = img_source.copy()



for i in range(360):
    img = pygame.transform.rotate(img_source, i).convert_alpha()
    pygame.image.save(img, "arrow"+str(i)+".png")


pygame.quit()
