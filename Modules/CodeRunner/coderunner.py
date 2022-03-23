import sys
from io import StringIO
import contextlib
from time import time


class CodeRunner:
    def __init__(self):
        print('CodeRunner initialized')
        self.m_validArgs = ['--save', '--test', '--public', '--private']
        self.saves = {}

    def parse(self, message):
        # Remove "-python " from the message
        if message.content == '-python':
            return self.helper_box()
        # Process
        cmd = message.content.lstrip('-python ')
        print('{}'.format(cmd))
        args = self.getArgs(cmd)
        if not self.checkArgs(args):
            return 'Invalid arguments'

        code = cmd[cmd.index("```") + 3:cmd.rindex("```")]
        if '--save' in args:
            self.save(message, args, cmd)
        return self.runPython(code)

    def save(self, message, args, code):
        self.code[message.author.id] = {}
        self.code[message.author.id]['code'] = code
        self.code[message.author.id]['access'] = 'private' if '--private' in args else 'public'

    def getArgs(self, cmd: str):
        args = cmd[:min(cmd.index('\n'), cmd.index('```'))].split()
        print('args: {}'.format(args))
        if '--save' not in args and '--test' not in args:
            args.append('--save')
        if '--public' not in args and '--private' not in args:
            args.append('--public')
        return args

    def checkArgs(self, args):
        print(args)
        validArgsCheck = all(param in self.m_validArgs for param in args)
        testSaveCheck = False if '--save' in args and '--test' in args else True
        return validArgsCheck and testSaveCheck

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
        return f"```\n{output}\n```\n> Total time: {total_time:.2f}ms"

    def helper_box(self):
        return '''
        ```
        Use the command like:
        -python `​`​`print('Hello World') `​`​`
        ```
        '''
