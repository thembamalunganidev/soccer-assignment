from typing import List


class LogSorter:
    def sort(self, class_: str, teams: List) -> List:
        raise NotImplementedError


class SimpleLogSorter(LogSorter):
    def __init__(self, order: str = 'desc', property_: str = 'points'):
        self.order = order
        self.property_ = property_

    def sort(self, class_, teams: List):
        if not hasattr(class_, self.property_):
            raise AttributeError(f'Invalid sorting property supplied: {self.property_}')

        reverse = True
        if self.order == 'asc':
            reverse = False
        return sorted(teams, key=lambda x: getattr(x, self.property_), reverse=reverse)
