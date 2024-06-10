from .plugins import LogPlugin, BasePlugin, DynamicColorPlugin
from .utils import Prefix, Color, Bracket

from .time_prefix import TimePrefix
from .pigmento import Pigmento

pnt = pigmento = Pigmento()


def add_time_prefix(bracket=Bracket.DEFAULT, color=Color.GREEN):
    pnt.add_prefix(Prefix(TimePrefix(), bracket, color))


def add_log_plugin(log_file):
    pnt.add_plugin(LogPlugin(log_file))


def add_dynamic_color_plugin():
    pnt.add_plugin(DynamicColorPlugin(
        Color.MAGENTA, Color.BLUE, Color.RED, Color.YELLOW
    ))
