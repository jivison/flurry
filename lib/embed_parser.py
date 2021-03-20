import discord
import re
from typing import Optional


class EmbedParser:
    def parse_embed_image(self, embed: discord.Embed) -> Optional[str]:
        if (embed.image != None):
            return embed.image.url

        return None

    def parse_view_card_description(self, embed: discord.Embed) -> str:
        if ("Flurry" in embed.author.name):
            return embed.description.split("\n")[0]
        else:
            if (embed.description == None):
                return ""

            regex = re.compile(r"(?<=: )`#\d+` \*\*.+")

            return regex.search(embed.description).group()

    def parse_dye_hex_code(self, embed: discord.Embed) -> str:
        regex = re.compile(r"(?<=Hex: \*\*)#\w+",
                           re.IGNORECASE | re.MULTILINE)

        color = regex.search(embed.description).group()

        return color
