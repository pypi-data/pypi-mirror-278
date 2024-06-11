#!/usr/bin/env python


"""
A tool for reading text files with an unknown encoding.

Source: https://github.com/bowmanjd/python-chardet-example
"""

import logging
from pathlib import Path

import chardet

from gsi.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def detect_file_encoding(filename: Path, stream_text: bool = False) -> tuple:
    def read_confidently(filename: str) -> tuple:
        """Detect encoding and return decoded text, encoding, and confidence level."""
        filepath = Path(filename)

        # We must read as binary (bytes) because we don't yet know encoding
        blob = filepath.read_bytes()

        detection = chardet.detect(blob)
        encoding = detection["encoding"]
        confidence = detection["confidence"]
        text = blob.decode(encoding) if encoding else None
        return text, encoding, confidence

    if not filename.exists():
        raise FileNotFoundError(f"File not found: {filename.as_posix()}")
    logger.info(f"Reading file: {filename.as_posix()}")
    try:
        text, encoding, confidence = read_confidently(filename.as_posix())
    except Exception as e:
        logger.exception(f"Error reading file: {e}")
        raise
    if encoding:
        # Print the confidence decimal as a percentage
        logger.info(f"Encoding: {encoding} (confidence: {confidence*100:.0f}%)")
    else:
        logger.info("Encoding: unknown")
    if stream_text and text:
        logger.info(f"\n{text}")
    return text, encoding, confidence


class ColorGradient:
    def __init__(
        self: "ColorGradient", start_hex: str, finish_hex: str, n: int
    ) -> None:
        """Create a gradient that is (n) steps between two colors.

        Args:
            start_hex (str): Starting hexidecimal color code.
            finish_hex (str): Ending hexidecimal color code.
            n (int): Number of gradient steps between the starting and
            ending hexidecimal colors.
        """
        self.start_hex = start_hex
        self.finish_hex = finish_hex
        self.n = n

    @classmethod
    def hex_to_rgb(cls, hex: str) -> list[int]:
        """Convert a hexidecimal code to RGB (#FFFFFF -> [255,255,255]).

        Args:
            hex (str): Hexidecimal color code.

        Returns:
            list[int]: List of red, green, and blue color values.
        """
        return [int(hex[i : i + 2], 16) for i in range(1, 6, 2)]

    @classmethod
    def rgb_to_hex(cls, rgb: list[int]) -> str:
        """Convert RGB to a hexidecimal code ([255,255,255] -> #FFFFFF).

        Args:
            rgb (list): List of red, green, and blue color values.

        Returns:
            list[int]: Hexidecimal color code.
        """
        rgb = [int(x) for x in rgb]
        return "#" + "".join(
            ["0{0:x}".format(v) if v < 16 else "{0:x}".format(v) for v in rgb]
        )

    def color_dict(self: "ColorGradient", gradient: list):
        """Takes in a list of RGB sub-lists and returns dictionary of colors
        in RGB and hex form for use in a graphing function defined later on.

        Args:
            gradient (list): List of red, green, and blue color values.

        Returns:
            dict: Dictionary containing RGB and hexidecimal codes
            of the generated color gradient.
        """
        return {
            "hex": [self.rgb_to_hex(rgb) for rgb in gradient],
            "rgb": gradient,
            "r": [rgb[0] for rgb in gradient],
            "g": [rgb[1] for rgb in gradient],
            "b": [rgb[2] for rgb in gradient],
        }

    def linear_gradient(self: "ColorGradient"):
        """Returns a gradient list of (n) colors between two hex colors.

        start_hex and finish_hex should be the full six-digit color string,
        inlcuding the number sign (#FFFFFF).

        Returns:
            dict: Dictionary containing RGB and hexidecimal codes
            of the generated color gradient.
        """
        # Starting and ending colors in RGB form
        s = self.hex_to_rgb(self.start_hex)
        f = self.hex_to_rgb(self.finish_hex)
        # Initilize a list of the output colors with the starting color
        rgb_list = [s]
        # Calcuate a color at each evenly spaced value of t from 1 to n
        for t in range(1, self.n):
            # Interpolate RGB vector for color at the current value of t
            curr_vector = [
                int(s[j] + (float(t) / (self.n - 1)) * (f[j] - s[j])) for j in range(3)
            ]
            # Add it to our list of output colors
            rgb_list.append(curr_vector)
        return self.color_dict(rgb_list)
