
class Border:
    def __init__(self, btype=None):
        self._type = None
        self.set_type("" if type is None else str(btype))

    @property
    def type(self):
        return self._type

    def set_type(self, value):
        if value == "_":
            value = ""
        self._type = value

    def __str__(self):
        return f"{self.type}"
