from PIL import Image, ImageDraw, ImageFont
from io import StringIO
import requests


class ImageManipulator:
    def __init__(self):
        pass

    def color(self, image: Image.Image, color: str) -> Image.Image:
        draw = ImageDraw.Draw(image)

        coordinates = (32, 453)
        size = (285, 8)

        draw.rectangle(
            [coordinates, (coordinates[0] + size[0], coordinates[1] + size[1])], fill=color)

        return image

    def get_image_from_url(self, url: str) -> Image.Image:
        im = Image.open(requests.get(url, stream=True).raw)

        return im
