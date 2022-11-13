import logging

from data.border import Border


class SquareBase:
    def __init__(self, stype, ground, nb_border):
        self._type = None
        self._ground = None
        self.set_type("" if stype is None else str(stype))
        self.set_ground("" if ground is None else str(ground))
        self._borders = [Border() for _ in range(nb_border)]

    @property
    def type(self):
        return self._type

    def set_type(self, value: str):
        if value == "_":
            value = ""
        self._type = value

    @property
    def ground(self):
        return self._ground

    def set_ground(self, value: str):
        if value == "_":
            value = ""
        self._ground = value

    def border(self, index: int):
        return self._borders[index]

    def number_of_borders(self):
        return len(self._borders)

    def _build_from_strings(self, stype: str, ground: str, borders: list[str]):
        if stype is None or len(stype) == 0:
            return False
        self.set_type(stype)
        self.set_ground(ground)
        if len(borders) != self.number_of_borders():
            logging.critical(f"Border string list must have {self.number_of_borders()} borders, not {len(borders)}.")
            return False
        for i, border in enumerate(borders):
            self.border(i).set_type(border)
        return True

    def __str__(self):
        bds = ", ".join([f"'{str(x)}'" for x in self._borders])
        return f"[T:'{self.type}', G:'{self._ground}', B:({bds})]"
