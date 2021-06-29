import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='>')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension[:-3]}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

token = os.environ.get('Token')
bot.run(token)
