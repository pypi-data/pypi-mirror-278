"""Toolkit for interacting with arXiv."""
from typing import List

from langchain_community.agent_toolkits.base import BaseToolkit
from langchain_community.tools import BaseTool

from ..tools.search.tool import ArxivQueryRun
from ..tools.paper import (ArxivBibitemRun,
                           ArxivFiguresRun,
                           ArxivLookupRun,
                           ArxivNavigationRun,
                            ArxivSectionRun,
                            ArxivSummaryRun,
                            ArxivTablesRun)

class ArXivToolkit(BaseToolkit):
    """Toolkit for interacting with arXiv"""

    def get_tools(self) -> List[BaseTool]:
        """Return list of tools in this toolkit."""

        return [
            # tools implemented using existing arxiv python package
            ArxivQueryRun(),

            # tools that we implemented
            ArxivSummaryRun(),
            ArxivNavigationRun(),
            ArxivSectionRun(),
            # ArxivBibitemRun(),
            # ArxivFiguresRun(),
            # ArxivTablesRun(),
            ArxivLookupRun(),
        ]