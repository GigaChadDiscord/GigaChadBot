import sys
import json
import discord
from discord.ext import commands
import logging

logger = logging.getLogger('gigachad')

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.info("Reddit initialized")

    @commands.command(
        name='snipe',
        help='Gets the latest deleted message'
    )
    async def snipe(self, ctx):
        msg = json.loads(open('Temp/snipe.json', 'r').read())['deleted']
        if msg is not None and msg != "":
            await ctx.send(msg)
    
    @commands.command(
        name='editsnipe',
        help='Gets the latest edited message'
    )
    async def editsnipe(self, ctx):
        msg = json.loads(open('Temp/snipe.json', 'r').read())['edited']
        if msg is not None and msg != "":
            await ctx.send(msg)

    def prettify(output, total_time):
        return f"```py\n{output}\n```\n> Total time: {total_time:.2f}ms"
    
    def save(message, type_):
        if type_ == 'deleted':
            temp = json.loads(open('Temp/snipe.json', 'r').read())
            temp['deleted'] = message.content
            open('Temp/snipe.json', 'w').write(json.dumps(temp))
        elif type_ == 'edited':
            temp = json.loads(open('Temp/snipe.json', 'r').read())
            temp['edited'] = message.content
            open('Temp/snipe.json', 'w').write(json.dumps(temp))

    # def helper_box():
    #     return '''
    #     ```
    #     Use the command like:
    #     $python `​`​`print('Hello World') `​`​`
    #     ```
    #     '''
