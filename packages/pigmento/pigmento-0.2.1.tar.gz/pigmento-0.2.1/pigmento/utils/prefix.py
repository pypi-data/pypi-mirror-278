import termcolor

from .bracket import Bracket
from .color import Color


class Prefix:
    def __init__(self, text, bracket=None, color: Color = None):
        self.text = text
        self.bracket = Bracket.format(bracket)
        self.color = color

        if self.color is not None:
            assert self.color in Color, f'color should be one of {Color}'

    def __eq__(self, other: 'Prefix'):
        if not isinstance(other, Prefix):
            return False
        return self.text == other.text and self.bracket == other.bracket and self.color == other.color

    def with_color(self):
        return termcolor.colored(str(self), self.color and self.color.value)

    def __str__(self):
        text = self.text() if callable(self.text) else self.text
        return self.bracket % text

    def __repr__(self):
        return str(self)
