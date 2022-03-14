import sys
from io import StringIO
import contextlib
from time import time


class CodeRunner:
    def __init__(self):
        pass

    def parse(self, message):
        message = message.content[8:]
        if message.startswith('help'):
            print('CodeRunner Help Module')
            return self.helper_box()
        elif message.startswith('```') and message.endswith('```'):
            print('CodeRunner runPython Module')
            code = message[message.index("```") + 3:message.rindex("```")]
            return self.runPython(code)
        else:
            return "Invalid command"

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
