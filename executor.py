from __future__ import annotations

import shlex
import subprocess
import typing
from functools import partial


class ExecutorClass(typing.Protocol):
    def __call__(
        self, command: str, *args: typing.Any, **kwargs: typing.Any
    ) -> typing.Any: ...


class Executor(typing.Protocol):
    executor: ExecutorClass
    errors_list: typing.Iterable[type[BaseException]]

    @classmethod
    def format(cls, command: str, args: list) -> str:
        return shlex.join([command, *args])

    @classmethod
    def execute(
        cls, command: str, *args, process_input: str | bytes | None = None
    ) -> dict:
        return cls.executor(cls.format(command, *args), input=process_input)


class ShellExecutor(Executor):
    executor = partial(
        subprocess.run,
        shell=True,
        check=True,
        encoding="UTF-8",
        capture_output=True,
    )
    errors_list = (subprocess.CalledProcessError,)

    @classmethod
    def execute(
        cls, command: str, args: list, process_input: str | bytes | None = None
    ) -> dict:
        try:
            result = cls.executor(cls.format(command, args), input=process_input)

            return {
                "result": result.stdout,
                "error_info": result.stderr,
            }
        except cls.errors_list as error:
            error_message = f"""
                Code: {error.returncode}
                Command: {error.cmd}
                Output: {error.stdout}
                Info: {error.stderr}
            """
            raise ValueError(error_message) from None


class Commander(typing.Protocol):
    executor: Executor

    @classmethod
    def run_args(
        cls, command: str, args: list, process_input: str | bytes | None = None
    ) -> dict:
        return cls.executor.execute(command, args, process_input=process_input)


class ShellCommander(Commander):
    executor = ShellExecutor
