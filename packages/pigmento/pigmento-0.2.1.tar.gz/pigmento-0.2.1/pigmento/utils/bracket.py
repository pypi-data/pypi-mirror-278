from enum import Enum


class Bracket(Enum):
    DEFAULT = ('[', ']')
    CLASS = '|'
    METHOD = ('(', ')')

    @classmethod
    def format(cls, bracket):
        if bracket is None:
            bracket = cls.DEFAULT.value

        if isinstance(bracket, cls):
            bracket = bracket.value

        for b in cls:
            value = b.value
            if isinstance(value, str):
                value = (value, value)

            if bracket in value:
                return value[0] + '%s' + value[1]

        if isinstance(bracket, str):
            return bracket + '%s' + bracket

        assert isinstance(bracket, tuple) or isinstance(bracket, list), 'bracket should be str, tuple or list'
        assert len(bracket) == 2, 'tuple or list bracket should have length 2'

        return bracket[0] + '%s' + bracket[1]
