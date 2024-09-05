import os
import asyncio
import discord
import logging
from logging.handlers import TimedRotatingFileHandler
from remind import constants

from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path
from remind.util import discord_common
from remind.util import clist_api


def setup():
    # Make required directories.
    for path in constants.ALL_DIRS:
        os.makedirs(path, exist_ok=True)

    class CustomFormatter(logging.Formatter):
        grey = "\x1b[38;20m"
        cyan = "\x1b[36;20m"
        yellow = "\x1b[33;20m"
        red = "\x1b[31;20m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        format_str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s (%(filename)s:%(lineno)d)"

        FORMATS = {
            logging.DEBUG: cyan + format_str + reset,
            logging.INFO: grey + format_str + reset,
            logging.WARNING: yellow + format_str + reset,
            logging.ERROR: red + format_str + reset,
            logging.CRITICAL: bold_red + format_str + reset,
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)

    ch = logging.StreamHandler()

    ch.setFormatter(CustomFormatter())
    # logging to console and file on daily interval
    logging.basicConfig(
        format="{asctime}:{levelname}:{name}:{message}",
        style="{",
        datefmt="%d-%m-%Y %H:%M:%S",
        level=logging.INFO,
        handlers=[
            ch,
            TimedRotatingFileHandler(
                constants.LOG_FILE_PATH, when="D", backupCount=3, utc=True
            ),
        ],
    )


async def main():
    load_dotenv()

    token = os.getenv("BOT_TOKEN_REMIND")
    if not token:
        logging.error("Token required")
        return

    super_users_str = os.getenv("SUPER_USERS")
    if not super_users_str:
        logging.error("Superusers required")
        return
    constants.SUPER_USERS = list(map(int, super_users_str.split(",")))

    remind_moderator_role = os.getenv("REMIND_MODERATOR_ROLE")
    if remind_moderator_role:
        constants.REMIND_MODERATOR_ROLE = remind_moderator_role

    setup()

    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True

    bot = commands.Bot(command_prefix=commands.when_mentioned_or("t;"), intents=intents)

    cogs = [file.stem for file in Path("remind", "cogs").glob("*.py")]
    for extension in cogs:
        bot.load_extension(f"remind.cogs.{extension}")
    logging.info(f'Cogs loaded: {", ".join(bot.cogs)}')

    async def no_dm_usage_check(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage("Private messages not permitted.")
        return True

    # Restrict bot usage to inside guild channels only.
    bot.add_check(no_dm_usage_check)

    @discord_common.on_ready_event_once(bot)
    async def init():
        clist_api.cache()
        asyncio.create_task(discord_common.presence(bot))

    bot.add_listener(discord_common.bot_error_handler, name="on_command_error")
    await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
