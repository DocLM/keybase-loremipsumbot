import asyncio
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import islice

import lorem
import pykeybasebot.types.chat1 as chat1
from pykeybasebot import Bot

from .commands import advertised_commands, lorem_ipsum_command

logger = logging.getLogger(__name__)


class Handler:
    def __init__(self):
        self.executor = ThreadPoolExecutor()

    def lorem_ipsum(self, bot, conversation_id, n_messages=1, after=0, delay=0):
        logger.debug(
            "Requested %s messages after %s ms and every %s ms",
            n_messages,
            after,
            delay,
        )

        time.sleep(after / 1000)
        for phrase in map(lambda i: lorem.sentence(), range(0, n_messages)):
            asyncio.run(bot.chat.send(conversation_id, phrase))
            time.sleep(delay / 1000)

    async def __call__(self, bot, event):
        if event.msg.sender.username != bot.username:
            if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
                logger.debug("Received unhandled event %s", event)
                return

            username_pattern = r"^((\@[a-zA-Z]*) *)*"
            command = re.sub(username_pattern, "", event.msg.content.text.body)
            if command.startswith(f"!{lorem_ipsum_command}"):
                arguments = map(int, command.replace(f"!{lorem_ipsum_command}", "").split())
                try:
                    self.executor.submit(
                        self.lorem_ipsum, bot, event.msg.conv_id, *islice(arguments, 3)
                    )
                    return
                except ValueError:
                    logger.debug(f"Invalid {lorem_ipsum_command} format", exc_info=True)

            await bot.chat.send(
                event.msg.conv_id, "Unreconized command: {}".format(command)
            )


class LoremIpsumBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, handler=Handler(), **kwargs)

    async def start(self, listen_options):
        await self.ensure_initialized()
        await self.advertise_commands()
        await super().start(listen_options)

    async def advertise_commands(self):
        return self.chat.execute(advertised_commands)
