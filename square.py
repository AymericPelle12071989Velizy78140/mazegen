from direction import Direction


class Square:
    class Border:
        def __init__(self, btype: str = ""):
            self.type = btype
            pass

        def __str__(self):
            return "'{}'".format(self.type)
    # class

    def __init__(self, stype: str = ""):
        self.type = ""
        self.borders = [Square.Border(), Square.Border(), Square.Border(), Square.Border()]

    @property
    def top(self):
        return self.borders[Direction.TOP]

    @property
    def left(self):
        return self.borders[Direction.LEFT]

    @property
    def bottom(self):
        return self.borders[Direction.BOTTOM]

    @property
    def right(self):
        return self.borders[Direction.RIGHT]

    def __str__(self):
        borders_str = "[{}, {}, {}, {}]".format(self.top, self.left, self.bottom, self.right)
        type_str = self.type.replace('\n', ' ') if self.type is not None else ""
        return "Square:{{'{}', {}}}".format(type_str, borders_str)
