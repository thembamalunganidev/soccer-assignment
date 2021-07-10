import os.path
from typing import List

import click

from models import Result
from parsers import InputParser, SimpleInputParser


class InputReader:
    def file(self, filename: str) -> List[Result]:
        raise NotImplementedError

    def std(self) -> List[Result]:
        raise NotImplementedError


class SimpleInputReader(InputReader):
    def __init__(self, parser: InputParser = SimpleInputParser()):
        self.parser = parser

    def file(self, filename) -> List[Result]:
        if not os.path.isfile(filename):
            click.echo(click.style(f'File does not exist: {filename}', fg='red'))
            return None

        with open(filename, 'r') as file:
            results: List[Result] = []
            for index, line in enumerate(file.readlines()):
                try:
                    result = self.parser.parse(line)
                    results.append(result)
                except ValueError:
                    line = line.strip('\n')
                    click.echo(click.style(f'Invalid input a line {index + 1}: [{line}]', fg='red'))
                    continue
            return results

    def std(self) -> List[Result]:
        prompt = 'Reading from standard input. Please enter input and press enter\n' \
                 'Example: Lions 3, Snakes 2\n' \
                 'Enter "done" or "d" to finish input\n'

        click.echo(prompt)
        results: List[Result] = []

        while True:
            line = input()
            if not line:
                if click.confirm('Done entering results?'):
                    break
                else:
                    continue
            elif line.lower() == "done" or line.lower() == "d":
                break
            else:
                try:
                    result = self.parser.parse(line)
                    results.append(result)
                except ValueError:
                    click.echo(click.style("Invalid input. Please enter input in format: Lions 3, Snakes 2", fg="red"))
                    continue
        return results
