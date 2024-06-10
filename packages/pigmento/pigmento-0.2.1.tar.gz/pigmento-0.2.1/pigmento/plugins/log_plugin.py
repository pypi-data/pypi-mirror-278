from pigmento.plugins.base_plugin import BasePlugin


class LogPlugin(BasePlugin):
    def __init__(self, log_file):
        self.log_file = log_file

    def middleware_after_print(self, prefixes, prefix_s, prefix_s_with_color, text):
        with open(self.log_file, 'a+') as f:
            f.write(f'{prefix_s} {text}\n')
