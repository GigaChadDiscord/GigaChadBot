# Main Discord Runner

import logging
import os
import sys
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Modules.Reddit.reddit import Reddit
from Modules.Gpay.gpay import Gpay
from Utils.Logger import startLogger
from Utils.dice import Dice, BooleanDice, ReplyDice
from Modules.Snipe.snipe import Snipe
import json
import argparse

startLogger('gigachad')
logger = logging.getLogger('gigachad')

# Init Modules
bot = commands.Bot(command_prefix="-")
code_runner = CodeRunner()
replier = Replier()

probability_reaction = 25
dice_reaction = ReplyDice(probability_reaction)
dice_reaction.add_reply("💀")


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    bot.add_cog(Reddit(bot))
    bot.add_cog(Gpay(bot))
    bot.add_cog(Snipe(bot))
    logger.info(f'{bot.user.name} is ready!')


@bot.event
async def on_message(message):
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
        Snipe.save(before, 'edited')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found bro, try `-help`")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Member not found bro")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"You are missing a required argument bro, try `-help {ctx.command.name}`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"You have entered an invalid argument bro, try `-help {ctx.command.name}`")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"You are on cooldown bro, try again in {error.retry_after:.2f} seconds")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command bro")
    else:
        logger.error(error)


@bot.command(
    name='python',
)
async def python_parsing(ctx):
    msg = code_runner.parse(ctx.message)
    if msg is not None and msg != "":
        await ctx.channel.send(msg)

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument("-t", "--test", help="Runs script using test bot token", action="store_true")
    args = parser.parse_args()
    if args.test:
        logger.info("Running in test mode")
        bot.run(os.getenv('DISCORD_TEST_TOKEN'))
    else:
        logger.info("Running in production mode")
        bot.run(os.getenv('DISCORD_TOKEN'))
