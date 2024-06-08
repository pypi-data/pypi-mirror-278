import time


class TimePrefix:
    def __init__(self):
        self.start_time = time.time()

    @staticmethod
    def div_num(n, base=60):
        return n // base, n % base

    def __call__(self):
        second = int(time.time() - self.start_time)
        minutes, second = self.div_num(second)
        hours, minutes = self.div_num(minutes)
        return '%02d:%02d:%02d' % (hours, minutes, second)
