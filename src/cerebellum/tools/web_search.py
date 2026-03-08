from ..core.tool import Tool

class WebSearchTool(Tool):

    name = "web_search"

    async def execute(self, query):

        return f"results for {query}"