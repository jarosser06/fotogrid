'''Fotogrid CLI'''
import argparse
import logging
from dataclasses import dataclass
from os import getcwd
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


LOG = logging.getLogger()
logging.basicConfig(level=logging.INFO)


@dataclass
class Gridder():
    divisions: int
    line_color: str
    line_thickness: int
    filename_suffix: str

    @staticmethod
    def supported_file(file: Path):
        supported_file_extensions = ['jpg', 'jpeg', 'jpe',
                                     'jif', 'jfif']
        if file.is_file():
            if file.suffix.lstrip('.') in supported_file_extensions:
                return True

        return False

    def destination_file_name(self, source: Path):
        source_pth = Path(source)

        filename = source_pth.name
        file_extension = source_pth.suffix
        LOG.debug(f'Filename: {filename}')

        filename_wout_ext = filename.rstrip(file_extension)
        LOG.debug(f'Filename without extension: {filename_wout_ext}')

        dest = [str(source_pth.parent),
                f'{filename_wout_ext}{self.filename_suffix}{file_extension}']
        return '/'.join(dest)

    def draw(self, source: str):
        img = Image.open(source)

        grid_x = img.width/self.divisions
        grid_y = img.height/self.divisions

        draw = ImageDraw.Draw(img)

        for i in range(1, self.divisions):
            draw.line([(grid_x * i, 0), (grid_x * i, img.height)],
                      fill=self.line_color, width=self.line_thickness)
            draw.line([(0, grid_y * i), (img.width, grid_y * i)],
                      fill=self.line_color, width=self.line_thickness)
            i += 1

        img.save(self.destination_file_name(Path(source)), 'JPEG')


def _execute(args: Any):
    photo_path = Path(args.photo_path)
    LOG.debug(f'{photo_path}')

    divisions = int(args.divisions)

    gridder = Gridder(divisions,
                      args.line_color,
                      int(args.line_thickness),
                      args.filename_suffix)

    if photo_path.is_dir():
        LOG.info('Path is a directory ... looking for jpeg images')

        for fil in photo_path.iterdir():
            LOG.info(f'Checking on file {fil}')

            if Gridder.supported_file(fil):
                LOG.info(f'Found supported file {fil} ... drawing grid')
                gridder.draw(str(fil.resolve()))

    elif Gridder.supported_file(photo_path):
        LOG.info(f'Drawing grid for supported file {photo_path}')
        gridder.draw(args.photo_path)

    else:
        raise Exception(f'File {str(photo_path)} is not supported')


def main():
    parser = argparse.ArgumentParser(
        description='JPEG Photo grid tool for painters'
    )
    parser.add_argument('--line-color', '-c', dest='line_color',
                        help='Color of the grid lines', default='black')
    parser.add_argument('--line-thickness', '-t', dest='line_thickness',
                        help='Thickness of grid lines', default=2)
    parser.add_argument('--divisions', '-d', dest='divisions',
                        help='Total number of divisions in grid',
                        default=4)
    parser.add_argument('--destination', '-D', dest='destination',
                        help='Directory to save results')
    parser.add_argument('--filename-suffix', '-P', dest='filename_suffix',
                        default='_grid',
                        help='Suffix to use for resulting file name')
    parser.add_argument('photo_path', default=getcwd(), nargs='?',
                        help='A JPEG file or directory of JPEG files to grid')

    args = parser.parse_args()

    _execute(args)
