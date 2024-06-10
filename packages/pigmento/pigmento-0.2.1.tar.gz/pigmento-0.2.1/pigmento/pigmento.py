import inspect
from typing import List

from .plugins.base_plugin import BasePlugin
from .utils.bracket import Bracket
from .utils.color import Color
from .utils.prefix import Prefix


class Pigmento:
    METHOD_BRACKET = Bracket.METHOD
    METHOD_COLOR = Color.CYAN

    CLASS_BRACKET = Bracket.CLASS
    CLASS_COLOR = Color.MAGENTA

    def __init__(self):
        self._prefixes = []  # type: List[Prefix]
        self._plugins = []  # type: List[BasePlugin]

        self._display_method_name = True
        self._display_class_name = True

        self._basic_printer = self._get_basic_printer()

    def add_prefix(self, prefix: Prefix):
        self._prefixes.append(prefix)

    def add_plugin(self, plugin: BasePlugin):
        plugin.init(self)
        self._plugins.append(plugin)

    def set_display_mode(self, display_method_name: bool = None, display_class_name: bool = None):
        if display_method_name is not None:
            self._display_method_name = display_method_name
        if display_class_name is not None:
            self._display_class_name = display_class_name

    @staticmethod
    def _get_basic_printer():
        def basic_printer(prefixes, prefix_s, prefix_s_with_color, text, **kwargs):
            print(prefix_s_with_color, text, **kwargs)
        return basic_printer

    def set_basic_printer(self, printer):
        self._basic_printer = printer

    def set_display_style(
            self,
            method_bracket: Bracket = None,
            method_color: Color = None,
            class_bracket: Bracket = None,
            class_color: Color = None,
    ):
        if method_bracket is not None:
            self.METHOD_BRACKET = method_bracket
        if method_color is not None:
            self.METHOD_COLOR = method_color
        if class_bracket is not None:
            self.CLASS_BRACKET = class_bracket
        if class_color is not None:
            self.CLASS_COLOR = class_color

    def __call__(self, *args, **kwargs):
        stack = inspect.stack()
        caller_frame = stack[1]
        caller_name = caller_frame.function
        caller_code = caller_frame[0].f_code

        inspected_info = None
        for name, obj in caller_frame.frame.f_globals.items():
            if inspect.isclass(obj):
                for m in dir(obj):
                    method = getattr(obj, m, None)
                    if hasattr(method, "__code__") and method.__code__ == caller_code:
                        inspected_info = (caller_name, name)
                        break

        if not inspected_info:
            inspected_info = (caller_name, None)

        caller_name, caller_class = inspected_info
        return self._call(*args, _caller_name=caller_name, _caller_class=caller_class, **kwargs)

    def _call(self, *args, _caller_name, _caller_class, **kwargs):
        prefixes = []
        if self._display_class_name and _caller_class:
            name, bracket, color = _caller_class, self.CLASS_BRACKET, self.CLASS_COLOR
            for plugin in self._plugins:
                name, bracket, color = plugin.middleware_before_class_prefix(
                    name=name,
                    bracket=bracket,
                    color=color,
                )
            caller_class_prefix = Prefix(name, bracket, color)
            prefixes.append(caller_class_prefix)

        if self._display_method_name:
            name, bracket, color = _caller_name, self.METHOD_BRACKET, self.METHOD_COLOR
            for plugin in self._plugins:
                name, bracket, color = plugin.middleware_before_method_prefix(
                    name=name,
                    bracket=bracket,
                    color=color,
                )
            caller_name_prefix = Prefix(name, bracket, color)
            prefixes.append(caller_name_prefix)

        prefixes = [*self._prefixes, *prefixes]

        for plugin in self._plugins:
            prefixes, args, kwargs = plugin.middleware_before_print(
                prefixes=prefixes,
                args=args,
                kwargs=kwargs,
            )

        prefix_s = ' '.join([str(prefix) for prefix in prefixes])
        prefix_s_with_color = ' '.join([prefix.with_color() for prefix in prefixes])
        text = ' '.join([str(arg) for arg in args])

        # print(prefix_s_with_color, text, **kwargs)
        self._basic_printer(
            prefixes=prefixes,
            prefix_s=prefix_s,
            prefix_s_with_color=prefix_s_with_color,
            text=text,
            **kwargs
        )

        for plugin in self._plugins:
            plugin.middleware_after_print(
                prefixes=prefixes,
                prefix_s=prefix_s,
                prefix_s_with_color=prefix_s_with_color,
                text=text
            )
