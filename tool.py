from __future__ import annotations

import importlib.util
import typing
from pathlib import Path
from types import ModuleType

from executor import ShellCommander

if typing.TYPE_CHECKING:
    from executor import Commander


class Tool:
    def __init__(
        self,
        command: str,
        commander: Commander | None = None,
        opt_args: list | None = None,
    ) -> None:
        self.command = command
        self.commander = commander or ShellCommander
        self.opt_args = opt_args or []

    def _default_args(self) -> list:
        args = ["-y"]

        args.extend(self.opt_args)

        return args

    def resource(self, resource_name: str) -> ModuleType:
        commands_dir = Path(__file__).parent / "commands"
        modules = {
            f.stem: f.resolve() for f in commands_dir.iterdir() if f.stem != "__init__"
        }

        if resource_name not in modules:
            raise ValueError("Module %s not found", resource_name)

        spec = importlib.util.spec_from_file_location(
            resource_name, modules[resource_name]
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        command = module.Command()
        setattr(self, resource_name, command)
        command.run = self.run

        return getattr(self, resource_name)

    def run(self, args: str, process_input: str | bytes | None = None) -> dict:
        default = self._default_args()
        args = default + args

        return self.commander.run_args(self.command, args, process_input=process_input)
