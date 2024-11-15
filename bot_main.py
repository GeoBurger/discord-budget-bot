import discord
from discord.ext import commands
import json


class BudgetBot:
    def __init__(self):

        # Load the configuration from the config.json file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        self.BOT_TOKEN = config["token"]
        self.CHANNEL_ID = config["channel_id"]

        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @bot.event
    async def on_ready(self):
        channel = self.bot.get_channel(self.CHANNEL_ID)
        await channel.send('Hello! The budget bot is ready')

    @bot.command()
    async def help_b(self,ctx):
        await ctx.send()

        # await ctx.send("""List of commands:
        #             \nSET UP COMMANDS
        #             \n!set_budget lets you define how much money is in the budget
        #             \n!set_length lets you set how many days are in that budget
        #             \n!set_auto_renew lets you turn auto renew on and off
        #             \n
        #             \nVIEW Commands
        #             \n!left tells you how much is left in the budget
        #             \n!table isn't set up yet
        #             \n!days tells you how many days till the budget ends
        #             \n
        #             \nSpend Commands
        #             \n!spend ### type !spend followed by a number to subtract that much from the budget
        #             \n!refund ### lets you put that much money back in the budget""")

    bot.run(BOT_TOKEN)

