from typing import List

from config import Config
from formatters import LogFormatter, SimpleLogFormatter
from helpers import PointsCalculator, SimplePointsCalculator
from sorters import SimpleLogSorter, LogSorter


class Result:
    team_a: {}
    team_b: {}

    def __init__(self, team_a: str, team_b: str):
        self.team_a = team_a
        self.team_b = team_b

    def __repr__(self):
        return f'{self.team_a["name"]} {self.team_a["score"]} - {self.team_b["name"]} {self.team_b["score"]}'

    def is_win(self, team) -> bool:
        if getattr(self, 'team_a')['name'] == team:
            return self.team_a['score'] > self.team_b['score']
        elif getattr(self, 'team_b')['name'] == team:
            return self.team_b['score'] > self.team_a['score']
        return False

    def is_draw(self):
        return self.team_a['score'] == self.team_b['score']


class Team:
    name: str = ''
    played: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    points: int = 0

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'{self.name} {self.points}'

    def update(self, result: Result) -> 'Team':
        self.played += 1
        if result.is_win(self.name):
            self.wins += 1
        elif result.is_draw():
            self.draws += 1
        else:
            self.losses += 1
        return self


class LogTable:
    def __init__(self):
        self.teams: List[Team] = []

    def get_team(self, name: str) -> Team:
        for team_ in self.teams:
            if team_.name == name:
                return team_
        return Team(name)

    def update(self, teams: List[Team]) -> None:
        for team_ in teams:
            if len(self.teams) > 0:
                found = False
                for _index, entry_ in enumerate(self.teams):
                    if entry_.name.strip() == team_.name.strip():
                        self.teams.pop(_index)
                        self.teams.insert(_index, team_)
                        found = True
                        break
                if not found:
                    self.teams.append(team_)
            else:
                self.teams.insert(0, team_)

    @classmethod
    def from_(cls, results: List[Result]) -> 'LogTable':
        log = LogTable()
        for result in results:
            log._process(result)
        return log

    def calculate_points(self, calculator: PointsCalculator = SimplePointsCalculator()):
        to_update = []
        for team in self.teams:
            team.points = calculator.calculate(team)
            to_update.append(team)
        self.update(to_update)
        return self

    def _process(self, result):
        team_a: Team = self.get_team(result.team_a['name'])
        team_b: Team = self.get_team(result.team_b['name'])
        self.update([team_a.update(result), team_b.update(result)])

    def sorted(self, sorter: LogSorter = SimpleLogSorter()) -> 'LogTable':
        self.teams = sorter.sort(Team, self.teams)
        return self

    def format(self, formatter: LogFormatter = SimpleLogFormatter(), print_: bool = True) -> str:
        formatted = formatter.format(self.teams)
        if print_:
            print('\n')
            print(formatted.strip(), '\n')
        return formatted
