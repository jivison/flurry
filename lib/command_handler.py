import discord
import io
import re
from typing import List, Optional
from PIL import Image

from lib.embed_parser import EmbedParser, NoReferenceException, NotZephyrException, NoEmbedException
from lib.image_manipulator import ImageManipulator
from lib.card_store import CardStore


class ClientFacingException(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class CommandHandler:
    client: discord.Client
    embed_parser: EmbedParser
    image_manipulator: ImageManipulator
    card_store: CardStore

    def __init__(self, client: discord.client):
        self.client = client
        self.embed_parser = EmbedParser()
        self.image_manipulator = ImageManipulator()
        self.card_store = CardStore()

    async def handle(self, message: discord.Message) -> None:
        if not self.is_valid_message(message):
            return None

        embed = None

        try:
            embed = await self.embed_parser.get_embed(message)

            await self.handle_embed_reply(message, embed)

        except NoReferenceException:
            card = self.card_store.get_card(message.author.id)
            color = self.get_argument(message, 0)

            if (card != None and color != None):
                await self.dye_card(card, message, color)
            elif card == None:
                raise ClientFacingException(
                    "Please mention me in a reply to a Zephyr `.card` embed to select a card!")
            elif color == None:
                raise ClientFacingException(
                    "Please specify a colour for me to dye the card with!")

        except (NoEmbedException, NotZephyrException):
            pass

    async def handle_embed_reply(self, message: discord.Message, embed: discord.Embed) -> None:
        color = None
        card = None

        if "View Dye" in embed.author.name:
            card = self.card_store.get_card(message.author.id)

            if card == None:
                raise ClientFacingException(
                    "Please mention me in a reply to a Zephyr `.card` embed to select a card!")

            regex = re.compile(r"(?<=Hex: \*\*)#\w+",
                               re.IGNORECASE | re.MULTILINE)
            color = regex.search(embed.description).group()

        elif "View Card" in embed.author.name:
            url = await self.embed_parser.parse_embed(embed)

            card = self.image_manipulator.get_image_from_url(url)

            self.card_store.add_card(message.author.id, card)
            await message.add_reaction("✅")

            color = self.get_argument(message, 0)

        else:
            raise ClientFacingException(
                "Please mention me with a valid Zephyr embed! (either `viewdye` or `viewcard`)")

        if color != None and card != None:
            await self.dye_card(card, message, color)

    async def dye_card(self, card: Image.Image, message: discord.Message, color: str) -> None:
        image = None

        try:
            image = self.image_manipulator.color(card, color)
        except ValueError:
            raise ClientFacingException(
                "Please enter a valid hex code! _(eg. #ffc107)_")

        await self.send_pillow_image(message.channel, image)

    def is_valid_message(self, message: discord.Message) -> bool:
        return message.author != self.client.user and self.mentions_user(message.content, self.client.user)

    def mentions_user(self, content: str, user: discord.User) -> bool:
        return f"<@!{user.id}>" in content or f"<@{user.id}>" in content

    def get_arguments(self, message: discord.Message, required_length: int = None) -> List[str]:
        arguments = message.content.split()[1:]

        if required_length != None and len(arguments) < required_length:
            raise ClientFacingException("Please enter a colour!")
        else:
            return arguments

    def get_argument(self, message: discord.Message, index: int) -> Optional[str]:
        try:
            return self.get_arguments(message)[index]
        except IndexError:
            return None

    async def send_pillow_image(self, channel: discord.TextChannel, image: Image.Image) -> None:
        with io.BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)

            await channel.send(file=discord.File(fp=image_binary, filename="ooga.png"))
