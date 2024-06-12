"""Functionality for getting the tables of an arxiv paper.

Ref: 
- https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html
"""

from typing import Optional, Type, Callable
from io import StringIO
import pandas as pd

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel
from langchain_core.tools import BaseTool

from .utils import (
    get_soup, 
    ArxivIdentifierInput,
)

def format_table(table):
    table_io = StringIO(str(table))
    dfs = pd.read_html(table_io, header=0)
    if len(dfs) == 1:
        return dfs[0].to_string(index=False)
    else:
        return table.text        

def get_tables(arxiv_id: str) -> str:
    # tables = get_soup(query).find_all('figure', class_='ltx_table')
    tables = get_soup(arxiv_id).css.select('figure[class=ltx_table]')
    s = ''
    for table in tables:
        if figcaption := table.find('figcaption'):
            # import pdb; pdb.set_trace()
            
            s += f"[{table['id']}] {figcaption.text}\n"
            s += format_table(table) + '\n'
        else:
            print(f"Warning: no caption for table {table['id']}")
            print(table.prettify())
    return s

class ArxivTablesRun(BaseTool):
    name: str = "arxiv_tables"
    description: str = """
    Get the tables from a paper given an arxiv identifier.

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
        return get_tables(arxiv_id)