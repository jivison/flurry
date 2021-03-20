from PIL import Image, ImageDraw, ImageFont
from io import StringIO
import requests
from typing import Tuple


class ImageManipulator:
    def __init__(self):
        pass

    def color(self, image: Image.Image, color: str) -> Image.Image:
        width, height = image.size

        is_large = width == 770

        draw = ImageDraw.Draw(image)

        coordinates = self.get_coordinates(is_large)
        size = self.get_size(is_large)

        draw.rectangle(
            [coordinates, (coordinates[0] + size[0], coordinates[1] + size[1])], fill=color)

        return image

    def get_image_from_url(self, url: str) -> Image.Image:
        im = Image.open(requests.get(url, stream=True).raw)

        return im

    def get_coordinates(self, is_large: bool) -> Tuple[int, int]:
        return (70, 998) if is_large else (32, 453)

    def get_size(self, is_large: bool) -> Tuple[int, int]:
        return (629, 16) if is_large else (285, 8)
