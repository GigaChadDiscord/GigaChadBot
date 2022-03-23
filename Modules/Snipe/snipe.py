import logging
import sys
import json

logger = logging.getLogger('gigachad')


class Snipe:
    def __init__(self):
        logger.info('Snipe initialized')
        pass

    def prettify(self, output, total_time):
        return f"```py\n{output}\n```\n> Total time: {total_time:.2f}ms"

    def save(self, message, type_):
        if type_ == 'deleted':
            temp = json.loads(open('Temp/snipe.json', 'r').read())
            temp['deleted'] = message.content
            open('Temp/snipe.json', 'w').write(json.dumps(temp))
        elif type_ == 'edited':
            temp = json.loads(open('Temp/snipe.json', 'r').read())
            temp['edited'] = message.content
            open('Temp/snipe.json', 'w').write(json.dumps(temp))
