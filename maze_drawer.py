import json
import os
from pathlib import Path

from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

import image_toolkit
import pxconv
from direction import Direction
from maze import Maze


class MazeDrawer:
    # https://docs.wand-py.org/en/0.6.7/

    def __init__(self):
        super().__init__()
        self.square_size = 124
        self.wall_size = 3
        self.bg_color = Color('white')
        self.bg_img_path = None
        self.wall_dict = dict()
        self.square_dict = dict()
        self.square_background_dict = dict()

    def init_from_json_file(self, image_dict_file, rsc_dir=None):
        with open(image_dict_file) as file:
            data = file.read()
            if rsc_dir is None:
                rsc_dir = Path(image_dict_file).parent
            self.load_from_jstruct(json.loads(data), rsc_dir)

    def load_from_jstruct(self, jstruct, rsc_dir=os.getcwd()):
        self.__load_square_size(jstruct)
        self.__load_wall_size(jstruct)
        self.bg_color = Color(jstruct.get('background_color', 'white'))
        bg_img_path = jstruct.get('background_image', None)
        if bg_img_path:
            self.bg_img_path = "{}/{}".format(rsc_dir, bg_img_path)
        self.__load_walls_from_jdict(jstruct['walls'])
        self.__load_square_backgrounds_from_jdict(jstruct['square_backgrounds'], rsc_dir)
        self.__load_squares_from_jdict(jstruct['squares'], rsc_dir)

    def __load_square_size(self, jstruct):
        sq_size = jstruct.get('square_size', "3cm")
        if isinstance(sq_size, str):
            sq_size = pxconv.str_to_px(sq_size)
        self.square_size = int(sq_size)

    def __load_wall_size(self, jstruct):
        wl_size = int(jstruct.get('wall_size', 3))
        if isinstance(wl_size, str):
            wl_size = pxconv.str_to_px(wl_size)
        self.wall_size = int(wl_size)

    def __load_walls_from_jdict(self, wall_jdict):
        self.wall_dict = dict()
        for key, value in wall_jdict.items():
            self.wall_dict[key] = Color(value)

    def __load_square_backgrounds_from_jdict(self, square_background_jdict, rsc_dir: str):
        self.square_background_dict = dict()
        for key, value in square_background_jdict.items():
            self.__load_square_img_from_jdata(self.square_background_dict, key, value, rsc_dir)

    def __load_squares_from_jdict(self, square_jdict, rsc_dir: str):
        self.square_dict = dict()
        for key, value in square_jdict.items():
            self.__load_square_img_from_jdata(self.square_dict, key, value, rsc_dir)

    def __load_square_img_from_jdata(self, img_dict: dict, key: str, jdata, rsc_dir: str):
        assert not key in img_dict
        image = None
        if type(jdata) is str:
            # "Finish": "finish.png"
            img_path = "{}/{}".format(rsc_dir, jdata)
            image = self.__load_image(img_path)
        else:
            # "Finish": { "shortname": "F", "file": "finish.png", "rotation": "90", "hflip": true, "vflip": true }
            img_path = "{}/{}".format(rsc_dir, jdata['file'])
            image = self.__load_image(img_path)
            rotation = int(jdata.get('rotation', 0))
            if rotation != 0:
                iwidth = image.width
                iheight = image.height
                assert iwidth % 2 == 0
                assert iheight % 2 == 0
                image.rotate(rotation)
                left = (image.width - iwidth) // 2
                top = (image.height - iheight) // 2
                image.crop(left=left, top=top, width=iwidth, height=iheight)
            if jdata.get('hflip', False):
                image.flop()
            if jdata.get('vflip', False):
                image.flip()
            shortname = jdata.get('shortname', None)
            if shortname is not None:
                assert not shortname in img_dict
                img_dict[shortname] = image
        img_dict[key] = image

    def __load_image(self, img_path):
        if Path(img_path).suffix == ".svg":
            return image_toolkit.load_svg_image(img_path, self.square_size)
        return image_toolkit.load_image(img_path)

    @property
    def wsquare_size(self):
        return self.wall_size + self.square_size

    def create_corner_image(self):
        return Image(width=self.wall_size, height=self.wall_size, background=self.wall_dict["wall"])

    def create_maze_image(self, maze: Maze):
        maze_img = self.create_empty_maze_image(maze.width, maze.height)
        self.draw_squares(maze_img, maze)
        self.draw_walls(maze_img, maze)
        return maze_img

    def create_empty_maze_image(self, width: int, height: int):
        iwidth = self.wsquare_size * width + self.wall_size
        iheight = self.wsquare_size * height + self.wall_size
        maze_img = Image(width=iwidth, height=iheight, background=self.bg_color)
        if self.bg_img_path:
            self.draw_background(maze_img, width, height)
        self.draw_corners(maze_img, width, height)
        self.draw_empty_walls(maze_img, width, height)
        return maze_img

    def draw_background(self, maze_img, width: int, height: int):
        with Drawing() as draw:
            mz_img_width = self.wsquare_size * width + self.wall_size
            mz_img_height = self.wsquare_size * height + self.wall_size
            bg_img = image_toolkit.load_image(self.bg_img_path, mz_img_width, mz_img_height)
            draw.composite(operator='over', left=0, top=0, width=mz_img_width, height=mz_img_height, image=bg_img)
            draw(maze_img)

    def draw_corners(self, maze_img, width, height):
        corner_img = self.create_corner_image()
        cwidth = corner_img.width
        cheight = corner_img.height
        for j in range(height + 1):
            for i in range(width + 1):
                x = self.wsquare_size * i
                y = self.wsquare_size * j
                with Drawing() as draw:
                    draw.composite(operator='over', left=x, top=y, width=cwidth, height=cheight, image=corner_img)
                    draw(maze_img)

    def draw_empty_walls(self, maze_img, width, height):
        fill_color = self.wall_dict["empty"]
        for j in range(height+1):
            for i in range(width):
                self.draw_top_border(maze_img, i, j, fill_color)
        for j in range(height):
            for i in range(width+1):
                self.draw_left_border(maze_img, i, j, fill_color)

    def draw_squares(self, maze_img, maze: Maze):
        for j in range(maze.height):
            for i in range(maze.width):
                square = maze.getitem(i, j)
                sq_bg = square.background
                if isinstance(sq_bg, str) and len(sq_bg) > 0:
                    sq_img = self.square_background_dict[sq_bg]
                    self.draw_on_square(maze_img, sq_img, i, j)
                sq_type = square.type
                if isinstance(sq_type, str) and len(sq_type) > 0:
                    sq_img = self.square_dict[sq_type]
                    self.draw_on_square(maze_img, sq_img, i, j)

    def draw_walls(self, maze_img, maze: Maze):
        for j in range(maze.height):
            for i in range(maze.width):
                borders = maze.getitem(i, j).borders
                self.draw_top_wall(maze_img, i, j, borders[Direction.TOP])
                self.draw_left_wall(maze_img, i, j, borders[Direction.LEFT])
                self.draw_bottom_wall(maze_img, i, j, borders[Direction.BOTTOM])
                self.draw_right_wall(maze_img, i, j, borders[Direction.RIGHT])

    def draw_top_wall(self, maze_img, i, j, border):
        bd_type = border.type
        if isinstance(bd_type, str) and len(bd_type) > 0:
            bd_color = self.get_border_color(border)
            self.draw_top_border(maze_img, i, j, bd_color)

    def draw_left_wall(self, maze_img, i, j, border):
        bd_type = border.type
        if isinstance(bd_type, str) and len(bd_type) > 0:
            bd_color = self.get_border_color(border)
            self.draw_left_border(maze_img, i, j, bd_color)

    def draw_bottom_wall(self, maze_img, i, j, border):
        bd_type = border.type
        if isinstance(bd_type, str) and len(bd_type) > 0:
            bd_color = self.get_border_color(border)
            self.draw_bottom_border(maze_img, i, j, bd_color)

    def draw_right_wall(self, maze_img, i, j, border):
        bd_type = border.type
        if isinstance(bd_type, str) and len(bd_type) > 0:
            bd_color = self.get_border_color(border)
            self.draw_right_border(maze_img, i, j, bd_color)

    def get_border_color(self, border):
        bd_key = border.as_key()
        if bd_key in self.wall_dict:
            bd_color = self.wall_dict[bd_key]
        else:
            bd_color = Color(border.color)
        return bd_color

    def draw_on_square(self, maze_img, sq_img, i, j):
        with Drawing() as draw:
            x = self.wsquare_size * i + self.wall_size
            y = self.wsquare_size * j + self.wall_size
            draw.composite(operator='over', left=x, top=y,
                           width=self.square_size, height=self.square_size, image=sq_img)
            draw(maze_img)

    def draw_top_border(self, maze_img, i, j, color):
        with Drawing() as draw:
            x = self.wsquare_size * i + self.wall_size
            y = self.wsquare_size * j
            draw.fill_color = color
            draw.rectangle(left=x, top=y, width=self.square_size - 1, height=self.wall_size - 1)
            draw(maze_img)

    def draw_left_border(self, maze_img, i, j, color):
        with Drawing() as draw:
            x = self.wsquare_size * i
            y = self.wsquare_size * j + self.wall_size
            draw.fill_color = color
            draw.rectangle(left=x, top=y, width=self.wall_size - 1, height=self.square_size - 1)
            draw(maze_img)

    def draw_bottom_border(self, maze_img, i, j, color):
        with Drawing() as draw:
            x = self.wsquare_size * i + self.wall_size
            y = self.wsquare_size * j + self.wsquare_size
            draw.fill_color = color
            draw.rectangle(left=x, top=y, width=self.square_size - 1, height=self.wall_size - 1)
            draw(maze_img)

    def draw_right_border(self, maze_img, i, j, color):
        with Drawing() as draw:
            x = self.wsquare_size * i + self.wsquare_size
            y = self.wsquare_size * j + self.wall_size
            draw.fill_color = color
            draw.rectangle(left=x, top=y, width=self.wall_size - 1, height=self.square_size - 1)
            draw(maze_img)
