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
    def __init__(self,
                 parser: InputParser = SimpleInputParser(),
                 ignore_errors: bool = True,
                 report_errors: bool = True
                 ):
        self.parser = parser
        self.report_errors = report_errors
        self.ignore_errors = ignore_errors

    def file(self, filename) -> List[Result]:
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                results: List[Result] = []
                for index, line in enumerate(file.readlines()):
                    try:
                        result = self.parser.parse(line)
                        results.append(result)
                    except ValueError:
                        line = line.strip('\n')
                        error = f'Invalid input at line {index + 1}: [{line}]'
                        self._handle_error(error)
                return results

        error = f'File does not exist: {filename}'
        self._handle_error(error=error)

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
                    error = "Invalid input. Please enter input in format: Lions 3, Snakes 2"
                    self._handle_error(error=error)
        return results

    def _handle_error(self, error):
        if self.report_errors:
            click.echo(click.style(error, fg='red'))
        if not self.ignore_errors:
            raise ValueError(error)
