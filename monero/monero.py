import discord
from discord.ext import commands
import asyncio
import aiohttp
import json

class Monero:

    def __init__(self,bot):
        self.bot = bot
                
    @commands.command(pass_context=True, no_pm=True)
    async def coin(self, ctx, coin):
        """Altcoin stats"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.coinmarketcap.com/v1/ticker/' + id) as resp:
                print(resp.status)
                yes = await resp.json()
                embed = discord.Embed(description=yes['name'], colour=discord.Colour.blue())
                embed.add_field(name="**Symbol:**",value=yes['symbol'])
                embed.add_field(name="**Rank:**",value=yes['rank'])
                embed.add_field(name="**Price(USD):**",value=yes['price_usd'])
                embed.add_field(name="**Price(BTC):**",value=yes['price_btc'])
                embed.add_field(name="**Market Cap Supply(USD):**",value=yes['market_cap_usd'])
                embed.add_field(name="**Percentage Change 1h:**",value=yes['percent_change_1h'])
                embed.add_field(name="**Percentage Change 24h:**",value=yes['percent_change_24h'])
                embed.add_field(name="**Percentage Change 7d:**",value=yes['percent_change_7d'])
                embed.set_thumbnail(url="http://www.iconarchive.com/download/i77833/custom-icon-design/pretty-office-11/coin-us-dollar.ico")
                await self.bot.say(embed=embed)

def setup(bot):
    n = Monero(bot)
    bot.add_cog(n)
