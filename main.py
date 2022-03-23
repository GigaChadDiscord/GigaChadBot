# Main Discord Runner

import os
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Modules.Reddit.reddit import Reddit
from Modules.Gpay.gpay import Gpay
from Utils.dice import Dice, BooleanDice, ReplyDice
from Modules.Snipe.snipe import Snipe
import json
import argparse

bot = commands.Bot(command_prefix="-")
code_runner = CodeRunner()
replier = Replier()
quiz_colab = QuizColab()
reddit = None
try:
    reddit = Reddit()
except Exception as e:
    print(e)
gpay = Gpay()

probability_reaction = 25
dice_reaction = ReplyDice(probability_reaction)
dice_reaction.add_reply("💀")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    print(f"{message.author.name} sent '{message.content}'")
    ctx = await bot.get_context(message)
    if ctx.valid:
        await bot.process_commands(message)
    else:
        msg = None
        if message.author != bot.user:
            emoji = dice_reaction.roll()
            if emoji:
                await message.add_reaction(emoji)
            msg = replier.parse(message)
        if msg is not None and msg != "":
            await message.channel.send(msg)


# Save deleted message in Temp/snipe.json
@bot.event
async def on_message_delete(message):
    if message.author != bot.user:
        Snipe.save(message, 'deleted')

# Save edited message in Temp/snipe.json


@bot.event
async def on_message_edit(before, after):
    if before.author != bot.user:
        print(before.content)
        Snipe.save(before, 'edited')


@bot.command(
    name='python',
)
async def python_parsing(ctx):
    msg = code_runner.parse(ctx.message)
    if msg is not None and msg != "":
        await ctx.channel.send(msg)


@bot.command(
    name='quiz',
)
async def quiz_parsing(ctx):
    msg = quiz_colab.parse(ctx.message)
    if msg is not None and msg != "":
        await ctx.channel.send(msg)


@bot.command(
    name='snipe',
)
async def snipe_parsing(ctx):
    msg = json.loads(open('Temp/snipe.json', 'r').read())['deleted']
    if msg is not None and msg != "":
        await ctx.channel.send(msg)


@bot.command(
    name='editsnipe',
)
async def editsnipe_parsing(ctx):
    msg = json.loads(open('Temp/snipe.json', 'r').read())['edited']
    if msg is not None and msg != "":
        await ctx.channel.send(msg)


@bot.command(
    name='reddit',
)
async def reddit_parsing(ctx):
    msg = reddit.parse(ctx.message)
    if msg is not None and msg != "":
        await ctx.channel.send(msg)


@bot.command(
    name='gpay',
)
async def gpay_parsing(ctx):
    for user in ctx.message.mentions:
        await user.avatar_url_as(static_format='png', size=256).save("Temp/gpay_receiver.png")
    msg = gpay.parse(ctx.message)
    if msg == "success":
        await ctx.channel.send(file=discord.File('Temp/gpay_edited.png'))
    else:
        await ctx.channel.send(msg)

# @bot.command(
#     name='valo',
# )
# async def valo_parsing(ctx):
#     msg = Valorant(ctx).parse()
#     if msg is not None and msg != "":
#         await ctx.channel.send(msg)

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument("-t", "--test", help="Runs script using test bot token", action="store_true")
    args = parser.parse_args()
    if args.test:
        print("Running in test mode")
        bot.run(os.getenv('DISCORD_TEST_TOKEN'))
    else:
        print("Running in production mode")
        bot.run(os.getenv('DISCORD_TOKEN'))
