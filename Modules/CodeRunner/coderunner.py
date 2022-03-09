import sys
from io import StringIO
import contextlib


class CodeRunner:
    def __init__(self):
        pass

    def parse(self, message):
        message = message.content[8:]
        if message.startswith('help'):
            return self.helper_box()
        elif message.startswith('```') and message.endswith('```'):
            code = message[message.index("```") + 3:message.rindex("```")]
            return self.runPython(code)
        else:
            return "Invalid command"

    def runPython(self, code):
        with self.stdoutIO() as s:
            exec(code)
        return s.getvalue()

    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
