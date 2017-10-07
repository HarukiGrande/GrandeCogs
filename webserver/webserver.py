from cogs.utils.dataIO import dataIO
from aiohttp import web
import datetime
import ipgetter
import os
from cogs.utils import checks
import discord
from discord.ext import commands
from __main__ import send_cmd_help

class webserver:
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.make_webserver())
        self.server = None
        self.app = web.Application()
        self.handler = None
        self.dispatcher = {}
        self.settings = dataIO.load_json('data/webserver/settings.json')
        self.ip = ipgetter.myip()
        
    @commands.command(pass_context=True)
    async def webserver(self, ctx):
        """Webserver"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @webserver.command(pass_context=True)
    async def link(self, ctx):
        """Link to webpage, use the permissions cog if you don't want the IP to be public when not using a reverse proxy."""
        if not self.settings['url'].startswith(tuple(['http://'])):
            await self.bot.say("http://{}".format(self.settings['url']))
        else:
            await self.bot.say("{}".format(self.settings['url']))

    @webserver.command(pass_context=True)
    @checks.is_owner()
    async def content(self, ctx, *, content):
        """Set webpage content, use HTML and CSS in a codeblock."""
        if content.startswith(tuple(['```html'])) and content.endswith(tuple(['```'])):
            self.settings['content'] = content[7:-3].strip("\n")
            dataIO.save_json("data/webserver/settings.json", self.settings)
            if not self.settings['url'].startswith(tuple(['http://'])):
                await self.bot.say("Content updated!\nhttp://{}".format(self.settings['url']))
            else:
                await self.bot.say("Content updated!\n{}".format(self.settings['url']))
        else:
            self.settings['content'] = content.strip("\n")
            dataIO.save_json("data/webserver/settings.json", self.settings)
            if not self.settings['url'].startswith(tuple(['http://'])):
                await self.bot.say("Content updated!\nhttp://{}".format(self.settings['url']))
            else:
                await self.bot.say("Content updated!\n{}".format(self.settings['url']))
    
    @webserver.command(pass_context=True)
    @checks.is_owner()
    async def url(self, ctx, url):
        """Change webserver url if reverse proxied."""
        self.settings['url'] = url
        dataIO.save_json("data/webserver/settings.json", self.settings)
        if not url.startswith(tuple(['http://'])):
            await self.bot.say("URL updated!\nhttp://{}".format(self.settings['url']))
        else:
            await self.bot.say("URL updated!\n{}".format(self.settings['url']))
        
    @webserver.command(pass_context=True)
    @checks.is_owner()
    async def port(self, ctx, port):
        """Change webserver port, remember to change DNS settings if using reverse proxied domain."""
        self.settings['server_port'] = port
        dataIO.save_json("data/webserver/settings.json", self.settings)
        await self.bot.say("Port updated!\n{}".format(self.settings['server_port']))

    async def make_webserver(self):

        async def page(request):
            body = self.settings['content']
            return web.Response(text=body, content_type='text/html')

        self.app.router.add_get('/', page)
        self.handler = self.app.make_handler()
        port = self.settings['server_port']
        self.server = await self.bot.loop.create_server(self.handler, '0.0.0.0', port)
        print('Serving webserver on {}:{}'.format(self.ip, port))

    async def get_owner(self):
        return await self.bot.get_user_info(self.bot.settings.owner)

    async def get_bot(self):
        return self.bot.user

    async def on_ready(self):
        message = 'Serving webserver on http://{}:{}'.format(self.ip, self.settings['server_port'])
        await self.bot.send_message(await self.get_owner(), message)

    def __unload(self):
        print('Closing webserver')
        self.server.close()
        self.bot.loop.run_until_complete(self.server.wait_closed())
        self.bot.loop.run_until_complete(self.app.shutdown())
        self.bot.loop.run_until_complete(self.handler.finish_connections(60.0))
        self.bot.loop.run_until_complete(self.app.cleanup())


def check_folder():
    if not os.path.exists('data/webserver'):
        print('Creating data/webserver folder...')
        os.makedirs('data/webserver')


def check_file():
    data = {}
    data['server_port'] = 8080
    data['content'] = "<center><h1>Haruki's WebServer cog for Red-DiscordBot</h1></center>"
    data['url'] = "{}:{}".format(ipgetter.myip(), data['server_port'])
    if not dataIO.is_valid_json('data/webserver/settings.json'):
        print('Creating settings.json...')
        dataIO.save_json('data/webserver/settings.json', data)


def setup(bot):
    check_folder()
    check_file()
    cog = webserver(bot)
    bot.add_cog(cog)
