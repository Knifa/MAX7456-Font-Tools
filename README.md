# MAX7456 Font Tools

A hacky set of Python tools for working with MAX7456 fonts (.mcm) using Pillow.
Tested on Python 3.6.1.

## Setup

1. Clone the repository.
2. Install requirements (just Pillow) with `pip install -r requirements.txt`.

## unpack_tiles.py

Splits an input image up into seperate image tiles. Intention is to be used to
generate tiles for a logo, then passed into `max.py`.

### Usage

`./unpack_tiles.py [--start-index I] width height filename`

- `--start-index I`: number to start file indexing from (defaults to 0)
- `width`: width of tiles (defaults to 12 for MAX7456)
- `height`: height of tiles (defaults to 18 for MAX7456)
- `filename`: image to unpack.

The script will output seperate images `I.png` to `I+N.png` in the current
directory.

### Notes

- Images must be divisible by tile width and height.
- Indexing starts from top left of image, sequential, row by row.
- Betaflight OSD starts logos from 160 (at time of writing).

## max.py

Packs or unpacks a MAX7456 font (`.mcm`).

### Usage

`./max.py (--pack | --unpack) filename`

- `--pack`: packs images in current directory into the font file.
- `--unpack`: unpacks images from font into the current directory.
- `filename`: font to pack/unpack.

#### Packing

On packing, the script will grab images `0.png` to `255.png` in the current
directory and pack them from the font file.

Any color other than black or white will be interpreted as transparent.

#### Unpacking

On unpacking, the script will spit out images from `0.png` to `255.png` into
the current directory from the font file.

Transparent pixels are represented by green.

### Notes

- RGB images are expected on packing, and are exported on unpacking.

## License

These scripts are licensed under the MIT License. See `LICENSE.md` for details.
