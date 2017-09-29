import discord
from discord.ext import commands
import asyncio
import aiohttp
import json

class AltCoin:

    def __init__(self,bot):
        self.bot = bot
                
    @commands.command(pass_context=True, no_pm=True)
    async def altcoin(self, ctx, coin):
        """Altcoin stats"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.coinmarketcap.com/v1/ticker/' + coin) as resp:
                print(resp.status)
                yes = await resp.json()
                owo = str(yes)
                embed = discord.Embed(description=owo['name'], colour=discord.Colour.blue())
                embed.add_field(name="**Symbol:**",value=owo['symbol'])
                embed.add_field(name="**Rank:**",value=owo['rank'])
                embed.add_field(name="**Price(USD):**",value=owo['price_usd'])
                embed.add_field(name="**Price(BTC):**",value=owo['price_btc'])
                embed.add_field(name="**Market Cap Supply(USD):**",value=owo['market_cap_usd'])
                embed.add_field(name="**Percentage Change 1h:**",value=owo['percent_change_1h'])
                embed.add_field(name="**Percentage Change 24h:**",value=owo['percent_change_24h'])
                embed.add_field(name="**Percentage Change 7d:**",value=owo['percent_change_7d'])
                embed.set_thumbnail(url="http://www.iconarchive.com/download/i77833/custom-icon-design/pretty-office-11/coin-us-dollar.ico")
                await self.bot.say(embed=embed)

def setup(bot):
    n = AltCoin(bot)
    bot.add_cog(n)
