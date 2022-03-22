# Main Discord Runner

import os
import discord
from discord.utils import get
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Modules.Reddit.reddit import Reddit
from Utils.dice import Dice, BooleanDice, ReplyDice
from Modules.Snipe.snipe import Snipe

client = discord.Client()
code_runner = CodeRunner()
replier = Replier()
quiz_colab = QuizColab()
reddit = None
try:
    reddit = Reddit()
except Exception as e:
    print(e)
snipe = Snipe()

probability_reaction = 25
dice_reaction = BooleanDice(probability_reaction)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author != client.user:
        if message.content.startswith('$'):
            if message.content.startswith('$python'):
                msg = code_runner.parse(message)
            elif message.content.startswith('$quiz'):
                msg = quiz_colab.parse(message)
            elif message.content.startswith('$snipe') or message.content.startswith('$editsnipe'):
                msg = snipe.parse(message)
            elif message.content.startswith('$meme'):
                msg = reddit.parse(message)
            # if message.content.startswith('$valo'):
            #     msg = Valorant(message).parse()
        else:
            if dice_reaction.roll():
                emoji = "💀"
                await message.add_reaction(emoji)
            msg = Replier().parse(message)
            
        if msg is not None:
            await message.channel.send(msg)


# Save deleted message in Temp/snipe.json
@client.event
async def on_message_delete(message):
    if message.author != client.user:
        Snipe().save(message, 'deleted')

# Save edited message in Temp/snipe.json
@client.event
async def on_message_edit(before, after):
    if before.author != client.user:
        print(before.content)
        Snipe().save(before, 'edited')
    
if __name__ == '__main__':
    load_dotenv()
    client.run(os.getenv('DISCORD_TOKEN'))
