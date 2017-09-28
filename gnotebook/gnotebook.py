from cogs.utils.dataIO import dataIO
from time import gmtime, strftime
from cogs.utils import checks
import discord
from discord.ext import commands
import os
from __main__ import send_cmd_help
from cogs.utils.chat_formatting import pagify, box

class GNotebook:
    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/gnotebook/settings.json')

    @commands.group(pass_context=True)
    async def gnotebook(self, ctx):
        """Global Notebook"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @gnotebook.command(pass_context=True)
    async def new(self, ctx):
        """Global Notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if user.id not in self.settings:
            self.settings[user.id] = ":book: __**Started Global Notebook!**__ :book:" + "\n`{} - ".format(server.name) + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "`"
            dataIO.save_json("data/gnotebook/settings.json", self.settings)
            await self.bot.say("Global notebook created! :book:")
        else:
            await self.bot.say("Global notebook already exists. :book:")

    @gnotebook.command(pass_context=True)
    async def update(self, ctx, *, content):
        """Global Notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if user.id not in self.settings:
            await self.bot.say("Global notebook empty, please create one with `{}gnotebook new`.".format(ctx.prefix))
            return
        else:
            previous = self.settings[user.id]
            self.settings[user.id] = "{}\n".format(previous) + "\n**Entry:**\n" + content + "\n`{} - ".format(server.name) + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "`"
            dataIO.save_json("data/gnotebook/settings.json", self.settings)
            await self.bot.say("Content updated!")

    @gnotebook.command(pass_context=True)
    async def view(self, ctx):
        """Global Notebook"""
        user = ctx.message.author
        server = ctx.message.server
        if user.id not in self.settings:
            await self.bot.say("Global notebook empty, please create one with `{}gnotebook new`.".format(ctx.prefix))
            return
        else:
            content = self.settings[user.id]
            for page in pagify(content):
                await self.bot.say("Check your DMs :book:")
                await self.bot.whisper(page)

def check_folder():
    if not os.path.exists('data/gnotebook'):
        print('Creating data/gnotebook folder...')
        os.makedirs('data/gnotebook')

def check_file():
    data = {}
    if not dataIO.is_valid_json('data/gnotebook/settings.json'):
        print('Creating settings.json...')
        dataIO.save_json('data/gnotebook/settings.json', data)

def setup(bot):
    check_folder()
    check_file()
    cog = GNotebook(bot)
    bot.add_cog(cog)
