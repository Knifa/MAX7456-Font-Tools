#!/usr/bin/env python
import argparse
from PIL import Image


HEADER_INDEX = 0
DATA_INDEX = HEADER_INDEX + 1
DATA_CHUNK_SIZE = 64

FONT_COUNT = 256
FONT_WIDTH = 12
FONT_HEIGHT = 18
FONT_BPP = 2

COLOR_BG = (0, 255, 0)
COLOR_MAP_FROM_MAX = {
    '00': (0, 0, 0),
    '01': COLOR_BG,
    '10': (255, 255, 255),
    '11': COLOR_BG
}

COLOR_MAP_FROM_IMAGE = {
    (0, 0, 0): '00',
    (255, 255, 255): '10'
}
COLOR_MAP_FROM_IMAGE_DEFAULT = '01'


def unpack(filename):
    with open(filename) as f:
        lines = [line.rstrip() for line in f]
        if len(lines) < FONT_COUNT * DATA_CHUNK_SIZE + 1:
            print("{} is not a MAX7456 font file or is corrupt (not enough lines).".format(filename))
            return

        header = lines[HEADER_INDEX]
        if not header == 'MAX7456':
            print("{} is probably not a MAX7456 font file (missing header).".format(filename))
            return

        data = lines[DATA_INDEX:]
        for i in range(FONT_COUNT):
            font_data = data[i * DATA_CHUNK_SIZE:i * DATA_CHUNK_SIZE + DATA_CHUNK_SIZE]
            image = get_image_from_max(font_data)
            image.save('{}.png'.format(i))

def pack(filename):
    lines = ["MAX7456\n"]
    with open(filename, 'w') as f:
        for i in range(FONT_COUNT):
            image = Image.open("{}.png".format(i))
            data = get_max_from_image(image)
            lines.extend(data)

        f.writelines(lines)
        f.flush()

def get_image_from_max(data):
    pixels = []
    for line in data:
        for i in range(0, len(line), FONT_BPP):
            pixels.append(line[i:i + FONT_BPP])

    actual_pixels = pixels[:FONT_WIDTH * FONT_HEIGHT]
    image = Image.new('RGB', (FONT_WIDTH, FONT_HEIGHT), color=COLOR_BG)
    for y in range(FONT_HEIGHT):
        for x in range(FONT_WIDTH):
            pixel = pixels[y * FONT_WIDTH + x]
            image.putpixel((x, y), COLOR_MAP_FROM_MAX[pixel])

    return image

def get_max_from_image(image):
    pixels = []
    for y in range(FONT_HEIGHT):
        for x in range(FONT_WIDTH):
            pixel = image.getpixel((x, y))
            pixels.append(map_image_color_to_max(pixel))

    data_lines = []
    for i in range(0, len(pixels), 4):
        data_lines.append("{}\n".format(''.join(pixels[i: i + 4])))

    while len(data_lines) < DATA_CHUNK_SIZE:
        data_lines.append("{}\n".format('01' * 4))

    return data_lines

def map_image_color_to_max(color):
    return COLOR_MAP_FROM_IMAGE.get(color, COLOR_MAP_FROM_IMAGE_DEFAULT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--pack', help='pack the specified file using unpacked images', action='store_true')
    group.add_argument('--unpack', help='unpack the font file into seperate images', action='store_true')
    parser.add_argument('filename', help='font file')

    args = parser.parse_args()
    if args.pack:
        pack(args.filename)
    else:
        unpack(args.filename)
