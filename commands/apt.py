from __future__ import annotations

from commands import BaseCommand


class Command(BaseCommand):
    def install(self, package_name: str) -> dict:
        args = [
            "install",
            f"{package_name}",
        ]

        return self.run(args)
