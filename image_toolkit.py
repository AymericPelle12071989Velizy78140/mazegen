import json
import os
import shutil
import tempfile
from pathlib import Path

from wand.image import Image


def load_image(img_path, *args):
    match len(args):
        case 1:
            return load_image(img_path, args[0], args[0])
        case 0:
            do_resize = False
        case 0 | 2:
            do_resize = True
    img_path = img_path.strip()
    if Path(img_path).suffix == ".svg":
        return load_svg_image(img_path, *args)
    img = Image(filename=img_path)
    if do_resize:
        img.resize(int(args[0]), int(args[1]))
    return img


def load_svg_image(svg_path, *args):
    match len(args):
        case 1:
            return load_svg_image(svg_path, args[0], args[0])
        case 0 | 2:
            pass
    svg_path = svg_path.strip()
    with tempfile.TemporaryDirectory() as tmp_dir:
        png_path = "{}/{}.png".format("/tmp", Path(svg_path).stem)
        convert_svg_to_png(svg_path, png_path, *args)
        img = Image(filename=png_path)
        return img


def convert_svg_to_png(svg_path, png_path, *args):
    match len(args):
        case 1:
            return convert_svg_to_png(svg_path, png_path, args[0], args[0])
        case 2:
            cmd = "rsvg-convert -f png -w {2} -h {3} -o {1} {0}"
            cmd = cmd.format(svg_path, png_path, args[0], args[1])
        case 0:
            cmd = "rsvg-convert -f png -o {1} {0}"
            cmd = cmd.format(svg_path, png_path)
    if not shutil.which("rsvg-convert"):
        raise EnvironmentError("External program 'rsvg-convert' is not found.")
    svg_path = svg_path.strip()
    os.system(cmd)
