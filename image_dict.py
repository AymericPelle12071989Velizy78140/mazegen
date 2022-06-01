import json
import logging
import os
import pathlib
import shutil
import tempfile

from wand.image import Image


class ImageDict:
    def __init__(self, convert_size=1024):
        self.convert_size = convert_size
        self.image_dict = dict()

    def load_images_from_json_file(self, image_dict_file):
        with open(image_dict_file) as file:
            data = file.read()
            self.load_images_from_jdict(json.loads(data))

    def load_images_from_jdict(self, image_jdict):
        for key in image_jdict:
            self.__load_image_from_jdata(key, image_jdict[key])

    def __getitem__(self, item):
        return self.image_dict[item]

    def __load_image_from_jdata(self, key: str, jdata):
        assert not key in self.image_dict
        image = None
        if type(jdata) is str:
            image = self.__load_image(jdata)
        else:
            image = self.__load_image(jdata['file'])
            rotation = int(jdata.get('rotation', 0))
            if rotation != 0:
                image.rotate(rotation)
            if jdata.get('hflip', False):
                image.flop()
            if jdata.get('vflip', False):
                image.flip()
            shortname = jdata.get('shortname', None)
            if shortname is not None:
                assert not shortname in self.image_dict
                self.image_dict[shortname] = image
        self.image_dict[key] = image

    def __load_image(self, value):
        img_path = value.strip()
        with tempfile.TemporaryDirectory() as tmpdirname:
            if pathlib.Path(img_path).suffix == ".svg":
                rsvg_convert_path = shutil.which("rsvg-convert")
                if rsvg_convert_path:
                    cmd = "rsvg-convert -f png -w {2} -h {2} -o {1} {0}"
                    new_img_path = tmpdirname + "/" + pathlib.Path(img_path).stem + ".png"
                    cmd = cmd.format(img_path, new_img_path, self.convert_size * 2)
                    os.system(cmd)
                    img_path = new_img_path
            return Image(filename=img_path)
