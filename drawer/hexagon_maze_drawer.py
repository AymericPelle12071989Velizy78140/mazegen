from wand.drawing import Drawing
from wand.image import Image

import hexa_tiling
import image_toolkit
from data.hexagon_maze import HexagonMaze
from drawer.maze_drawer_base import MazeDrawerBase


class HexagonMazeDrawer(MazeDrawerBase):
    def __init__(self):
        super().__init__()
        self._tiling = hexa_tiling.HexaTiling(self.square_size * 2)

    def create_maze_image(self, maze: HexagonMaze):
        maze_img = self.__create_empty_maze_image(maze)
        return maze_img

    def __create_empty_maze_image(self, maze: HexagonMaze):
        image_dim = self._tiling.surface_dimension((maze.width, maze.height))
        maze_img = Image(width=image_dim.x, height=image_dim.y, background=self.background_color)
        if self.background_image_path:
            self._draw_background(maze_img, image_dim)
        return maze_img

    def _draw_background(self, maze_img, image_dim):
        with Drawing() as draw:
            bg_img = image_toolkit.load_image(str(self.background_image_path), image_dim.x, image_dim.y)
            draw.composite(operator='over', left=0, top=0, width=image_dim.x, height=image_dim.y, image=bg_img)
            draw(maze_img)
