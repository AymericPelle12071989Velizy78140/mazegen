import logging

import openpyxl

from data.square_base import SquareBase


DataCell = openpyxl.cell.cell.Cell


class HexagonalSquare(SquareBase):
    @staticmethod
    def __number_of_borders():
        return 6

    def __init__(self, stype=None, ground=None):
        super().__init__(stype, ground, HexagonalSquare.__number_of_borders())

    def build_from_cells(self, s_cell: DataCell, g_cell: DataCell, b_cell: DataCell):
        assert s_cell is not None
        assert b_cell is not None
        ground = g_cell.value if g_cell is not None else ""
        self._build_from_strings(s_cell.value, ground, b_cell.value.split())
