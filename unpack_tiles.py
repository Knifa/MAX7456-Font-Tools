#!/usr/bin/env python
import argparse
from PIL import Image


def unpack(filename, width, height, start_index):
    try:
        image = Image.open(filename)
    except:
        print("Couldn't open file: {}".format(filename))
        return

    horiz_tiles = int(image.width / width)
    vert_tiles = int(image.height / height)

    expected_width = horiz_tiles * width
    expected_height = vert_tiles * height
    if not (
        expected_width == image.width
        and expected_height == image.height
    ):
        print("Incorrect sizes: expected image to be {}x{} but is {}x{}".format(
            expected_width, expected_height,
            image.width, image.height
        ))
        return

    for y in range(vert_tiles):
        for x in range(horiz_tiles):
            tile_index = x + y * horiz_tiles
            tile_rect = (
                x * width,
                y * height,
                x * width + width,
                y * height + height
            )

            tile_image = image.crop(tile_rect)
            tile_image.save('{}.png'.format(start_index + tile_index))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Unpacks tiles from an image.')
    parser.add_argument('--start-index', metavar='I', type=int, help='number to start counting files from', default=0)
    parser.add_argument('width', type=int, help='tile width (pixels) (default: 12)', default=12)
    parser.add_argument('height', type=int, help='tile height (pixels) (default: 18)', default=18)
    parser.add_argument('filename', help='image to unpack')

    args = parser.parse_args()
    unpack(args.filename, args.width, args.height, args.start_index)
