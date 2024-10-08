import os
import subprocess
import sys
import time
import textwrap

from discord.ext import commands
from remind.util.discord_common import pretty_time_format
from remind.util import clist_api
from remind import constants

from remind.util import discord_common

RESTART = 42


# Adapted from numpy sources.
# https://github.com/numpy/numpy/blob/master/setup.py#L64-85
def git_history():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ["SYSTEMROOT", "PATH"]:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env["LANGUAGE"] = "C"
        env["LANG"] = "C"
        env["LC_ALL"] = "C"
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        branch = out.strip().decode("ascii")
        out = _minimal_ext_cmd(["git", "log", "--oneline", "-5"])
        history = out.strip().decode("ascii")
        return (
            "Branch:\n"
            + textwrap.indent(branch, "  ")
            + "\nCommits:\n"
            + textwrap.indent(history, "  ")
        )
    except OSError:
        return "Fetching git info failed"


def check_if_superuser(ctx):
    return ctx.author.id in constants.SUPER_USERS


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.group(brief="Bot control", invoke_without_command=True)
    async def meta(self, ctx):
        """Command the bot or get information about the bot."""
        await ctx.send_help(ctx.command)

    @meta.command(brief="Restarts Remind")
    @commands.check(check_if_superuser)
    async def restart(self, ctx):
        """Restarts the bot."""
        # Really, we just exit with a special code
        # the magic is handled elsewhere
        await ctx.send("Restarting...")
        os._exit(RESTART)

    @meta.command(brief="Kill Remind")
    @commands.check(check_if_superuser)
    async def kill(self, ctx):
        """Restarts the bot."""
        await ctx.send("Dying...")
        os._exit(0)

    @meta.command(brief="Is Remind up?")
    async def ping(self, ctx):
        """Replies to a ping."""
        start = time.perf_counter()
        message = await ctx.send(":ping_pong: Pong!")
        end = time.perf_counter()
        duration = (end - start) * 1000
        content = f"REST API latency: {int(duration)}ms\n"
        f"Gateway API latency: {int(self.bot.latency * 1000)}ms"
        await message.edit(content=content)

    @meta.command(brief="Get git information")
    async def git(self, ctx):
        """Replies with git information."""
        await ctx.send("```yaml\n" + git_history() + "```")

    @meta.command(brief="Prints bot uptime")
    async def uptime(self, ctx):
        """Replies with how long Remind has been up."""
        await ctx.send(
            "Remind has been running for "
            + pretty_time_format(time.time() - self.start_time)
        )

    @meta.command(brief="Print bot guilds")
    @commands.check(check_if_superuser)
    async def guilds(self, ctx):
        "Replies with info on the bot's guilds"
        msg = [
            f"Guild ID: {guild.id} | Name: {guild.name}"
            f"| Owner: {guild.owner.id} | Icon: {guild.icon}"
            for guild in self.bot.guilds
        ]
        await ctx.send("```" + "\n".join(msg) + "```")

    @meta.command(brief="Forcefully reset contests")
    @commands.has_any_role("Admin", constants.REMIND_MODERATOR_ROLE)
    async def resetcache(self, ctx):
        """Resets contest cache."""
        try:
            clist_api.cache(True)
            await ctx.send(
                "```Cache reset completed. "
                "Restart to reschedule all contest reminders."
                "```"
            )
        except BaseException:
            await ctx.send("```" + "Cache reset failed." + "```")

    # @meta.command(brief='Show Superuser')
    # async def superuser(self, ctx):
    #     """Show Super User Details"""
    #     superusers = os.getenv('SUPER_USERS')
    #     if not superusers:
    #         await ctx.send('Super Users not set')
    #         return
    #
    #     superusers = superusers.split(',')
    #
    #     await ctx.send("List of Superusers")
    #
    #     for id in


async def setup(bot):
    await bot.add_cog(Meta(bot))
