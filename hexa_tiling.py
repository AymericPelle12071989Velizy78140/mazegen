from hexa_pixel_shape import HexaPixelShape
from vec2i import Vec2i


class HexaTiling:
    def __init__(self, width: int):
        assert width % 4 == 0
        self.__pixel_shape = HexaPixelShape(width)

    def hexagon_width(self):
        return self.__pixel_shape.width

    def hexagon_height(self):
        return self.__pixel_shape.height

    def hexagon_dimension(self):
        return self.__pixel_shape.dimension

    def surface_dimension(self, cr_dim):
        pos = (cr_dim[0] - 1, cr_dim[1] - 1)
        if cr_dim[0] % 2 == 0:
            return self.tile_pos(pos) + self.hexagon_dimension()
        px = self.tile_x(pos[0])
        py = self.tile_y(pos[0] - 1, pos[1])
        return Vec2i(px, py) + self.hexagon_dimension()

    def tile_pos(self, pos):
        px = self.tile_x(pos[0])
        py = self.tile_y(pos[0], pos[1])
        return Vec2i(px, py)

    def tile_x(self, i: int):
        hexa_width = self.hexagon_width()
        if i % 2 == 0:
            i = max(0, i - 1)
            return i * (hexa_width - 1 + hexa_width / 2 - 1)
        i -= 1
        return i * (hexa_width * 3 / 4 - 1) + hexa_width * 3 / 4 - 1

    def tile_y(self, i: int, j: int):
        hexa_height = self.hexagon_height()
        if i % 2 == 0:
            return j * (hexa_height - 1)
        return j * (hexa_height - 1) + hexa_height // 2
