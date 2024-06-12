"""Functionality for getting references in an arxiv paper."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from .utils import (get_soup, 
                    ARXIV_IDENTIFIER_DESCRIPTION, ARXIV_IDENTIFIER_PATTERN)

def get_bibitem(arxiv_id: str, i: int) -> str:
    bib_id = f'bib.bib{i}'
    return get_soup(arxiv_id).find(id=bib_id).text

class ArxivBibitemInput(BaseModel):
    """Input for the Arxiv bibitem tool."""

    arxiv_id: str = Field(
        description="arxiv identifier" + ARXIV_IDENTIFIER_DESCRIPTION,
        pattern=ARXIV_IDENTIFIER_PATTERN
    )
    i: int = Field(description="index of bib item")

class ArxivBibitemRun(BaseTool):
    name: str = "arxiv_section"
    description: str = """
    Get the i-th reference from a paper given an arxiv identifier.

    Args:
        arxiv_id (str): valid arxiv identifier
        i (int): i is the index of the reference
    """
    args_schema: Type[BaseModel] = ArxivBibitemInput
    handle_tool_error: Callable = lambda e: f"Error: {e}"

    def _run(
        self,
        arxiv_id: str,
        i: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        return get_bibitem(arxiv_id, i)