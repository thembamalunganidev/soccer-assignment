import os.path
from typing import List

import click

from models import Result
from parsers import InputParser, SimpleInputParser


class InputErrorHandler:
    def handle(self, error: str):
        raise NotImplementedError


class SimpleInputErrorHandler(InputErrorHandler):
    def __init__(self, ignore_errors: bool = True, report_errors: bool = True):
        self.ignore_errors = ignore_errors
        self.report_errors = report_errors

    def handle(self, error: str):
        if self.report_errors:
            click.echo(click.style(error, fg='red'))
        if not self.ignore_errors:
            raise ValueError(error)


class InputReader:
    def __init__(self, parser: InputParser = SimpleInputParser()):
        self.parser = parser

    def read(self) -> List[Result]:
        raise NotImplementedError


class FileInputReader(InputReader):
    def __init__(self,
                 filename: str,
                 parser: InputParser = SimpleInputParser(),
                 error_handler: InputErrorHandler = SimpleInputErrorHandler()
                 ):
        super(FileInputReader, self).__init__(parser=parser)
        self.filename = filename
        self.error_handler = error_handler

    def read(self) -> List[Result]:
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as file:
                results: List[Result] = []
                for index, line in enumerate(file.readlines()):
                    try:
                        result = self.parser.parse(line)
                        results.append(result)
                    except ValueError:
                        line = line.strip('\n')
                        error = f'Invalid input at line {index + 1}: [{line}]'
                        self.error_handler.handle(error=error)
                return results
        self.error_handler.handle(error=f'File does not exist: {self.filename}')


class StandardInputReader(InputReader):
    def __init__(self,
                 parser: InputParser = SimpleInputParser(),
                 error_handler: InputErrorHandler = SimpleInputErrorHandler()
                 ):
        super(StandardInputReader, self).__init__(parser=parser)
        self.error_handler = error_handler

    def read(self) -> List[Result]:
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
                    self.error_handler.handle(error='Invalid input. Please enter input in format: Lions 3, Snakes 2')
        return results
