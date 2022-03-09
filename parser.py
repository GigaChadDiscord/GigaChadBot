import discord

from Modules.CodeRunner.coderunner import CodeRunner


class Parser:
    def __init__(self) -> None:
        pass

    def parse(self, message: discord.Message) -> str:
        cmd = message.content[1:]

        if cmd.startswith("python"):
            # ex: python ```print('hello world')```
            msg = CodeRunner(lang="python", code=cmd[cmd.index("```") + 3:cmd.rindex("```")]).run()
        print(msg)
        return msg
