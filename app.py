import click

from formatters import ComplexLogFormatter, SimpleLogFormatter
from models import LogTable
from readers import InputReader, SimpleInputReader


@click.command()
@click.option('-f', '--filename', help='Specify the file containing match results')
def run_app(
        filename: str,
        reader: InputReader = SimpleInputReader()
):
    input_ = reader.file(filename) if filename else reader.std()
    if input_:
        LogTable \
            .from_(input_) \
            .sorted() \
            .format(formatter=SimpleLogFormatter(), print_=True)


if __name__ == '__main__':
    run_app()
