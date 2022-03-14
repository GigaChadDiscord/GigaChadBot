# Main Discord Runner

import os
import discord
from discord.utils import get
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Utils.dice import Dice

client = discord.Client()

probability_reaction = 1
dice_reaction = Dice(probability_reaction)
dice_reaction.values = [1]


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
                msg = CodeRunner().parse(message)
            elif message.content.startswith('$quiz'):
                msg = QuizColab().parse(message)
            # if message.content.startswith('$valo'):
            #     msg = Valorant(message).parse()
        else:
            if dice_reaction.roll() == 1:
                emoji = get(client.get_all_emojis(), name='EmojiName')
                await client.add_reaction(message, emoji)
            msg = Replier().parse(message)
            
        if msg is not None:
            await message.channel.send(msg)

if __name__ == '__main__':
    load_dotenv()
    client.run(os.getenv('DISCORD_TOKEN'))
