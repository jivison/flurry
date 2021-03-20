from discord import Message, MessageReference, Client, Embed, Colour, TextChannel, MessageReference, File
from typing import Optional, Tuple, List
import io
from PIL import Image

from lib.embed_parser import EmbedParser
from lib.image_manipulator import ImageManipulator
from lib.card_store import CardStore
from lib.config import get_config


class ClientFacingException(Exception):
    message: str

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BaseCommand:
    embed_parser = EmbedParser()
    image_manipulator = ImageManipulator()
    card_store = CardStore()

    def __init__(self, client: Client, message: Message, reply: Optional[Embed]):
        self.config = get_config()

        self.message = message
        self.client = client
        self.reply = reply

        self.aliases = []
        self.name = ""
        self.zephyr_embed_titles = []

        self.bullet = "•"
        self.args_start_at = 1

    async def run(self, args: List[str]) -> None:
        pass

    async def prerun(self) -> bool:
        self.reply_message, self.reply_embed = await self.__get_reply(message)

        if not self.__is_valid_message(this.message):
            return False

        return True

    def should_run(self, commandName: str) -> bool:
        if self.reply != None:
            for embed_title in self.zephyr_embed_titles:
                if embed_title in self.reply.author.name:
                    self.args_start_at = 0

                    return True

        if self.name != "":
            if commandName.lower() == self.name.lower():
                return True

        if len(self.aliases) > 1:
            if commandName.lower() in self.aliases:
                return True

        return False

    def new_embed(self, authorTitle="", description="", title="", color=None) -> Embed:
        embed = Embed(title=title,
                      color=color if color != None else Colour.greyple(), description=description)

        embed.set_author(
            name=f"Flurry | {authorTitle} | {self.message.author}" if authorTitle != "" else "Flurry", icon_url=self.message.author.avatar_url)

        return embed

    def get_argument(self, args: List[str], atPosition: int) -> Optional[str]:
        try:
            return args[atPosition]
        except IndexError:
            return None

    def get_discord_file(self, image: Image.Image) -> File:
        with io.BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)

            return File(fp=image_binary, filename="zephyrdrip.png")

    def replied_to(self, embed_title: str) -> bool:
        if self.reply == None:
            return False

        return embed_title in self.reply.author.name
