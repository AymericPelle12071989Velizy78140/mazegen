#!/usr/bin/env python3
from pathlib import Path

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
        argparser.add_argument('input_xlsx_path', type=str, help='Input XLSX file or directory')
        argparser.add_argument('output_path', type=str, help='Output directory')
        argparser.add_argument('-D', '--display', action='store_true')
        return argparser.parse_args()

    def run(self):
        maze_drawer = MazeDrawer()
        maze_drawer.init_from_json_file(self.args.maze_drawer)
        maze_files = self.__input_mazes()
        self.draw_mazes(maze_drawer, maze_files)

    def __input_mazes(self):
        input_xlsx_path = Path(self.args.input_xlsx_path)
        if not input_xlsx_path.exists():
            raise Exception("Input XSLX path does not exist : '{}'".format(self.args.input_xlsx_path))
        if input_xlsx_path.absolute().is_file():
            return [self.args.input_xlsx_path]
        elif input_xlsx_path.is_dir():
            return input_xlsx_path.glob("*.xlsx")
        raise Exception("Input XSLX path must be a file or a directory.")

    def draw_mazes(self, maze_drawer, maze_files):
        self.__check_output_path()
        for maze_file in maze_files:
            self.draw_maze(maze_drawer, str(maze_file), self.__output_file(maze_file))

    def __check_output_path(self):
        odir = Path(self.args.output_path)
        if odir.exists():
            if not odir.is_dir():
                raise Exception("Output path must be a directory : '{}'".format(self.args.output_path))
        else:
            odir.mkdir(parents=True)

    def __output_file(self, input_file, ext="bmp"):
        opath = "{}/{}.{}"
        return opath.format(self.args.output_path, Path(input_file).stem, ext)

    def draw_maze(self, maze_drawer, maze_file, output_file):
        print("# Generating '{output}' from '{input}'...".format(input=maze_file, output=output_file))
        maze = Maze(maze_file)
        with maze_drawer.create_maze_image(maze) as img:
            img.save(filename=output_file)
            if self.args.display:
                display(img)


if __name__ == "__main__":
    program = Mazegen()
    program.run()
