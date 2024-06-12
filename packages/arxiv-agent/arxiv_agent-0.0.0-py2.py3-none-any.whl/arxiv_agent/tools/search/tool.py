"""Tool for the Arxiv API."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from .util_arxiv import ArxivAPIWrapper

class ArxivInput(BaseModel):
    """Input for the Arxiv tool."""

    query: str = Field(description="search query to look up")


class ArxivQueryRun(BaseTool):
    """
    Tool that searches the Arxiv API.

    Old description:
    description: str = (
        "A wrapper around Arxiv.org "
        "Useful for when you need to answer questions about Physics, Mathematics, "
        "Computer Science, Quantitative Biology, Quantitative Finance, Statistics, "
        "Electrical Engineering, and Economics "
        "from scientific articles on arxiv.org. "
        "Input should be a search query."
    )
    
    """

    name: str = "arxiv_query"
    description: str = """
    Get search results from arxiv.org.

    Args:
        query: search query to look up
    """
    api_wrapper: ArxivAPIWrapper = Field(default_factory=ArxivAPIWrapper)
    args_schema: Type[BaseModel] = ArxivInput
    handle_tool_error: Callable = lambda e: f"Error: {e}"

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the Arxiv tool."""
        return self.api_wrapper.run(query)
