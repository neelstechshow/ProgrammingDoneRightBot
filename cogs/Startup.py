import discord
from discord.ext import commands
import requests
import json
from discord.ext import tasks

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)

class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=3600.0)
    async def my_background_task(self):
        quote = get_quote()
        await self.bot.change_presence(activity = discord.Game(type = discord.ActivityType.watching, name = quote))

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.bot))
        await self.bot.wait_until_ready()
        self.my_background_task.start()

def setup(bot):
    bot.add_cog(Startup(bot))
