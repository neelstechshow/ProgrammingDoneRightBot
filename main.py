import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='>', intents=intents )

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension[:-3]}')


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
token = os.environ.get('Token')
bot.run(token)
