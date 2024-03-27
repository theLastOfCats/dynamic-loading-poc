from abc import ABCMeta


class BaseCommand(metaclass=ABCMeta):
    def run(self, args: list, process_input: str | bytes | None = None) -> dict: ...
