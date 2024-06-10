import hashlib

from .base_plugin import BasePlugin


class DynamicColorPlugin(BasePlugin):
    def __init__(self, *colors):
        self.colors = colors

    def middleware_before_class_prefix(self, name, bracket, color):
        # get md5 of class name
        # use md5 to get a color (mod operation)

        md5 = hashlib.md5(name.encode('utf-8')).hexdigest()[:-4]
        color = self.colors[int(md5, 16) % len(self.colors)]
        return name, bracket, color
