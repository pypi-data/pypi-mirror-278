from .base import RawReader, DataDumper


class TOML(RawReader, DataDumper):
    ext = 'toml', 'tml'

    def load(self, raw):
        try:
            # py 3.11
            from tomllib import loads
        except ModuleNotFoundError:
            # pip install toml
            from toml import loads
        return loads(raw)
