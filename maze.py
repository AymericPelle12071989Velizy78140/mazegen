import openpyxl

import grid.grid
from direction import Direction
from square import Square


class Maze(grid.grid.Grid):
    class Square(Square):
        def __init__(self):
            super().__init__()

        def __init__(self, cell: openpyxl.cell.cell.Cell):
            super().__init__()
            self.type = cell.value
            self.borders[Direction.TOP] = Maze.Square.__border_from_side(cell.border.top)
            self.borders[Direction.LEFT] = Maze.Square.__border_from_side(cell.border.left)
            self.borders[Direction.BOTTOM] = Maze.Square.__border_from_side(cell.border.bottom)
            self.borders[Direction.RIGHT] = Maze.Square.__border_from_side(cell.border.right)

        @staticmethod
        def __border_from_side(side: openpyxl.styles.borders.Side):
            # https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.borders.html?highlight=border#openpyxl.styles.borders.Border
            if side.style is not None:
                match side.style:
                    case "hair"|"thin"|"thick"|"medium":
                        return Maze.Square.Border("wall")
                    case _:
                        pass
            return Maze.Square.Border()
    # class

    def __init__(self, maze_arg=None, sheet_name: str = ""):
        # https://www.geeksforgeeks.org/python-reading-excel-file-using-openpyxl-module/
        if maze_arg is not None:
            if type(maze_arg) is openpyxl.workbook.workbook.Workbook:
                self.build_from_workbook(maze_arg, sheet_name)
            elif type(maze_arg) is openpyxl.worksheet.worksheet.Worksheet:
                self.build_from_sheet(maze_arg)
            elif type(maze_arg) is str:
                self.build_from_xslx(maze_arg, sheet_name)

    def build_from_xslx(self, xlsx_file: str, sheet_name: str = ""):
        wbook = openpyxl.load_workbook(xlsx_file)
        self.build_from_workbook(wbook, sheet_name)

    def build_from_workbook(self, wbook: openpyxl.workbook.workbook.Workbook, sheet_name: str = ""):
        sheet = wbook.active if sheet_name == "" else wbook[sheet_name]
        self.build_from_sheet(sheet)

    def build_from_sheet(self, sheet: openpyxl.worksheet.worksheet.Worksheet):
        self.build(sheet.max_column - sheet.min_column + 1, sheet.max_row - sheet.min_row + 1)
        j = 0
        for sj in range(sheet.min_row, sheet.max_row + 1):
            i = 0
            for si in range(sheet.min_column, sheet.max_column + 1):
                cell = sheet.cell(row=sj, column=si)
                square = Maze.Square(cell)
                print("{},{}: {}".format(si, sj, square))
                self.setitem(i, j, square)
                i += 1
            j += 1
            print()
