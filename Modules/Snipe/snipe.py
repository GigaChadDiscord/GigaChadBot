import sys
import json

class Snipe:
    def __init__(self):
        print('Snipe initialized')
        pass

    # def parse(self, message):
    #     if message.content.startswith('$snipe'):
    #         # Get deleted message from Temp/snipe.json
    #         deletedMsg = json.loads(open('Temp/snipe.json', 'r').read())['deleted']
    #         return deletedMsg
    #     elif message.content.startswith('$editsnipe'):
    #         # Get edited message from Temp/snipe.json
    #         editedMsg = json.loads(open('Temp/snipe.json', 'r').read())['edited']
    #         return editedMsg
    #     else:
    #         print('Invalid Snipe command')

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

    def helper_box(self):
        return '''
        ```
        Use the command like:
        $python `​`​`print('Hello World') `​`​`
        ```
        '''
