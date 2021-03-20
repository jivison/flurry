from lib.commands.base_command import BaseCommand, ClientFacingException
from typing import List


class Ping(BaseCommand):
    def __init__(self, client, message, reply):
        super().__init__(client, message, reply)

        self.name = "ping"
        self.aliases = ["pong"]

    async def run(self, args: List[str]):
        await self.message.channel.send("Pong!")
