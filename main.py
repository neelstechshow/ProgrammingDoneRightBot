import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import requests
import json
import random
import pyjokes
from discord.ext import tasks


list_of_muted_members = []
intents=intents=discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents )

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.wait_until_ready()
    my_background_task.start()


@tasks.loop(seconds=3600.0)
async def my_background_task():
    quote = get_quote()
    await bot.change_presence(activity = discord.Game(type = discord.ActivityType.watching, name = quote))

@bot.event
async def on_member_join(member: discord.Member):
    if (member in list_of_muted_members):
        muterole = discord.utils.get(member.guild.roles, name = "Muted")
        await member.add_roles(muterole)
    await member.send('Hello!! Welcome to the Programming Done Right discord server, read the rules carefully and react with a checkmark to get roles! We hope you enjoy your stay')


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    member = payload.member
    guild_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)
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
          

@bot.event
async def on_message_delete(message):
    Title = f'{str(message.author)} Deleted A Message In {str(message.channel)}'
    embedVar = discord.Embed(title=Title , description='', color=0x00ff00)
    embedVar.add_field(name='Deleted Message: ', value=message.content, inline=False)
    channel = bot.get_channel(847919803011170344)
    await channel.send(embed=embedVar)

@bot.event
async def on_message_edit(message_before, message_after):
    Title = f'{str(message_before.author)} Edited A Message In {str(message_before.channel)}'
    embedVar = discord.Embed(title=Title , description='', color=0x00ff00)
    embedVar.add_field(name='Before: ', value=message_before.content, inline=False)
    embedVar.add_field(name='After: ', value=message_after.content, inline=False)
    channel = bot.get_channel(847919803011170344)
    await channel.send(embed=embedVar)


@bot.command(aliases=['hi', 'hey', 'yello', 'ello'], description='Just sends hello')
async def hello(ctx):
    await ctx.send('Hello!')

@bot.command (description = 'Sends Pong!')
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command(description='Sends generic rules, for the full rules check #rules')
async def rules(ctx):
    await ctx.send('No racism, sexism, bullying ect. If you would like to self promote please use the self-promotion chat. Spamming will not be allowed.')

@bot.command(aliases=['8ball'], description='Acts as a virtual 8ball')
async def eightball(ctx, *, question = None):
    responses = ['nah', 'I dunno, why r u asking me?', 'Yeah ig',
                'YES DEFINITELY ANYONE WHO DISAGREES WILL FACE MY WRATH',
                'Probably not', 'yes?', 'I guess', 'who cares?', 'yea',
                'HAHA KEEP DREAMING']

    if(question == None):
       await ctx.send('You have to ask me a question...')
    else:
       await ctx.send(random.choice(responses))

@bot.command(description='Sends a random inspirational quote')
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@bot.command(aliases = ['roll'], description='Rolls a virtual dice')
async def dice (ctx):
    rating = random.randint(1, 6)
    await ctx.send(rating)

@bot.command(aliases=['laugh'], description='Tells a random joke')
async def joke(ctx):
    joke = pyjokes.get_joke(language='en', category='all')
    await ctx.send(joke)

@bot.command(description='Rates a specific thing')
async def rate(ctx, *, rated = None):   
    if(rated == None):
       await ctx.send('You have to ask me to rate something...')
    else:   
       percent = random.randint(0, 100)
       await ctx.send(f'{percent}%')

@bot.command(pass_context=True, description='Purges the chat. Only Admins can use this command.')
@commands.has_permissions(administrator=True)
async def clear(ctx, limit = 10):
    await ctx.channel.purge(limit=limit)

@bot.command(description='Ban a specified user. Only Admins can use this command.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
    if role in member.roles:
        embed = discord.Embed(title='Error',
                              description='You do not have the permissions (Ban Members) to use that command!',
                              color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        if reason is None:
            reason = 'No reason given'
        try:
            await member.ban(reason=reason)
        except:
            return await ctx.send(f'Unable to kick user {member}, does the bot have the correct permissions?')
        embedVar = discord.Embed(title=f'{str(member)} has been banned',
                                 description=f'Reason: {reason}', color=0x00ff00)
        await ctx.send(embed=embedVar)
        await member.send(
            f'You have been banned from {ctx.guild.name}, submit your ban appeal at this link: https://forms.gle/JiXoo2BdthLUXePHA')


@bot.command(description='Kicks a specified user. Only Admins can use this command.')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
    if role in member.roles:
        embed = discord.Embed(title='Error',
                              description='You do not have the permissions (Administrator) to use that command!',
                              color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        if reason is None:
            reason = 'No reason given'
        try:
            await member.kick(reason=reason)
        except  :
            return await ctx.send(f'Unable to kick user {member}, does the bot have the correct permissions?')
        embed = discord.Embed(title=f'{str(member)} Has been kicked',
                              description=f'Reason: {reason}', color=0x00ff00)
        await ctx.send(embed=embed)


@bot.command(description='Mutes the specified user. Only Moderators can use this command.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
    if role in member.roles:
        embedVar = discord.Embed(title='Error',
                                 description='You do not have the permissions (Manage Messages) to use that command!',
                                 color=0x00ff00)
        await ctx.send(embed=embedVar)

    else:
        if reason is None:
            reason = 'No reason given'
        embedVar = discord.Embed(title=f'Member {str(member)} has been muted',
                                 description=f'Reason: {reason}', color=0x00ff00)
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        memberRole = discord.utils.get(guild.roles, name='Member')
        await member.add_roles(mutedRole, reason=reason)
        await member.remove_roles(memberRole)
        await ctx.send(embed=embedVar)
        await member.send(embed=embedVar)
        list_of_muted_members.append(member)


@bot.command(description='Unmutes a specified user. Only Moderators can use this command.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
    if role in member.roles:
        embed = discord.Embed(title='Error',
                              description='You do not have the permissions (Manage Messages) to use that command!',
                              color=0x00ff00)
        await ctx.send(embed=embed)

    else:
        embedVar = discord.Embed(title=f'{str(member)} has been unmuted',
                                 description='', color=0x00ff00)
        mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
        memberRole = discord.utils.get(guild.roles, name='Member')
        await member.add_roles(memberRole)
        await member.remove_roles(mutedRole)
        await ctx.send(embed=embedVar)
        await member.send(embed=embedVar)
        list_of_muted_members.remove(member)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: str = None):
    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
    if role in member.roles:
        embed = discord.Embed(title='Error',
                              description='You do not have the permissions (Manage Messages) to use that command!',
                              color=0x00ff00)
        await ctx.send(embed=embed)

    else:
        if reason is None:
            reason = 'No reason given'
        embed = discord.Embed(title=f'Member {str(member)} has been warned',
                              description=f'Reason: {reason}', color=0x00ff00)
        await ctx.send(embed=embed)
        await member.send(embed=embed)


keep_alive()
token = os.environ.get('Token')
bot.run(token)
