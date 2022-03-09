import sys
from io import StringIO
import contextlib


class CodeRunner:
    def __init__(self, lang, code):
        self.lang = lang
        self.code = code

    def run(self):
        if self.lang == "python":
            return self.runPython()
        else:
            return "Language not supported"

    def runPython(self):
        with self.stdoutIO() as s:
            exec(self.code)
        return s.getvalue()

    @contextlib.contextmanager
    def stdoutIO(self, stdout=None):
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
