#! /usr/bin/env_python
import pygame, sys, os
import main, imgLoaders 
pygame.init()

win = pygame.display.set_mode((600,600))

pygame.display.set_caption("Game Win")


White = (255,255,255)
clock = pygame.time.Clock()
print(os.path.join(os.path.split(__file__)[0], 'level1.ldtk'))
map1 = main.Ldtk(os.path.join(os.path.split(__file__)[0], 'level1.ldtk'), scaler=2).levels[0]
map1Image = map1.autoPgTileRender()
map2 = main.Ldtk(os.path.join(os.path.split(__file__)[0], 'level1.ldtk'), scaler=1, imageLoader=imgLoaders.pilLoader).levels[0]
map2Image = map2.autoPilTileRender()
map2Image.save("cool.png")

while True:
    pygame.display.update()

    win.fill(White)
    win.blit(map1Image,(10,10))

    clock.tick(16) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 