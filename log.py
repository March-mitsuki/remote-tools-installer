from datetime import datetime


class Log:
    @staticmethod
    def _now():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

    @staticmethod
    def info(*args):
        print(f"[INFO][{Log._now()}]", *args)

    @staticmethod
    def warning(*args):
        print(f"[WARNING][{Log._now()}]", *args)

    @staticmethod
    def error(*args):
        print(f"[ERROR][{Log._now()}]", *args)
