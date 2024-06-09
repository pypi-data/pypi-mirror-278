import os

from typing import List
from vigor.utils import CommandRunner


class Compose(CommandRunner):
    def __init__(self, project_name: str):
        self.project_name = project_name

    def run(self, *args) -> str:
        """
        Runs commands using CommandRunner's run function.

        Project name is specified here so that every instance of Compose has the same name.
        Extension: Project directory could also be set here as well.

        Returns:
            str: _description_
        """
        params = ["docker", "compose", "-p", self.project_name]
        params.extend(args)

        process = super().run(*params, capture_output=True)
        return process.stdout

    def generate_compose_file(self, files: List[str], env: str=None) -> str:
        """
        Generates aggregated Compose file using Docker Compose's built-in config command.

        Args:
            files (List[str]): List of Docker Compose files (absolute path) to aggregate together.
            env (str, optional): Absolute path to aggregated env file. Defaults to None.

        Returns:
            str: Parsed and interpolated valid Compose file, in string.
        """
        params = []

        if env:
            if not os.path.isabs(env):
                raise ValueError("Environment file (.env) must be an Absolute Path!")

            params.append("--env-file")
            params.append(env)

        for file in files:
            if not os.path.isabs(file):
                raise ValueError("Compose files must be an Absolute Path!")

            params.append("--file")
            params.append(file)

        params.append("config")

        return self.run(*params)
