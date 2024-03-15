import pygame
pygame.font.init()
print(pygame.font.Font(None,20).render('a',True,"#FFFFFF").get_width())