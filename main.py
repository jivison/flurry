import discord

from lib.command_handler import CommandHandler, ClientFacingException
from lib.embed_parser import EmbedParser
from lib.config import get_config

client = discord.Client()
handler = CommandHandler(client)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    await handler.handle(message)


client.run(get_config().discord_token)
