from .tool import Tool


class WebSearchTool(Tool):

    name = "web_search"

    async def execute(self, query: str = "", **kwargs) -> str:
        return f"Search results for {query}"
