import discord
from discord.ext import commands
import json
import requests
import random
import pyjokes

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hi', 'hey', 'yello', 'ello'], description='Just sends hello')
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command (description = 'Sends Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong!')


    @commands.command(description='Sends generic rules, for the full rules check #rules')
    async def rules(self, ctx):
        await ctx.send('No racism, sexism, bullying ect. If you would like to self promote please use the self-promotion chat. Spamming will not be allowed.')

    @commands.command(aliases=['8ball'], description='Acts as a virtual 8ball')
    async def eightball(self, ctx, *, question = None):
        responses = ['nah', 'I dunno, why r u asking me?', 'Yeah ig',
                    'YES DEFINITELY ANYONE WHO DISAGREES WILL FACE MY WRATH',
                    'Probably not', 'yes?', 'I guess', 'who cares?', 'yea',
                    'HAHA KEEP DREAMING']

        if(question == None):
           await ctx.send('You have to ask me a question...')
        else:
           await ctx.send(random.choice(responses))

    @commands.command(description='Sends a random inspirational quote')
    async def quote(self, ctx):
        quote = get_quote()
        await ctx.send(quote)

    @commands.command(aliases = ['roll'], description='Rolls a virtual dice')
    async def dice (self, ctx):
        rating = random.randint(1, 6)
        await ctx.send(rating)

    @commands.command(aliases=['laugh'], description='Tells a random joke')
    async def joke(self, ctx):
        joke = pyjokes.get_joke(language='en', category='all')
        await ctx.send(joke)

    @commands.command(description='Rates a specific thing')
    async def rate(self, ctx, *, rated = None):   
        if(rated == None):
           await ctx.send('You have to ask me to rate something...')
        else:   
           percent = random.randint(0, 100)
           await ctx.send(f'{percent}%')	

			

def setup(bot):
    bot.add_cog(FunCommands(bot))
