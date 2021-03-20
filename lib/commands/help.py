from lib.commands.base_command import BaseCommand, ClientFacingException
from typing import List


class Help(BaseCommand):
    def __init__(self, client, message, reply):
        super().__init__(client, message, reply)

        self.name = "help"

    async def run(self, args: List[str]):
        help_message = f"""
**The following commands are available:**

{self.bullet}`help` - display this message
{self.bullet}`dye` - dye a card

To run a command, mention <@{self.client.user.id}>, with the command name and arguments. For example:
`@Flurry dye #54d7e4`
Some commands take a reply as an argument.
        """

        embed = self.new_embed(authorTitle="Help", description=help_message)

        await self.message.channel.send(embed=embed)
