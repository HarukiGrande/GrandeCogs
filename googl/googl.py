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

class GoogleUrlShortener:

    def __init__(self,bot):
        self.bot = bot
        self.apikey = "data/googl/api.json"
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
    async def googl(self, ctx):
        """Googl"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
        
    @googl.command(pass_context=True)
    @checks.is_owner()
    async def setkey(self, ctx, key):
        """Set api key
        
        DM the bot when doing this command."""
        if not await self.checkPM(ctx.message):
            return
        self.loadapi["ApiKey"] =  key
        await self.bot.say("Key updated!")

    @googl.command(pass_context=True, no_pm=True)
    async def shorten(self, ctx, url):
        """Shorten url"""
        key = self.loadapi["ApiKey"]
        shorten = 'https://www.googleapis.com/urlshortener/v1/url?key=' + key
        payload = {"longUrl": url}
        headers = {'content-type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.post(shorten,data=json.dumps(payload),headers=headers) as resp:
                print(resp.status)
                yes = await resp.json()
                await self.bot.say(yes['id'])
                
    @googl.command(pass_context=True, no_pm=True)
    async def expand(self, ctx, url):
        """Expand goo.gl url"""
        key = self.loadapi["ApiKey"]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.googleapis.com/urlshortener/v1/url?key=' + key + '&shortUrl=' + url) as resp:
                print(resp.status)
                yes = await resp.json()
                await self.bot.say(yes['longUrl'])
                
    @googl.command(pass_context=True, no_pm=True)
    async def analytics(self, ctx, url):
        """Analytics for url"""
        key = self.loadapi["ApiKey"]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.googleapis.com/urlshortener/v1/url?key=' + key + '&shortUrl=' + url + '&projection=FULL') as resp:
                print(resp.status)
                yes = await resp.json()
                embed = discord.Embed(colour=discord.Colour.blue())
                embed.add_field(name="**Shortened Url:**",value=yes['id'])
                embed.add_field(name="**Long Url:**",value=yes['longUrl'])
                embed.add_field(name="**Date Created:**",value=yes['created'])
                embed.add_field(name="**Clicks:**",value=yes['analytics']['allTime']['shortUrlClicks'])
                embed.set_image(url="https://www.ostraining.com/cdn/images/coding/google-url-shortener-tool.jpg")
                await self.bot.say(embed=embed)

def check_folder():
    if not os.path.exists("data/googl"):
        print("Creating data/account folder...")
        os.makedirs("data/googl")
        
def check_file():
    system = {"ApiKey": ""}
    f = "data/googl/api.json"
    if not dataIO.is_valid_json(f):
        print("Creating default api.json...")
        dataIO.save_json(f, system)
                
def setup(bot):
    check_folder()
    check_file()
    n = GoogleUrlShortener(bot)
    bot.add_cog(n)
