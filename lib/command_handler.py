from discord import Message, Client, Embed, Colour, User, TextChannel, MessageReference
from typing import Optional, List

from lib.config import get_config
from lib.commands.base_command import BaseCommand, ClientFacingException
from lib.commands.ping import Ping
from lib.commands.help import Help
from lib.commands.dye_card import DyeCard


class CommandHandler:
    def __init__(self, client: Client):
        self.config = get_config()

        self.client = client

        self.commands = [
            Ping, Help, DyeCard
        ]

    async def handle(self, message: Message) -> None:
        if not self.__is_valid_message(message):
            return

        messageContent = self.__get_message_content(
            message).strip().split(" ")

        commandName, args = messageContent[0], [
        ] if messageContent == [""] else messageContent

        command = await self.__find_command(commandName, message)

        if command != None:
            await self.__run_command(command, args[command.args_start_at:])

    async def __find_command(self, commandName: str, message: Message) -> Optional[BaseCommand]:
        embed = await self.get_reply_embed(message)

        for command in self.commands:
            commandInstance: BaseCommand = command(self.client, message, embed)

            if commandInstance.should_run(commandName):
                return commandInstance

        return None

    async def __run_command(self, command: BaseCommand, args: List[str]) -> None:
        print(f"Running command '{type(command).__name__}'")

        try:
            await command.run(args)

        except ClientFacingException as e:
            message = command.message

            embed = Embed(color=Colour.red(),
                          description=e.message)

            embed.set_author(
                name=f"Error | {message.author}", icon_url=message.author.avatar_url)

            await message.channel.send(embed=embed)

    def __is_valid_message(self, message: Message) -> bool:
        return message.author != self.client.user and self.__mentions_user(message.content, self.client.user)

    def __mentions_user(self, content: str, user: User) -> bool:
        return f"<@!{user.id}>" in content or f"<@{user.id}>" in content

    def __get_message_content(self, message: Message) -> str:
        messageContent: str = message.content

        messageContent = messageContent.replace(
            f"<@!{self.client.user.id}>", "").replace(f"<@{self.client.user.id}>", "").strip()

        return messageContent

    async def get_reply_embed(self, message: Message) -> Optional[Embed]:
        reference = await self.__get_message(message.channel, message.reference)

        if reference == None:
            return None

        if reference.author.id != self.config.zephyr_id and reference.author.id != self.config.flurry_id:
            return None

        if len(reference.embeds) < 1:
            None

        return reference.embeds[0]

    async def __get_message(self, channel: TextChannel, reference: Optional[MessageReference]) -> Optional[Message]:
        if reference == None:
            return None

        return await channel.fetch_message(reference.message_id)
