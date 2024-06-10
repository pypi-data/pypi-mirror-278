from tempfile import NamedTemporaryFile
from os.path import isfile, expanduser


class Reader:
    mode = 'r'

    def load(self, raw):
        raise NotImplementedError

    def load_file(self, path):
        raise NotImplementedError

    def parse(self, data):
        return data

    def read(self, path):
        if hasattr(path, 'read'):
            # stdin
            if self.mode == 'rb':
                raw = path.buffer.read()
            else:
                raw = path.read()
            if isinstance(self, FileReader):
                raw = self.load_raw(raw)
        else:
            raw = self.load_file(path)
        raw = self.load(raw)
        data = self.parse(raw)
        return data


class RawReader(Reader):
    def load_file(self, path):
        with open(path, self.mode) as inp:
            raw = inp.read()
        return raw


class FileReader(Reader):
    def load(self, raw):
        return raw

    def load_raw(self, raw):
        with NamedTemporaryFile(delete=False) as tmp:
            try:
                tmp.write(raw)
            except TypeError:
                tmp.write(raw.encode())
        return self.load_file(tmp.name)


class Dumper:
    def dump(self, data):
        raise NotImplemented


class DataDumper(Dumper):
    @property
    def conf(self):
        from . import INI, JSON, TOML, YAML
        conf = dict()
        try:
            for reader in (INI, JSON, TOML, YAML):
                for ext in reader.ext:
                    confil = expanduser(f'~/.config/caty.{ext}')
                    if isfile(confil):
                        try:
                            conf = reader().read(confil)
                        except Exception:
                            print(f" ! can't load config file : {confil}")
                            raise
                        raise StopIteration
        except StopIteration:
            pass
        else:
            from . import config
            try:
                from yaml import dump
                with open(expanduser('~/.config/caty.yaml'), 'w') as confil:
                    dump(config, confil)
            except ImportError:
                from json import dump
                with open(expanduser('~/.config/caty.json'), 'w') as confil:
                    dump(config, confil)
            conf = config
        return conf

    def dump(self, data):
        from nicely import Printer
        Printer(**self.conf).print(data)


class TextDumper(Dumper):
    def dump(self, lines):
        for line in lines:
            print(line)

