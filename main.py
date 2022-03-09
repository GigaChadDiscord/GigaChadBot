# Main Discord Runner

import os
import discord
from dotenv import load_dotenv

from parser import Parser

from Modules.Replier.replier import Replier

client = discord.Client()
parser = Parser()


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
            msg = parser.parse(message)
            await message.channel.send(msg)
        else:
            msg = Replier(message.content).run()
            if msg is not None:
                await message.channel.send(msg)

if __name__ == '__main__':
    load_dotenv()
    client.run(os.getenv('DISCORD_TOKEN'))
