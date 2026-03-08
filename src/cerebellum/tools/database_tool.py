from ..core.tool import Tool


class DatabaseTool(Tool):

    name = "database"

    def __init__(self, db=None):
        self.db = db

    async def execute(self, query="", **kwargs):
        if self.db:
            return self.db.execute(query)
        return f"[DatabaseTool] mock result for: {query}"
