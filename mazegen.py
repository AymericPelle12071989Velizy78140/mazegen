#!/usr/bin/env python3
import logging
import math
import os
from builtins import min
from pathlib import Path

from parse import with_pattern, parse
import argparse

from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.image import Image

import pxconv
from data.hexagon_maze import HexagonMaze
from hexa_pixel_mask import HexaPixelMask
from hexa_tiling import HexaTiling
from maze import Maze
from maze_drawer import MazeDrawer
from program import Program
from vec2i import Vec2i


class Mazegen(Program):
    def _parse_args(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument('maze_drawer', type=str, help='Input maze drawer JSON file')
        argparser.add_argument('input_path', type=str, help='Input XLSX file or directory')
        argparser.add_argument('output_directory_path', type=str, help='Output directory')
        argparser.add_argument('-D', '--display', action='store_true')
        argparser.add_argument('-S', '--square_maze', action='store_true')
        argparser.add_argument('-H', '--hexagon_maze', action='store_true')
        return argparser.parse_args()

    def run(self):
        # try:
            # self.wip()
        maze_files = self.__input_mazes()
        maze_drawer = self.__load_maze_drawer()
        self.draw_mazes(maze_drawer, maze_files)
        # except BaseException as ex:
        #     logging.critical(f"Exception raised: {ex}")
        #     raise ex

    # SQUARE or HEXA
    def __load_maze_drawer(self):
        if self.args.square_maze:
            maze_drawer = MazeDrawer()
            maze_drawer.init_from_json_file(self.args.maze_drawer)
            return maze_drawer
        if self.args.hexagon_maze:
            return None
        raise Exception("WHUT")

    # SQUARE or HEXA
    def __load_maze(self, maze_file):
        if self.args.square_maze:
            return Maze(maze_file)
        if self.args.hexagon_maze:
            return HexagonMaze(maze_file)
        raise Exception("WHUT")

    def wip(self):
        hexa_width = 124

        hexa_pixel_mask = HexaPixelMask(hexa_width)
        hexa_tiling = HexaTiling(hexa_width)

        hexa_pixel_mask.create_test_image(f"/tmp/hexatest_{hexa_width}.bmp")

        sq_image = Image(filename=f"rsc/img/hexa/hexatest_{hexa_width}.bmp")
        hexa_pixel_mask.crop_image(sq_image)

        surface_dim = hexa_tiling.surface_dimension((4, 4))
        mz_image = Image(width=surface_dim.x, height=surface_dim.y, background=Color("#00000000"))
        for j in range(0, 4):
            for i in range(0, 4):
                with Drawing() as draw:
                    sq_pos = hexa_tiling.tile_pos((i, j))
                    draw.composite(operator='over',
                                   left=sq_pos[0], top=sq_pos[1], width=sq_image.width, height=sq_image.height,
                                   image=sq_image)
                    draw(mz_image)
#        mz_image.antialias = False
        with Drawing() as draw:
            draw.stroke_width = 4
            draw.stroke_color = Color('black')
            draw.line((50, 50), (400, 200))
            draw(mz_image)

        image_path = "output/mz_image.png"
        mz_image.save(filename=image_path)
        os.system(f"eog {image_path}")
        # if Path(image_path).exists():
        #     os.remove(image_path)

    def __input_mazes(self):
        input_path = Path(self.args.input_path)
        if not input_path.exists():
            raise Exception("Input path does not exist : '{}'".format(self.args.input_path))
        if input_path.absolute().is_file():
            return [self.args.input_path]
        elif input_path.is_dir():
            return input_path.glob("*.xlsx")
        raise Exception("Input path must be a file or a directory.")

    def draw_mazes(self, maze_drawer, maze_files):
        self.__check_output_path()
        for maze_file in maze_files:
            self.draw_maze(maze_drawer, str(maze_file), self.__output_file(maze_file))

    def draw_maze(self, maze_drawer, maze_file, output_file):
        logging.info(f"Generating '{output_file}' from '{maze_file}'...")
        maze = self.__load_maze(maze_file)
        if maze_drawer is None:
            logging.error("WIP: No maze drawer provided.")
            return
        with maze_drawer.create_maze_image(maze) as img:
            img.save(filename=output_file)
            if self.args.display:
                # os.system(f"eog {output_file}")
                display(img)

    def __check_output_path(self):
        odir = Path(self.args.output_directory_path)
        if odir.exists():
            if not odir.is_dir():
                raise Exception("Output path must be a directory : '{}'".format(self.args.output_directory_path))
        else:
            odir.mkdir(parents=True)

    def __output_file(self, input_file, ext="bmp"):
        opath = "{}/{}.{}"
        return opath.format(self.args.output_directory_path, Path(input_file).stem, ext)


if __name__ == "__main__":
    program = Mazegen()
    program.run()
