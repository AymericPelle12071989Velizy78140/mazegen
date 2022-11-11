class Vec2i:
    def __init__(self, *args):
        match len(args):
            case 0:
                self.x = int(0)
                self.y = int(0)
            case 2:
                self.x = int(args[0])
                self.y = int(args[1])
            case 1:
                if isinstance(args[0], Vec2i):
                    self.x = args[0].x
                    self.y = args[0].y
                else:
                    raise ValueError(args)
            case _:
                raise ValueError(args)

    def xy(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __iadd__(self, other):
        self.x += int(other.x)
        self.y += int(other.y)
        return self

    def __add__(self, other):
        vec = Vec2i(self)
        vec += other
        return vec

    def __isub__(self, other):
        self.x -= int(other.x)
        self.y -= int(other.y)
        return self

    def __sub__(self, other):
        vec = Vec2i(self)
        vec -= other
        return vec

    def __imul__(self, fac):
        self.x = int(self.x * fac)
        self.y = int(self.y * fac)
        return self

    def __mul__(self, fac):
        vec = Vec2i(self)
        vec *= fac
        return vec

    def __idiv__(self, fac):
        self.x = int(self.x / fac)
        self.y = int(self.y / fac)
        return self

    def __div__(self, fac):
        vec = Vec2i(self)
        vec /= fac
        return vec

    def __imod__(self, div):
        self.x %= int(div)
        self.y %= int(div)
        return self

    def __mod__(self, fac):
        vec = Vec2i(self)
        vec %= fac
        return vec

    def __getitem__(self, item):
        match int(item):
            case 0: return self.x
            case 1: return self.y
            case _: raise ValueError(item)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)
