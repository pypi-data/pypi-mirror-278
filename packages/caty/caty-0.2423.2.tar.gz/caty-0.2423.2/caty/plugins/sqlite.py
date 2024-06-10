from .base import FileReader, DataDumper


class SQLITE(FileReader, DataDumper):
    ext = 'sqlite', 'db', 'db3'
    mode = 'rb'

    def load_file(self, path):
        from sqlview import DB
        return DB(path)

    def parse(self, db):
        tables = {
            table.name : table
            for table in db
        }
        return tables
