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
        reader: InputReader = SimpleInputReader(report_errors=True, ignore_errors=False)
):
    try:
        input_ = reader.file(filename) if filename else reader.std()
        LogTable \
            .from_(input_) \
            .calculate_points(calculator=SimplePointsCalculator()) \
            .sorted(sorter=SimpleLogSorter()) \
            .format(formatter=SimpleLogFormatter(), print_=True)

    except ValueError as e:
        click.echo(click.style(f'Input error: "{str(e)}"', fg='red'))


if __name__ == '__main__':
    run_app()
