import discord
from discord.ext import commands
import bad_words
badWords = bad_words.bad_words()


class BadWordScanner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        for x in badWords:
            if x in msg:
                await message.delete()
                embedVar = discord.Embed(title=f'{message.author} Please do not use that language' , description='Your message has been deleted due to foul language', color=0x00ff00)
                await message.channel.send(embed=embedVar)
    

def setup(bot):
    bot.add_cog(BadWordScanner(bot))
