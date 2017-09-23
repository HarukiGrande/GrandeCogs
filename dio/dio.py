import discord
from discord.ext import commands
import asyncio
from .utils import checks
import aiohttp
import json
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
import os
from .utils.chat_formatting import *

class Dio:

    def __init__(self,bot):
        self.bot = bot
        self.apikey = "data/dio/api.json"
        self.loadapi = dataIO.load_json(self.apikey)
    
    async def checkPM(self, message):
        # Checks if we're talking in PM, and if not - outputs an error
        if message.channel.is_private:
            # PM
            return True
        else:
            # Not in PM
            await self.bot.send_message(message.channel, 'DM the bot this command.')
            return False
        
    @commands.group(pass_context=True)
    async def dio(self, ctx):
        """Discord.io"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
    
    @dio.command(pass_context=True)
    async def setkey(self, ctx, key):
        """Set api key
        
        DM the bot when doing this command."""
        if not await self.checkPM(ctx.message):
            return
        self.loadapi["ApiKey"] =  key
        await self.bot.say("Key updated!")

    @dio.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def alias(self, ctx, alias):
        """Create D.io link"""
        key = self.loadapi["ApiKey"]
        inv = await self.bot.create_invite(ctx.message.server, unique=False)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.io/api?api={0}&url={1}'.format(key, inv) + "&custom=" + alias + '&format=text') as resp:
                print(resp.status)
                try:
                    await self.bot.say(await resp.text())
                except discord.errors.HTTPException:
                    await self.bot.say("Link already exists, or the alias is reserved for Pro users.")
                    
def check_folder():
    if not os.path.exists("data/dio"):
        print("Creating data/account folder...")
        os.makedirs("data/dio")
        
def check_file():
    system = {"ApiKey": ""}
    f = "data/dio/api.json"
    if not dataIO.is_valid_json(f):
        print("Creating default api.json...")
        dataIO.save_json(f, system)

def setup(bot):
    n = Dio(bot)
    bot.add_cog(n)
