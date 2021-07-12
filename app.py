import click

from formatters import SimpleLogFormatter
from helpers import SimplePointsCalculator
from models import LogTable
from readers import InputReader, StandardInputReader, FileInputReader
from sorters import SimpleLogSorter


@click.command()
@click.option('-f', '--filename', help='Specify the file containing match results')
def app(
        filename: str
):
    try:
        reader: InputReader = FileInputReader(filename=filename, report_errors=True, ignore_errors=True) \
            if filename else StandardInputReader()

        LogTable \
            .from_(reader.read()) \
            .calculate_points(calculator=SimplePointsCalculator()) \
            .sorted(sorter=SimpleLogSorter()) \
            .format(formatter=SimpleLogFormatter(), print_=True)

    except ValueError as e:
        click.echo(click.style(f'Input error: "{str(e)}"', fg='red'))


if __name__ == '__main__':
    app()
