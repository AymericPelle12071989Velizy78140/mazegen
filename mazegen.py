#!/usr/bin/env python3

from parse import with_pattern, parse
import argparse

from wand.display import display

import pxconv
from maze import Maze
from maze_drawer import MazeDrawer
from program import Program


class Mazegen(Program):
    def _parse_args(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument('maze_drawer', type=str, help='Input maze drawer JSON file')
        argparser.add_argument('xlsx_file', type=str, help='Input XLSX file')
        argparser.add_argument('output_file', type=str, help='Output file')
        # argparser.add_argument('sheet', nargs='?', type=str, help='Sheet name', default="")
        return argparser.parse_args()

    def run(self):
        # maze = Maze(self.args.xlsx_file, self.args.sheet)
        maze = Maze(self.args.xlsx_file)
        maze_drawer = MazeDrawer()
        maze_drawer.init_from_json_file(self.args.maze_drawer)
        with maze_drawer.create_maze_image(maze) as img:
            display(img)
            img.save(filename=self.args.output_file)


if __name__ == "__main__":
    vstr = ["3cm", "3.5cm", "3 px", "3.5 mm", "3px", "3wh", "3      "]
    for item in vstr:
        print("-" * 80)
        print(pxconv.str_to_px(item), " px!")
    program = Mazegen()
    program.run()
