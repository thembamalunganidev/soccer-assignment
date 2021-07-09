from typing import List


class LogFormatter:
    def format(self, teams: List) -> str:
        raise NotImplementedError


class SimpleLogFormatter(LogFormatter):
    def format(self, teams: List) -> str:
        res = ''
        for index, entry in enumerate(teams):
            res += f'{index + 1}: {entry.name}, {entry.points} pts\n'
        return res


class ComplexLogFormatter(LogFormatter):
    def format(self, teams: List) -> str:
        data = []
        for index, team in enumerate(teams):
            data.append([index + 1, team.name, team.played, team.wins, team.draws, team.losses, team.points])

        from tabulate import tabulate
        return tabulate(data, headers=['Position', 'Name', 'P', 'W', 'D', 'L', 'P'])
