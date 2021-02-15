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
    try:
        await handler.handle(message)

    except ClientFacingException as e:
        embed = discord.Embed(color=discord.Colour.red(),
                              description=e.message)

        embed.set_author(
            name=f"Error | {message.author}", icon_url=message.author.avatar_url)

        await message.channel.send(embed=embed)


client.run(get_config().discord_token)
