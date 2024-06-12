"""Functionality for getting the navigation of an arxiv paper."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool

from .utils import (
    get_soup, 
    ArxivIdentifierInput,
    get_section_title,
)

def get_nav(arxiv_id: str) -> str:
    """
    Version of get_navigation that uses the class of the section to determine the level
    """
    soup = get_soup(arxiv_id)

    cls_map = {
        '_' : 'ltx_section',
        'ltx_section': 'ltx_subsection',
        'ltx_subsection': 'ltx_subsubsection'
    }

    def helper(el, cls, level=0):
        s = ''
        el_class = el.get('class')
        if el_class and el_class[0] == cls:
            sid = el['id']
            tabs = '\t'*level
            s += f'{tabs}[{sid}]' + ' ' + get_section_title(el) + '\n'

        if cls in cls_map:
            for child in el.find_all('section', class_=cls_map[cls]):
                s += helper(child, cls_map[cls], level+1)
        return s
    
    # start with level -1 because the first level is always the document level
    return helper(soup, '_', level=-1)

class ArxivNavigationRun(BaseTool):
    name: str = "arxiv_navigation"
    description: str = """
    Get the navigation of a paper given an arxiv identifier. 
    The output is a hierarchical list of sections, subsections, and subsubsections
    with the corresponding section identifier (ID) in brackets at the start of each new line.

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
        return get_nav(arxiv_id)