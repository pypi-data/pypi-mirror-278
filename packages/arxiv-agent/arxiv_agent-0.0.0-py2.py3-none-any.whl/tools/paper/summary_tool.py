"""Functionality for getting the summary of an arXiv paper."""

from typing import Optional, Type, Callable
import arxiv

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool
from langchain_core.tools import ToolException

from .utils import ArxivIdentifierInput

def get_summary(arxiv_id: str) -> str:
    results = list(arxiv.Search(id_list=[arxiv_id,]).results())
    
    if len(results) == 0:
        raise ToolException(f"Could not find paper with arxiv id {arxiv_id}")
    
    return results[0].summary

class ArxivSummaryRun(BaseTool):
    name: str = "arxiv_summary"
    description: str = """
    Get the summary a paper given an arxiv identifier. 

    Args:
        arxiv_id: valid arxiv identifier
    """
    args_schema: Type[BaseModel] = ArxivIdentifierInput
    handle_tool_error: Callable = lambda e: f"Error: {e}"

    def _run(
        self,
        arxiv_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return get_summary(arxiv_id)