import json
import pygame
import os, sys

def get_data(file):
    with open(file, "r") as data:
        return json.loads(data.read())

## This is object holds all the data for a .ldtk file
class Ldtk:
    def __init__(self, ldtkfile): ## It takes in the file path
        self.ldtkData = get_data(ldtkfile) ## Loads the JSON
        self.header = self.ldtkData['__header__'] ## Sets the header info to something more convenient

        for k, v in self.ldtkData.items(): ## Here what it does is load all the floating information into the object as attributes  
            if not isinstance(v, dict) or not isinstance(v, list): ## but it ignores all the lists and dictionary to handle them seperately
                self.__dict__[k] = v
            else:
                print(v)
        
        self.levels = []

        for l in self.ldtkData['levels']:
            self.levels.append(Ldtklevel(l))

class Ldtklevel:
    def __init__(self, data):
        self.data = data
        for k, v in self.data.items():
            self.__dict__[k] = v
        
        self.layers = [layer(l, self) for l in self.layerInstances]
        self.layers.reverse() 

        self.width, self.height = self.pxWid, self.pxHei   
    
    def getTileLayers(self):
        return list(l for l in self.layers if l._type == "Tiles")

class layer:
    def __init__(self, data, level):
        self.data = data
        self.level = level
        for k, v in self.data.items():
            if k[0:2] == '__':      ## Note this part where python seems to dislike the use of __ so I reduced it to a single underscore
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v
        
        if self._type == "Tiles":
            self.loadTileSheet()

    def loadTileSheet(self):
        self.tilesetPath = self._tilesetRelPath
        self.tiles = [tile(t, self) for t in self.gridTiles]
        self.tileSet = pygame.image.load(self.tilesetPath).convert_alpha()
        

class tile:
    def __init__(self, data, layer):
        self.data = data
        self.layer = layer
        for k, v in self.data.items():
            if k[0:2] == '__':      
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v

        self.pos = pygame.Vector2(tuple(self.px))
        self.src = pygame.Vector2(tuple(self.src))
        self.srcRect = (self.src.x, self.src.y, self.layer._gridSize, self.layer._gridSize)
    
    def getImg(self):
        return self.layer.tileSet.subsurface(self.srcRect)

