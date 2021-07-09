from config import Config


class PointsCalculator:
    def calculate(self, team):
        raise NotImplementedError


class SimplePointsCalculator(PointsCalculator):
    def calculate(self, team):
        return (team.wins * Config.WIN_POINTS) + (team.draws * Config.DRAW_POINTS)
