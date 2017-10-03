import os
import discord
from discord.ext import commands
from .utils import checks
import asyncio
try:
    from chatterbot import ChatBot
    module_avail = True
except ImportError:
    module_avail = False
from chatterbot.trainers import ChatterBotCorpusTrainer

class ChatBot:
    """Chat"""

    def __init__(self, bot):
        self.bot = bot
        self.chatbot = ChatBot('Chatterbot', storage_adapter='chatterbot.storage.SQLStorageAdapter', logic_adapters=[
        "chatterbot.logic.BestMatch", 
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        ],
        database='/data/chatbot/database.sqlite3'
        )
        self.chatbot.set_trainer(ChatterBotCorpusTrainer) 
        self.chatbot.train("chatterbot.corpus.english.greetings", "chatterbot.corpus.english.conversations", "chatterbot.corpus.english.trivia", "chatterbot.corpus.english",)

    @commands.command(pass_context=True, invoke_without_command=True)
    async def chat(self, ctx, *, message):
        """Chat with me, I learn!!"""
        
        await self.bot.say(self.chatbot.get_response(message))

def check_folders():
    if not os.path.exists("data/chatbot"):
        print("Creating data/chatbot folder...")
        os.makedirs("data/chatbot")

def setup(bot):
    check_folders()
    if module_avail == True:
        bot.add_cog(ChatBot(bot))
    else:
        raise RuntimeError("You need to run `pip3 install chatterbot`")
