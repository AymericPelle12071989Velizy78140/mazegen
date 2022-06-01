#!/usr/bin/env python3

import logging
import argparse

from wand.display import display

from direction import Direction
from image_dict import ImageDict
from maze import Maze
from maze_drawer import MazeDrawer
from program import Program


class Mazegen(Program):
    def _parse_args(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument('xlsx_file', type=str, help='Input XLSX file')
        argparser.add_argument('sheet', nargs='?', type=str, help='Sheet name', default="")
        return argparser.parse_args()

    def run(self):
        maze = Maze(self.args.xlsx_file, self.args.sheet)
        image_dict = self.__load_images("rsc/square_dict.json")
        maze_drawer = MazeDrawer(image_dict)
        with maze_drawer.create_maze_image(maze) as img:
            display(img)
            img.save(filename="output/maze.bmp")

    def __load_images(self, image_dict_path: str):
        try:
            image_dict = ImageDict(124)
            image_dict.load_images_from_json_file(image_dict_path)
            return image_dict
        except Exception as exc:
            logging.error("Unexpected error: %s", exc)
            raise exc


program = Mazegen()
program.run()
