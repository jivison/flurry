from lib.commands.base_command import BaseCommand, ClientFacingException
from typing import List, Optional
import re

from lib.embed_parser import EmbedParser
from lib.image_manipulator import ImageManipulator
from lib.card_store import CardStore, Card

from PIL import Image


class DyeCard(BaseCommand):
    def __init__(self, client, message, reply):
        super().__init__(client, message, reply)

        self.name = "dye"
        self.zephyr_embed_titles = ["View Card", "Preview Card", "View Dye"]

        self.embed_parser = EmbedParser()
        self.image_manipulator = ImageManipulator()
        self.card_store = CardStore()

    # Override of default to allow backwards compatibilty with `@Flurry <hex code>`
    def should_run(self, commandName: str) -> bool:
        hexRegex = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")

        match = hexRegex.search(commandName)

        if super().should_run(commandName):
            return True

        elif match != None:
            self.args_start_at = 0

            return True

        return False

    async def run(self, args: List[str]):
        color = self.__get_color(args)

        card = None

        if self.replied_to("View Card") or self.replied_to("Preview Card"):
            card_url = self.embed_parser.parse_embed_image(self.reply)
            card_image = self.image_manipulator.get_image_from_url(card_url)
            card_description = self.embed_parser.parse_view_card_description(
                self.reply)

            card = self.card_store.add_card(
                self.message.author.id, card_image, card_description)
            await self.message.add_reaction("✅")
        else:
            card = self.card_store.get_card(self.message.author.id)

        if card != None and color != None:
            image = self.__dye_card(card, color)

            image_file = self.get_discord_file(image)

            readableHex = int(hex(int(color.replace("#", ""), 16)), 0)

            embed = self.new_embed(
                authorTitle="Preview Card",
                color=readableHex, description=card.description + f"\n\nPreviewing with **{color}**")

            embed.set_image(url="attachment://zephyrdrip.png")

            await self.message.channel.send(embed=embed, file=image_file)
        elif card == None:
            raise ClientFacingException(
                "Please mention me in a reply to a Zephyr `.card` embed to select a card!")

    def __get_color(self, args: List[str]) -> Optional[str]:
        if self.replied_to("View Dye"):
            return self.embed_parser.parse_dye_hex_code(self.reply)

        return self.get_argument(args, 0)

    def __dye_card(self, card: Card, color: str) -> Image.Image:
        try:
            return self.image_manipulator.color(card.card, color)
        except ValueError:
            raise ClientFacingException(
                "Please enter a valid hex code! _(eg. #ffc107)_")
