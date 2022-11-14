import logging
from pathlib import Path

from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

import hexa_tiling
import image_toolkit
from data.border import Border
from data.hexagon_maze import HexagonMaze
from data.hexagonal_square import HexagonalSquare
from drawer.maze_drawer_base import MazeDrawerBase
from grid.types import GridPosition
from hexa_pixel_mask import HexaPixelMask
from vec2i import Vec2i


class HexagonMazeDrawer(MazeDrawerBase):
    def __init__(self):
        super().__init__()
        self._tiling = hexa_tiling.HexaTiling(self.square_size * 2)
        self._hexa_pixel_mask = HexaPixelMask(self._tiling.hexagon_width())

    def load_from_jstruct(self, jstruct, rsc_dirpath: Path = None):
        super().load_from_jstruct(jstruct, rsc_dirpath)
        assert self.square_size % 2 == 0
        self._tiling = hexa_tiling.HexaTiling(self.square_size * 2)
        self._hexa_pixel_mask = HexaPixelMask(self._tiling.hexagon_width())

    def create_maze_image(self, maze: HexagonMaze):
        maze_img = self.__create_empty_maze_image(maze)
        self._draw_squares(maze, maze_img)
        return maze_img

    def __create_empty_maze_image(self, maze: HexagonMaze):
        image_dim = self._tiling.surface_dimension((maze.width, maze.height))
        maze_img = Image(width=image_dim.x, height=image_dim.y, background=Color("#00000000"))
        if self.background_image_path:
            self._draw_background(maze_img, image_dim)
        return maze_img

    def _draw_background(self, maze_img, image_dim):
        with Drawing() as draw:
            bg_img = image_toolkit.load_image(str(self.background_image_path), image_dim.x, image_dim.y)
            draw.composite(operator='over', left=0, top=0, width=image_dim.x, height=image_dim.y, image=bg_img)
            draw(maze_img)

    def _draw_squares(self, maze: HexagonMaze, maze_img: Image):
        for j in range(maze.height):
            for i in range(maze.width):
                tile_pos = GridPosition(i, j)
                h_square = maze[tile_pos]
                if h_square is not None:
                    assert isinstance(h_square, HexagonalSquare)
                    self._draw_square(h_square, tile_pos, maze_img)
        for j in range(maze.height):
            for i in range(maze.width):
                tile_pos = GridPosition(i, j)
                h_square = maze[tile_pos]
                if h_square is not None:
                    assert isinstance(h_square, HexagonalSquare)
                    self._draw_square_borders(h_square, tile_pos, maze_img)

    def _draw_square(self, square: HexagonalSquare, tile_pos: GridPosition, maze_img: Image):
        sq_ground = square.ground
        if isinstance(sq_ground, str) and len(sq_ground) > 0:
            ground_img: Image = self.ground_dict[sq_ground]
            self._draw_on_tile(ground_img, tile_pos, maze_img)
        sq_type = square.type
        if isinstance(sq_type, str) and len(sq_type) > 0:
            type_img: Image = self.square_dict[sq_type]
            self._draw_on_tile(type_img, tile_pos, maze_img)

    def _draw_square_borders(self, square: HexagonalSquare, tile_pos: GridPosition, maze_img: Image):
        tile_pixel_pos = self._tiling.tile_pos(tile_pos)
        points = self._hexa_pixel_mask.hexagon_pixel_shape.points(tile_pixel_pos)
        points.append(points[0])
        for bd_index in range(square.number_of_borders()):
            border: Border = square.border(bd_index)
            if isinstance(border.type, str) and len(border.type) > 0:
                border_style = self.border_dict[border.type]
                with Drawing() as draw:
                    draw.stroke_color = border_style
                    draw.stroke_width = self.border_size
                    draw.line(points[bd_index].xy(), points[bd_index + 1].xy())
                    draw(maze_img)

    def _draw_on_tile(self, image: Image, t_pos: GridPosition, maze_img: Image):
        tile_img_pos = self._tiling.tile_pos(t_pos)
        with Drawing() as draw:
            draw.composite(operator='over',
                           left=tile_img_pos.x, top=tile_img_pos.y,
                           width=image.width, height=image.height, image=image)
            draw(maze_img)

    def _filter_image(self, image):
        self._hexa_pixel_mask.crop_image(image)

    def _square_image_size(self):
        return self._tiling.hexagon_width()
