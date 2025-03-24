class Table:
    def __init__(self, table: dict):
        self.table = list(table.keys())[0]
        self.body = table.get(self.table)
        self.tablename = self.body.get("tablename")
        self.columns = self.body.get("columns")
        self.links = self.body.get("links")
        self.pos = self.body.get("pos")


class Loader:
    def __init__(self, obj, database):
        self.datababse = database
        tables = obj.get(database).get("tables")
        self.tables = [Table(table) for table in tables]
        self.links = obj.get(database).get("links")
