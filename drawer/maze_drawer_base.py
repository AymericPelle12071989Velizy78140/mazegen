import json
import logging
from pathlib import Path

from wand.color import Color

import image_toolkit
import pxconv


class MazeDrawerBase:
    # https://docs.wand-py.org/en/0.6.7/

    def __init__(self):
        super().__init__()
        # dimensions:
        self.square_size = 124
        self.border_size = 3
        # background:
        self.background_color = Color('white')
        self.background_image_path = None
        # maze components:
        self.square_dict = dict()
        self.ground_dict = dict()
        self.border_dict = dict()

    def init_from_json_file(self, drawer_filepath, rsc_dirpath: Path = None):
        with open(drawer_filepath) as drawer_file:
            data = drawer_file.read()
            if rsc_dirpath is None:
                rsc_dirpath = Path(drawer_filepath).parent
            self.load_from_jstruct(json.loads(data), rsc_dirpath)

    def load_from_jstruct(self, jstruct, rsc_dirpath: Path = None):
        # dimensions:
        self.__load_square_size(jstruct)
        self.__load_border_size(jstruct)
        # background:
        self.background_color = Color(jstruct.get('background_color', 'white'))
        self.__load_background_image(jstruct, rsc_dirpath)
        # maze components:
        self.__load_borders_from_jdict(jstruct['borders'], rsc_dirpath)
        self.__load_grounds_from_jdict(jstruct['grounds'], rsc_dirpath)

    def __load_square_size(self, jstruct):
        sq_size = jstruct.get('square_size', "3cm")
        self.square_size = pxconv.to_px(sq_size)

    def __load_border_size(self, jstruct):
        bd_size = jstruct.get('border_size', "3")
        self.border_size = pxconv.to_px(bd_size)

    def __load_background_image(self, jstruct, rsc_dirpath: Path):
        bg_img_relpath = jstruct.get('background_image', None)
        if bg_img_relpath:
            self.background_image_path = rsc_dirpath / bg_img_relpath

    def __load_borders_from_jdict(self, border_jdict, rsc_dirpath: Path):
        self.wall_dict = dict()
        for key, value in border_jdict.items():
            self.wall_dict[key] = Color(value)

    def __load_grounds_from_jdict(self, ground_jdict, rsc_dirpath: Path):
        self.ground_dict = dict()
        for key, value in ground_jdict.items():
            self.__load_square_image_from_jdata(self.ground_dict, key, value, rsc_dirpath)

    def __load_square_image_from_jdata(self, img_dict: dict, key: str, jdata, rsc_dirpath: Path):
        logging.info(f"{self.__class__.__name__}: Loading image '{key}'.")
        if key in img_dict:
            logging.error(f"{self.__class__.__name__}: Image '{key}' is already loaded in image dict.")
            return
        match jdata:
            case str(jdata):
                self.__load_square_image_from_str(img_dict, jdata, key, rsc_dirpath)
            case _:
                self.__load_square_image_from_jstruct(img_dict, key, jdata, rsc_dirpath)

    def __load_square_image_from_str(self, img_dict, jdata, key, rsc_dirpath):
        # "Finish": "finish.png"
        img_path = rsc_dirpath / jdata
        image = image_toolkit.load_image(str(img_path), self._square_image_size())
        self._filter_image(image)
        img_dict[key] = image

    def _square_image_size(self):
        return self.square_size

    def __load_square_image_from_jstruct(self, img_dict: dict, key: str, jstruct, rsc_dirpath: Path):
        # "Finish": { "shortname": "F", "file": "finish.png", "rotation": "90", "hflip": true, "vflip": true }
        img_path = rsc_dirpath / jstruct['file']
        image = image_toolkit.load_image(str(img_path), self._square_image_size())
        self.__transform_image_with_jstruct(image, jstruct)
        self._filter_image(image)
        img_dict[key] = image
        self.__register_image_with_shortname_if_present(img_dict, jstruct, image)

    def __transform_image_with_jstruct(self, image, jstruct):
        rotation = int(jstruct.get('rotation', 0))
        if rotation != 0:
            image_toolkit.rotate_and_center_crop_image(image, rotation)
        if jstruct.get('hflip', False):
            image.flop()
        if jstruct.get('vflip', False):
            image.flip()

    def __register_image_with_shortname_if_present(self, img_dict, jstruct, image):
        shortname = jstruct.get('shortname', None)
        if shortname is not None:
            if shortname not in img_dict:
                img_dict[shortname] = image
            else:
                logging.error(f"{self.__class__.__name__}: Image '{shortname}' is already loaded in image dict.")

    def _filter_image(self, image):
        pass
