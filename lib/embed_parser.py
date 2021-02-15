import discord

from lib.config import Config, get_config


class NoReferenceException(Exception):
    pass


class NotZephyrException(Exception):
    pass


class NoEmbedException(Exception):
    pass


class EmbedParser:
    config: Config

    def __init__(self):
        self.config = get_config()

    async def get_embed(self, message: discord.Message) -> discord.Embed:
        reference = await self.get_message(message.channel, message.reference)

        if reference.author.id != self.config.zephyr_id:
            raise NotZephyrException()

        if len(reference.embeds) < 1:
            raise NoEmbedException()

        return reference.embeds[0]

    async def get_message(self, channel: discord.TextChannel, reference: discord.MessageReference) -> discord.Message:
        if reference == None:
            raise NoReferenceException()

        return await channel.fetch_message(reference.message_id)

    async def parse_embed(self, embed: discord.Embed) -> str:
        if (embed.image != None):
            return embed.image.url
        
        raise Exception("No image!")