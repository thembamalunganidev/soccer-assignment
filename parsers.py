from models import Result


class InputParser:
    def parse(self, input_: str):
        raise NotImplementedError


class SimpleInputParser(InputParser):
    def parse(self, input_: str):
        input_segments = input_.split(',')

        if len(input_segments) != 2:
            raise ValueError('Invalid result input')

        team_a, team_b = [self._extract(x) for x in input_segments]
        return Result(team_a, team_b)

    @staticmethod
    def _extract(team_data):
        team_data = team_data.strip(' ').strip('\n').split(' ')
        return {
            'name': " ".join(team_data[:-1]),
            'score': int(team_data[-1])
        }
