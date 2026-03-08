class DatabaseTool:

    def __init__(self, db):
        self.db = db

    def query(self, q):
        return self.db.execute(q)