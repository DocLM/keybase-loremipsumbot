import asyncio
import logging
import sys

from .loremipsumbot import LoremIpsumBot

logger = logging.getLogger(__name__)


def main():
    logger.info("Initializing...")
    if "win32" in sys.platform:
        # Windows specific event-loop policy
        asyncio.set_event_loop_policy(
            asyncio.WindowsProactorEventLoopPolicy()  # type: ignore
        )

    listen_options = {}

    asyncio.run(LoremIpsumBot().start(listen_options))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
