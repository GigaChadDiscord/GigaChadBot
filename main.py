# Main Discord Runner

import os
import discord
from discord.utils import get
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Modules.Reddit.reddit import Reddit
from Modules.Gpay.gpay import Gpay
from Utils.dice import Dice, BooleanDice, ReplyDice
from Modules.Snipe.snipe import Snipe
import argparse

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
gpay = Gpay()

probability_reaction = 25
dice_reaction = ReplyDice(probability_reaction)
dice_reaction.add_reply("💀")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    msg = None
    print(f"{message.author.name} sent '{message.content}'")
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
            elif message.content.startswith('$gpay'):
                for user in message.mentions:
                    await user.avatar_url_as(static_format='png', size=256).save("Temp/gpay_receiver.png")
                msg = gpay.parse(message)
                
                if msg == "success":
                    await message.channel.send(file=discord.File('Temp/gpay_edited.png'))
                    msg = None
            # if message.content.startswith('$valo'):
            #     msg = Valorant(message).parse()
        else:
            emoji = dice_reaction.roll()
            if emoji:
                await message.add_reaction(emoji)
            msg = replier.parse(message)
            
        if msg is not None and msg != "":
            await message.channel.send(msg)


# Save deleted message in Temp/snipe.json
@client.event
async def on_message_delete(message):
    if message.author != client.user:
        snipe.save(message, 'deleted')

# Save edited message in Temp/snipe.json
@client.event
async def on_message_edit(before, after):
    if before.author != client.user:
        print(before.content)
        snipe.save(before, 'edited')

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument("-t", "--test", help="Runs script using test bot token", action="store_true")
    args = parser.parse_args()
    if args.test:
        print("Running in test mode")
        client.run(os.getenv('DISCORD_TEST_TOKEN'))
    else:
        print("Running in production mode")
        client.run(os.getenv('DISCORD_TOKEN'))
