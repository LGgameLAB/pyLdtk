import pygame


class imageLoader:
    def __init__(self, filename):
        self.file = filename

    def getTile(self, rect=None, flags=None):
        pass


class pygameLoader(imageLoader):
    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        self.tilesetImage = pygame.image.load(self.file)
        #pixelalpha = kwargs.get('pixelalpha', True)

    def getTileImage(self, rect, scale=1):
        if rect:
            try:
                tile = self.tilesetImage.subsurface(rect)
            except ValueError:
                print('Tile bounds outside bounds of tileset image')
                raise
        else:
            tile = self.tilesetImage.copy().convert_alpha()

        if scale != 1:
            tile = pygame.transform.scale(tile.convert_alpha(), (tile.get_width()*scale, tile.get_height()*scale))
            
        return tile


class pilLoader(imageLoader):

    def __init__(self, filename, **kwargs):
        super().__init__(filename)
        from PIL import Image
        self.tilesetImage = Image.open(filename)

    def getTileImage(self, rect, scaler=1):
        if rect:
            try:
                rectP = pygame.Rect(rect)
                tile = self.tilesetImage.crop(
                    (rectP.x,
                     rectP.y,
                     rectP.x + rectP.width,
                     rectP.y + rectP.height))
                # Setting the points for cropped image

            except SystemError:  # System error for PIL
                print('ERROR: Tile bounds outside bounds of tileset image')
                raise
        else:
            tile = image.copy()

        return tile
