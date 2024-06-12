"""Functionality to lookup keywords in an arxiv paper."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from .utils import (
    get_soup, 
    ARXIV_IDENTIFIER_DESCRIPTION,
    ARXIV_IDENTIFIER_PATTERN,
    get_section_title,
)

def get_lookup_generator(arxiv_id: str, keyword: str, ignore_case: bool =True):
    """
    create generator that gets the text from the p tags
    """

    p_list = get_soup(arxiv_id).find_all('p')
    
    for p in p_list:
        # import pdb; pdb.set_trace()
        # print([el.name for el in p.parents])
        # find section title
        # List of possible class attribute values
        classes = {'ltx_section', 'ltx_subsection', 'ltx_subsubsection'}
        # print('28>', p)
        section = p.find_parent(
            lambda el: el.name == 'section' and (set(el['class']) & classes) 
                        # or (el.name == 'div' and set(el['class']) & {'ltx_abstract'})
        )
        if section is None:
            continue
        # else:
        # print(section['class'])
        section_title = get_section_title(section)
        section_id = section['id']

        # get paragraph text
        p_text = p.get_text()

        text = f'In [{section_id}] {section_title}:\n{p_text}'
        if ignore_case:
            has_match = keyword.lower() in text.lower()
        else:
            has_match = keyword in text
        if has_match:
            yield text

class ArxivLookupInput(BaseModel):
    """Input for the Arxiv section tool."""

    arxiv_id: str = Field(
        description="arxiv identifier" + ARXIV_IDENTIFIER_DESCRIPTION,
        pattern=ARXIV_IDENTIFIER_PATTERN
    )
    query: str = Field(description="keyword to search")

class ArxivLookupRun(BaseTool):
    name: str = "arxiv_lookup"
    description: str = """
    Get paragraphs containing a keyword given arxiv ID and the keyword.

    Args:
        arxiv_id: valid arxiv identifier
        query: keyword or phrase to search
    """
    args_schema: Type[BaseModel] = ArxivLookupInput
    handle_tool_error: Callable = lambda e: f"Error: {e}"

    def _run(
        self,
        arxiv_id: str,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        g = get_lookup_generator(arxiv_id, query)

        return '\n\n'.join(g)