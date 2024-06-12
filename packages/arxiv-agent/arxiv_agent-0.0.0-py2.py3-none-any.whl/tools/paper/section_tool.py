"""Functionality for retrieving a specific section from an arxiv paper."""

from typing import Optional, Type, Callable

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool, ToolException

from .tables_tool import format_table
from .utils import (get_soup, 
                    ARXIV_IDENTIFIER_DESCRIPTION, ARXIV_IDENTIFIER_PATTERN)

SECTION_IDENTIFIER_FORMAT = """
For sections, the section ID has the format S1
For subsections, the section ID has the format S1.1
For subsubsections, the section ID has the format S1.1.1
"""

def _handle_error(error: ToolException) -> str:
    return "The following errors occurred during tool execution:" + error.args[0]
        # + "Please try another tool.

def get_section(arxiv_id: str, section_id: str, format_tables: bool = False):
    soup = get_soup(arxiv_id)
    if section := soup.find(id=section_id):
        if format_tables:
            # replace tables with formatted tables
            for table in section.select('figure[class=ltx_table]'):
                table.replace_with(table.find('figcaption').text + '\n' + format_table(table))
        return section.text
    raise ToolException(f"paper with arxiv id {arxiv_id} has no section {section_id}")

class ArxivSectionInput(BaseModel):
    """Input for the Arxiv section tool."""

    arxiv_id: str = Field(
        description="arxiv identifier" + ARXIV_IDENTIFIER_DESCRIPTION,
        pattern=ARXIV_IDENTIFIER_PATTERN
    )
    section_id: str = Field(description="section identifier (ID)") # + SECTION_IDENTIFIER_FORMAT)

class ArxivSectionRun(BaseTool):
    name: str = "arxiv_section"
    description: str = """
    Get a section by arxiv ID and section ID. 
    The arxiv_navigation tool needs to be run to get the list of section and the required section id.

    Args:
        arxiv_id: valid arxiv identifier (ID)
        section_id: valid section identifier (ID)
    """
    args_schema: Type[BaseModel] = ArxivSectionInput
    handle_tool_error: Callable = _handle_error

    def _run(
        self,
        arxiv_id: str,
        section_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        format_tables=True
        return get_section(arxiv_id, section_id)
