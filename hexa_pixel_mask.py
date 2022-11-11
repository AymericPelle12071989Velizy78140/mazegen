from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

from hexa_pixel_shape import HexaPixelShape
from vec2i import Vec2i


class HexaPixelMask:
    def __init__(self, width: int):
        assert width % 4 == 0
        self.__mask_image = Image(width=width, height=width, background=Color("#00000000"))
        self.__mask_image.antialias = False
        self.__pixel_shape = HexaPixelShape(self.__mask_image.width)
        with Drawing() as draw:
            pts = self.hexagon_points()
            draw.polygon(pts)
            draw(self.__mask_image)

    def __off_y(self):
        return self.__pixel_shape.width_2 - self.__pixel_shape.diag_2

    def hexagon_points(self):
        return self.__pixel_shape.points(Vec2i(0, self.__off_y()))

    def crop_image(self, image: Image):
        self.alpha_image(image)
        image.crop(left=0, top=self.__pixel_shape.left_up.y + self.__off_y(),
                   width=image.width, height=self.__pixel_shape.height)

    def alpha_image(self, image):
        with Drawing() as draw:
            draw.composite(operator='dst_in',
                           left=0, top=0, width=image.width, height=image.height,
                           image=self.__mask_image)
            draw(image)

    def create_test_image(self, output_image_path):
        hexa_width = self.__pixel_shape.width
        hexa_image = Image(width=hexa_width, height=hexa_width, background=Color("cyan"))
        self.alpha_image(hexa_image)
        hexa_points = self.hexagon_points()
        with Drawing() as draw:
            draw.fill_color = Color("white")
            draw.color(0, 0, 'replace')
            draw.fill_color = Color("magenta")
            for hexa_pt in hexa_points:
                draw.point(*hexa_pt.xy())
            draw(hexa_image)
        hexa_image.save(filename=output_image_path)
