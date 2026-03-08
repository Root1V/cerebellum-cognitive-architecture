from ..core.tool import Tool

class WebSearchTool(Tool):

    name = "web_search"

    async def execute(self, query):

        return f"Search results for {query}"
