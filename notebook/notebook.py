from cogs.utils.dataIO import dataIO
from time import gmtime, strftime
from cogs.utils import checks
import discord
from discord.ext import commands
import os
from __main__ import send_cmd_help
from cogs.utils.chat_formatting import pagify, box

class Notebook:
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/notebook/settings.json')
        
    @commands.group(pass_context=True)
    async def notebook(self, ctx):
        """Notebook"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @notebook.command(pass_context=True)
    async def new(self, ctx):
        """Create new guild notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if server.id not in self.settings:
            self.settings[server.id] = {}
            self.settings[server.id][user.id] = ":book: __**Started {} Notebook!**__ :book:".format(server.name) + "\n`" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "`"
            dataIO.save_json("data/notebook/settings.json", self.settings)
            await self.bot.say("Notebook created for this guild! :book:")
        else:
            await self.bot.say("Notebook already exists. :book:")

    @notebook.command(pass_context=True)
    async def update(self, ctx, *, content):
        """Update guild notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.say("Notebook empty for this guild, please create one with `{}notebook new`.".format(ctx.prefix))
            return
        else:
            previous = self.settings[server.id][user.id]
            self.settings[server.id][user.id] = "{}\n".format(previous) + "\n**Entry:**\n" + content + "\n`" + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "`"
            dataIO.save_json("data/notebook/settings.json", self.settings)
            await self.bot.say("Content updated!")

    @notebook.command(pass_context=True)
    async def view(self, ctx):
        """View guild notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if server.id not in self.settings:
            await self.bot.say("Notebook empty for this guild, please create one with `{}notebook new`.".format(ctx.prefix))
            return
        else:
            content = self.settings[server.id][user.id]
            for page in pagify(content):
                await self.bot.say("Check your DMs :book:")
                await self.bot.whisper(page)

def check_folder():
    if not os.path.exists('data/notebook'):
        print('Creating data/notebook folder...')
        os.makedirs('data/notebook')

def check_file():
    data = {}
    if not dataIO.is_valid_json('data/notebook/settings.json'):
        print('Creating settings.json...')
        dataIO.save_json('data/notebook/settings.json', data)

def setup(bot):
    check_folder()
    check_file()
    cog = Notebook(bot)
    bot.add_cog(cog)
