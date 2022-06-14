from direction import Direction


class Square:
    class Border:
        def __init__(self, btype: str = "", color: str = "black"):
            self.type = btype
            self.color = color
            pass

        def as_key(self):
            return "{}-{}".format(self.type, self.color)

        def __str__(self):
            if not self.type:
                return "''"
            return "'{}-{}'".format(self.type, self.color)
    # class

    def __init__(self, stype: str = ""):
        self.type = ""
        self._background = ""
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

    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, value):
        self._background = value

    def __str__(self):
        borders_str = "[{}, {}, {}, {}]".format(self.top, self.left, self.bottom, self.right)
        type_str = self.type.replace('\n', ' ') if self.type is not None else ""
        background_str = self._background.replace('\n', ' ') if self._background is not None else ""
        return "Square:{{'{}', '{}', {}}}".format(type_str, background_str, borders_str)
