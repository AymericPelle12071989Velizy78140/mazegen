from grid.types import GridPosition


class Grid:
    def __init__(self, *args):
        self._width = 0
        self._height = 0
        self._data = []
        self.build(args)

    def build(self, *args):
        match len(args):
            case 0:
                pass
            case 2:
                self._width = int(args[0])
                if self._width < 0:
                    raise ValueError(self._width)
                self._height = int(args[1])
                if self._height < 0:
                    raise ValueError(self._height)
                self._data = [None] * (self._width * self._height)
            case 3:
                self._width = int(args[0])
                if self._width < 0:
                    raise ValueError(self._width)
                self._height = int(args[1])
                if self._height < 0:
                    raise ValueError(self._height)
                self._data = [args[2]] * (self._width * self._height)
            case _:
                raise ValueError(len(args))

    @classmethod
    def from_list(cls, width: int, height: int, values: list):
        gr = Grid()
        gr._width = width
        gr._height = height
        count = width * height
        vlen: int = len(values)
        match vlen:
            case vlen if vlen == count:
                gr._data = values
            case vlen if vlen > count:
                gr._data = values[:count]
            case _:  # if vlen < count:
                gr._data = values + [None] * (count - vlen)
        return gr

    def contains_position(self, pos: GridPosition):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def getitem(self, x: int, y: int):
        return self._data[y * self._width + x]

    def __getitem__(self, pos: GridPosition):
        return self._data[pos.y * self._width + pos.x]

    def setitem(self, x: int, y: int, value):
        self._data[y * self._width + x] = value

    def __setitem__(self, pos: GridPosition, value):
        self._data[pos.y * self._width + pos.x] = value

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def count(self) -> int:
        return len(self._data)

    def index_to_position(self, index: int):
        return GridPosition(index % self._width, index / self._height)

    def index(self, item):
        return self.index_to_position(self._data.index(item))

    def __str__(self) -> str:
        res = ""
        for j in range(self._height):
            for i in range(self._width):
                res += str(self.getitem(i, j)) + " "
            res += "\n"
        return res
