import discord
from discord.ext import commands

class MessageLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embedVar = discord.Embed(title=f'{str(message.author)} Deleted A Message In {str(message.channel)}' , description='', color=0xff0000)
        embedVar.add_field(name='Deleted Message: ', value=message.content, inline=False)
        channel = self.bot.get_channel(847919803011170344)
        await channel.send(embed=embedVar)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        embedVar = discord.Embed(title=f'{str(message_before.author)} Edited A Message In {str(message_before.channel)}' , description='', color=0x00ff00)
        embedVar.add_field(name='Before: ', value=message_before.content, inline=False)
        embedVar.add_field(name='After: ', value=message_after.content, inline=False)
        channel = self.bot.get_channel(847919803011170344)
        await channel.send(embed=embedVar)



def setup(bot):
    bot.add_cog(MessageLogs(bot))
