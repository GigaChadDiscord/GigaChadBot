import sys
import json

class Snipe:
    def __init__(self):
        pass

    def snipe(self, message):
        if message.content.startswith('$snipe'):
            msg = message.content.split('$snipe')[1]
            # Get deleted message from Temp/snipe.json
            deletedMsg = json.loads(open('Temp/snipe.json', 'r').read())['deleted']
            return deletedMsg
        elif message.content.startswith('$editsnipe'):
            # Get edited message from Temp/snipe.json
            deletedMsg = json.loads(open('Temp/snipe.json', 'r').read())['edited']
            return deletedMsg
        else:
            print('Invalid Snipe command')

    def runPython(self, code):
        with self.stdoutIO() as s:
            start = time()
            exec(code)
            total_time = time() - start
        msg = self.prettify(s.getvalue(), total_time * 1000)
        return msg

    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old

    def prettify(self, output, total_time):
        return f"```py\n{output}\n```\n> Total time: {total_time:.2f}ms"

    def helper_box(self):
        return '''
        ```
        Use the command like:
        $python `​`​`print('Hello World') `​`​`
        ```
        '''
