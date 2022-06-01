import argparse
import logging
import os
import re
import sys


class Program:
    def __init__(self, name: str = os.path.splitext(sys.argv[0])[0]):
        name = re.sub('\s+', '_', name)
        self.name = re.sub('\s+', '_', name)
        self.args = self._parse_args()
        self._init_logging()
        pass

    def _parse_args(self):
        return argparse.Namespace()

    def _init_logging(self):
        # https://stackoverflow.com/questions/9321741/printing-to-screen-and-writing-to-a-file-at-the-same-time
        logging.basicConfig(filename='{}.log'.format(self.name),
                            level=logging.DEBUG,
                            format='%(levelname)-6s:%(asctime)s: %(message)s',
                            filemode='w',
                            datefmt='%Y-%m-%d %H:%M:%S')
        console = Program.create_console_logging_handler()
        logging.getLogger().addHandler(console)

    @staticmethod
    def create_console_logging_handler():
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('### %(levelname)s: %(message)s')
        console.setFormatter(formatter)
        return console
