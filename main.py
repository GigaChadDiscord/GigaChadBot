# Main Discord Runner

import os
import discord
from dotenv import load_dotenv
from Modules.CodeRunner.coderunner import CodeRunner
from Modules.QuizColab.quizcolab import QuizColab
from Modules.Replier.replier import Replier
from Modules.Snipe.snipe import Snipe

client = discord.Client()


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
            elif message.content.startswith('$snipe') or message.content.startswith('$editsnipe'):
                msg = Snipe().parse(message)
            # if message.content.startswith('$valo'):
            #     msg = Valorant(message).parse()
        else:
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
