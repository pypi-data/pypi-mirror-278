"""Functionality for getting the figures of an arxiv paper."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool, ToolException

from .utils import (
    get_soup, 
    ArxivIdentifierInput,
)

def get_figure(arxiv_id: str) -> str:
    # figures = get_soup(arxiv_id).find_all('figure', class_=lambda cls : cls == 'ltx_figure')
    
    # NOTE: Use css selector allows you to match exact class names
    #   https://stackoverflow.com/questions/47776762/beautiful-soup-exact-match-when-using-findall
    # Official documentation:
    #   https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors-through-the-css-property
    figures = get_soup(arxiv_id).css.select('figure[class=ltx_figure]')
    s = ''
    for fig in figures:
        if figcaption := fig.find('figcaption'):
            s += f"[{fig['id']}] {figcaption.text}\n"
        else:
            print(f"Warning: no caption for figure {fig['id']}")
            print(fig.prettify())
    return s

class ArxivFiguresRun(BaseTool):
    name: str = "arxiv_figures"
    description: str = """
    Get the figures from a paper given an arxiv identifier.

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
        return get_figure(arxiv_id)