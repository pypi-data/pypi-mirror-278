class BasePlugin:
    def init(self, printi):
        pass

    def middleware_after_print(self, prefixes, prefix_s, prefix_s_with_color, text):
        pass

    def middleware_before_print(self, prefixes, args, kwargs):
        return prefixes, args, kwargs

    def middleware_before_class_prefix(self, name, bracket, color):
        return name, bracket, color

    def middleware_before_method_prefix(self, name, bracket, color):
        return name, bracket, color
