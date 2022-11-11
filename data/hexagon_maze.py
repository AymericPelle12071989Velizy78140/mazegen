from data.hexagonal_square import HexagonalSquare
from data.maze_base import MazeBase


class HexagonMaze(MazeBase):
    def __init__(self, maze_arg=None):
        super().__init__(maze_arg)

    def _build_square_from_cells(self, s_cell, g_cell, b_cell):
        square = HexagonalSquare()
        square.build_from_cells(s_cell, g_cell, b_cell)
        return square
