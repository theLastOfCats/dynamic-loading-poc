from __future__ import annotations

import typing

from tool import Tool

if typing.TYPE_CHECKING:
    from commands.install import Command as InstallCommand

tool = Tool(command="apt")
command: InstallCommand = tool.resource("install")
result = command.install("vim")

print(result)
