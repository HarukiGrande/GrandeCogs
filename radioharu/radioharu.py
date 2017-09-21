import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import send_cmd_help

class RadioHaru:
    """Radio Haru"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(pass_context=True, no_pm=True)
    async def radioharu(self, ctx):
        """Radio Haru"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @radioharu.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def play(self, ctx):
        """Play Radio Haru"""
        server = ctx.message.server
        author = ctx.message.author
        if self.voice_connected(server):
            await self.bot.say("Already connected to a voice channel, do `{}stop` to change radio.".format(ctx.prefix))
        else:
            voice_channel = author.voice_channel
            voice = await self.bot.join_voice_channel(voice_channel)
            player = voice.create_ffmpeg_player('http://stream.radioharu.pw/owo')
            player.start()
            await self.bot.say("**Playing Radio Haru!**")

    @radioharu.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(manage_server=True)
    async def stop(self, ctx):
        """Stop Radio Haru"""
        server = ctx.message.server
        await self._disconnect_voice_client(server)
        await self.bot.say("**Stopped playing Radio!**")
        
    def voice_client(self, server):
        return self.bot.voice_client_in(server)

    def voice_connected(self, server):
        if self.bot.is_voice_connected(server):
            return True
        return False

    async def _disconnect_voice_client(self, server):
        if not self.voice_connected(server):
            return

        voice_client = self.voice_client(server)

        await voice_client.disconnect()

def setup(bot):
    bot.add_cog(RadioHaru(bot))
