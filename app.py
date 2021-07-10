import click

from formatters import SimpleLogFormatter
from helpers import SimplePointsCalculator
from models import LogTable
from readers import InputReader, SimpleInputReader
from sorters import SimpleLogSorter


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
            .calculate_points(calculator=SimplePointsCalculator()) \
            .sorted(sorter=SimpleLogSorter()) \
            .format(formatter=SimpleLogFormatter(), print_=True)
    else:
        click.echo('No input entered. Aborting!')


if __name__ == '__main__':
    run_app()
