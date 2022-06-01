from wand.image import Image
from wand.color import Color
from wand.drawing import Drawing

from direction import Direction
from image_dict import ImageDict
from maze import Maze


class MazeDrawer:
    # https://docs.wand-py.org/en/0.6.7/

    def __init__(self, square_dict: ImageDict):
        super().__init__()
        self.square_dict = square_dict
        self.bg_color = Color('white')
        self.empty_wall_color = Color('rgb(207,207,207)')
        self.wall_color = Color('black')
        self.square_size = 124
        self.wall_size = 3

    @property
    def wsquare_size(self):
        return self.wall_size + self.square_size

    def create_corner_image(self):
        return Image(width=self.wall_size, height=self.wall_size, background=self.wall_color)

    def create_maze_image(self, maze: Maze):
        maze_img = self.create_empty_maze_image(maze.width, maze.height)
        self.draw_squares(maze_img, maze)
        self.draw_walls(maze_img, maze)
        return maze_img

    def create_empty_maze_image(self, width: int, height: int):
        iwidth = self.wsquare_size * width + self.wall_size
        iheight = self.wsquare_size * height + self.wall_size
        maze_img = Image(width=iwidth, height=iheight, background=self.bg_color)
        self.draw_corners(maze_img, width, height)
        self.draw_empty_walls(maze_img, width, height)
        return maze_img

    def draw_corners(self, maze_img, width, height):
        corner_img = self.create_corner_image()
        cwidth = corner_img.width
        cheight = corner_img.height
        with Drawing() as draw:
            for j in range(height + 1):
                for i in range(width + 1):
                    x = self.wsquare_size * i
                    y = self.wsquare_size * j
                    draw.composite(operator='over', left=x, top=y, width=cwidth, height=cheight, image=corner_img)
                    draw(maze_img)

    def draw_empty_walls(self, maze_img, width, height):
        with Drawing() as draw:
            draw.fill_color = self.empty_wall_color
            for j in range(height+1):
                for i in range(width):
                    self.draw_top_border(maze_img, draw, i, j)
            for j in range(height):
                for i in range(width+1):
                    self.draw_left_border(maze_img, draw, i, j)

    def draw_squares(self, maze_img, maze: Maze):
        with Drawing() as draw:
            for j in range(maze.height):
                for i in range(maze.width):
                    sq_type = maze.getitem(i, j).type
                    if isinstance(sq_type, str) and len(sq_type) > 0:
                        sq_img = self.square_dict[sq_type]
                        self.draw_square(maze_img, draw, sq_img, i, j)
            pass

    def draw_walls(self, maze_img, maze: Maze):
        with Drawing() as draw:
            for j in range(maze.height):
                for i in range(maze.width):
                    borders = maze.getitem(i, j).borders
                    bd_type = borders[Direction.TOP].type
                    if isinstance(bd_type, str) and len(bd_type) > 0:
                        draw.fill_color = self.wall_color
                        self.draw_top_border(maze_img, draw, i, j)
                    bd_type = borders[Direction.LEFT].type
                    if isinstance(bd_type, str) and len(bd_type) > 0:
                        draw.fill_color = self.wall_color
                        self.draw_left_border(maze_img, draw, i, j)
                    bd_type = borders[Direction.BOTTOM].type
                    if isinstance(bd_type, str) and len(bd_type) > 0:
                        draw.fill_color = self.wall_color
                        self.draw_bottom_border(maze_img, draw, i, j)
                    bd_type = borders[Direction.RIGHT].type
                    if isinstance(bd_type, str) and len(bd_type) > 0:
                        draw.fill_color = self.wall_color
                        self.draw_right_border(maze_img, draw, i, j)

    def draw_square(self, maze_img, draw, sq_img, i, j):
        x = self.wsquare_size * i + self.wall_size
        y = self.wsquare_size * j + self.wall_size
        draw.composite(operator='over', left=x, top=y,
                       width=self.square_size, height=self.square_size, image=sq_img)
        draw(maze_img)

    def draw_top_border(self, maze_img, draw, i, j):
        x = self.wsquare_size * i + self.wall_size
        y = self.wsquare_size * j
        draw.rectangle(left=x, top=y, width=self.square_size - 1, height=self.wall_size - 1)
        draw(maze_img)

    def draw_left_border(self, maze_img, draw, i, j):
        x = self.wsquare_size * i
        y = self.wsquare_size * j + self.wall_size
        draw.rectangle(left=x, top=y, width=self.wall_size - 1, height=self.square_size - 1)
        draw(maze_img)

    def draw_bottom_border(self, maze_img, draw, i, j):
        x = self.wsquare_size * i + self.wall_size
        y = self.wsquare_size * j + self.wsquare_size
        draw.rectangle(left=x, top=y, width=self.square_size - 1, height=self.wall_size - 1)
        draw(maze_img)

    def draw_right_border(self, maze_img, draw, i, j):
        x = self.wsquare_size * i + self.wsquare_size
        y = self.wsquare_size * j + self.wall_size
        draw.rectangle(left=x, top=y, width=self.wall_size - 1, height=self.square_size - 1)
        draw(maze_img)
