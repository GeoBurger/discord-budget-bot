import discord
from discord.ext import commands
import json
from budget_class import Budget
from datetime import datetime, timedelta


class BudgetBot:
    def __init__(self):
        # Load the configuration from the config.json file
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)

        self.BOT_TOKEN = config["token"]
        self.CHANNEL_ID = config["channel_id"]

        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.register_events_and_commands()

        self.budget_obj = None


    def register_events_and_commands(self):

        # Register bot events
        @self.bot.event
        async def on_ready():
            channel = self.bot.get_channel(self.CHANNEL_ID)
            await channel.send('Hello! The budget bot is ready. Currently no budget')

        # Register bot commands
        @self.bot.command()
        async def help_b(ctx):
            await ctx.send("""
            List of commands:

            VIEW COMMANDS:
            !left - Check how much is left in the budget
            !days - View how many days till the budget ends

            SPEND COMMANDS:
            !spend ### - Subtract that amount from the budget
            !refund ### - Add that amount back to the budget
            """)

        @self.bot.command()
        async def create(ctx, budget_amount, lenth=0, override=""):
            if self.budget_obj and override.lower() != 'override': # if there is and object and your not asking to over-ride throw an issue, if there is not object or you are asking to over-ride then make a new one
                await ctx.send(f"There is already a budget created. Please send the command with override as third arg to make a new budget")

            else:
                if lenth:
                    end_date = (datetime.now() + timedelta(days=lenth)).date()
                    self.budget_obj = Budget('food', float(budget_amount), end_date)
                    await ctx.send(f"Budget created with amount {budget_amount} and end date {end_date}.")

                else:
                    await ctx.send('Please specify either a length.')

        @self.bot.command()
        async def spend(ctx, amount):
            if self.budget_obj:
                self.budget_obj.spend(amount)
                budget_left = self.budget_obj.remaining_amount
                await ctx.send(f'Spent ${amount}, there is ${budget_left} left')
            else:
                await ctx.send('There is no budget set up please make a new budget')

        @self.bot.command()
        async def refund(ctx, amount):
            if self.budget_obj:
                self.budget_obj.refund(amount)
                budget_left = self.budget_obj.remaining_amount
                await ctx.send(f'Refunded ${amount}, there is now ${budget_left} left')
            else:
                await ctx.send('There is no budget set up please make a new budget')

        @self.bot.command()
        async def rate(ctx):
            if self.budget_obj:
                spend_rate = self.budget_obj.get_spend_rate()
                await ctx.send(f'{spend_rate}')
            else:
                await ctx.send('There is no budget set up please make a new budget')


    def run(self):
        self.bot.run(self.BOT_TOKEN)


if __name__ == "__main__":
    bot_instance = BudgetBot()
    bot_instance.run()
