import os
from discord.ext import commands
from dotenv import load_dotenv
import discord

class CI_notificator:
    def __init__(self):
        self.token = self.get_token()
        self.bot = self.setup()

    def setup(self):
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix="!", intents=intents)

        @bot.command()
        async def ping(ctx):
            print(ctx)
            await ctx.send('pong')
        
        return bot

    def get_token(self):
        load_dotenv("tokens.env")
        return os.getenv('DISCORD_BOT_TOKEN')

if __name__ == "__main__":
    notificator = CI_notificator()
    notificator.bot.run(notificator.token)