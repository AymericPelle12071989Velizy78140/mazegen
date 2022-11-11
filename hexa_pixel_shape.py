import math

from vec2i import Vec2i


class HexaPixelShape:
    def __init__(self, width: int):
        assert width % 4 == 0
        self._width = width
        size_2 = width // 2
        size_4 = width // 4
        diag_2 = int((size_2 * math.sqrt(3)) / 2)
        self.left = Vec2i(0, diag_2)
        self.left_down = Vec2i(int(self.left.x + size_4), self.left.y + diag_2)
        self.right_down = Vec2i(self.left_down.x + size_2 - 1, self.left_down.y)
        self.right = Vec2i(width - 1, self.left.y)
        self.left_up = Vec2i(int(self.left.x + size_4), self.left.y - diag_2)
        self.right_up = Vec2i(self.left_up.x + size_2 - 1, self.left_up.y)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self.left_down.y - self.left_up.y + 1

    @property
    def dimension(self):
        return Vec2i(self.width, self.height)

    @property
    def width_2(self):
        return self._width // 2

    @property
    def width_4(self):
        return self._width // 4

    @property
    def diag_2(self):
        return int((self.width_2 * math.sqrt(3)) / 2)

    def points(self, offset: Vec2i = Vec2i()):
        pts = [x + offset
               for x in [self.left, self.left_up, self.right_up, self.right, self.right_down, self.left_down]]
        return pts
