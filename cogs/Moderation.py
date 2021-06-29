import discord
from discord.ext import commands
list_of_muted_members = []
import asyncio


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member: discord.Member):
        if (member in list_of_muted_members):
            muterole = discord.utils.get(member.guild.roles, name = "Muted")
            await member.add_roles(muterole)
        else:
            embedVar = discord.Embed(title = 'Welcome To The Programming Done Right Discord Server', description = 'Read the rules carefully and react with a checkmark to get roles! We hope you enjoy your stay', color = 0x00ff00)
            await member.send(embed=embedVar)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        member = payload.member
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
        timeout_role = discord.utils.get(guild.roles, name = 'Muted')
        if timeout_role in member.roles:
           Title = 'You can not get your role back when you are muted'
           embedVar = discord.Embed(title=Title , description='', color=0x00ff00)
           await member.send(embed=embedVar)
        else:
           if message_id == 830936392724119582:

               if payload.emoji.name == 'checkmark':
                   member_role = discord.utils.get(guild.roles, name = 'Member')
                   await member.add_roles(member_role)
        
    @commands.command(pass_context=True, description='Purges the chat. Only Admins can use this command.')
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit = 10):
        await ctx.channel.purge(limit=limit)

    @commands.command(description='Ban a specified user. Only Admins can use this command.')
    @commands.has_permissions(ban_members = True)
    async def ban(self,ctx, member : discord.Member, *, reason = None):
        role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
        if (role in member.roles):
           embedVar = discord.Embed(title='You can not use that command!' , description='You do not have the permissions to use that command', color=0x00ff00)
           await ctx.send(embed=embedVar)

        else:
           await member.ban(reason = reason)
           embedVar = discord.Embed(title=f'{str(member)} Has been banned' , description='', color=0x00ff00)
           embedVar.add_field(name='Reason ', value=reason, inline=False)
           await ctx.send(embed=embedVar)
           await member.send('You have been banned from the programming done right server, submit you ban appeal at this link: https://forms.gle/JiXoo2BdthLUXePHA')

    @commands.command(description='Kicks a specified user. Only Admins can use this command.')
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
        if (role in member.roles):
           embedVar = discord.Embed(title='You can not use that command!' , description='You do not have the permissions to use that command', color=0x00ff00)
           await ctx.send(embed=embedVar)
        else:
           await member.kick(reason=reason)
           embedVar = discord.Embed(title=f'{str(member)} Has been kicked' , description='', color=0x00ff00)
           embedVar.add_field(name='Reason ', value=reason, inline=False)
           await ctx.send(embed=embedVar)


    @commands.command(description='Mutes the specified user. Only Moderators can use this command.')
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, hrs, mms, *, reason=None, ):
        guild = ctx.guild
        role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
        if (role in member.roles):
           embedVar = discord.Embed(title='You can not use that command!' , description='You do not have the permissions to use that command', color=0x00ff00)
           await ctx.send(embed=embedVar)
          
        else:
           mutedRole = discord.utils.get(guild.roles, name='Muted')
           memberRole = discord.utils.get(guild.roles, name='Member')
           embedVar = discord.Embed(title=f'{str(member)} Has been muted' , description='', color=0x00ff00)
           embedVar.add_field(name='Reason ', value=reason, inline=False)
           mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
           memberRole = discord.utils.get(guild.roles, name='Member')
           await member.add_roles(mutedRole, reason=reason)
           await member.remove_roles(memberRole)
           await ctx.send(embed=embedVar)
           await member.send(embed=embedVar)
           list_of_muted_members.append(member)
           time = 60*60*int(hrs)+60 * int(mms)
           await asyncio.sleep(time)
           embedVar = discord.Embed(title=f'{str(member)} Has been unmuted ' , description='', color=0x00ff00)
           mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
           memberRole = discord.utils.get(guild.roles, name='Member')
           await member.add_roles(memberRole)
           await member.remove_roles(mutedRole)
           await ctx.send(embed=embedVar)
           await member.send(embed=embedVar)
           list_of_muted_members.remove(member)
           

    @commands.command(description='Unmutes a specified user. Only Moderators can use this command.')
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        guild = ctx.guild
        role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
        if (role in member.roles):
           embedVar = discord.Embed(title='You can not use that command!' , description='You do not have the permissions to use that command', color=0x00ff00)
           await ctx.send(embed=embedVar)

        else:
           embedVar = discord.Embed(title=f'{str(member)} Has been unmuted ' , description='', color=0x00ff00)
           mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
           memberRole = discord.utils.get(guild.roles, name='Member')
           await member.add_roles(memberRole)
           await member.remove_roles(mutedRole)
           await ctx.send(embed=embedVar)
           await member.send(embed=embedVar)
           list_of_muted_members.remove(member)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
        if (role in member.roles):
           embedVar = discord.Embed(title='You can not use that command!' , description='You do not have the permissions to use that command', color=0x00ff00)
           await ctx.send(embed=embedVar)
          
        else:
           embedVar = discord.Embed(title=f'{str(member)} Has been warned ' , description='', color=0x00ff00)
           embedVar.add_field(name='Reason ', value=reason, inline=False)
           await ctx.send(embed=embedVar)
           await member.send(embed=embedVar)

    
    

def setup(bot):
    bot.add_cog(Moderation(bot))
    



