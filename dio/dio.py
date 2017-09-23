import discord
from discord.ext import commands
import asyncio
from .utils import checks
import aiohttp

class Dio:

    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def dio(self, ctx, alias):
        """Discord.io Links"""
        inv = await self.bot.create_invite(ctx.message.server, unique=False)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.io/api?api=UfRAQCmVuCl9&url={}&custom='.format(inv) + alias + '&format=text') as resp:
                print(resp.status)
                try:
                    await self.bot.say(await resp.text())
                except discord.errors.HTTPException:
                    await self.bot.say("Link already exists, or the alias is reserved for Pro users.")

def setup(bot):
    n = Dio(bot)
    bot.add_cog(n)
