from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, cast

from langchain_core.pydantic_v1 import Extra, root_validator
from langchain_core.tools import BaseTool, BaseToolkit

# ################ Old implementation of Wikipedia toolkit ################
# from langchain_community.tools import WikipediaQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper

# wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=4000)

# class WikiToolkit(BaseToolkit):
#     """Toolkit for interacting with Wikipedia"""

#     def get_tools(self) -> List[BaseTool]:
#         """Return list of tools in this toolkit."""

#         query_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

#         return [
#             query_tool,
#         ]


################ New implementation of Wikipedia toolkit ################
# Wrapper for ReAct WikiEnv environment

# from langchain_community.tools.playwright.base import (
#     BaseBrowserTool,
#     lazy_import_playwright_browsers,
# )
from ..tools.wiki import (WikiEnv, BaseWikiTool, 
                          SearchTool, LookupTool)

# class WikiToolkit(BaseToolkit):
#     """Toolkit for interacting with Wikipedia"""

#     def get_tools(self) -> List[BaseTool]:
#         """Return list of tools in this toolkit."""
#         return [
#             SearchTool(),
#             LookupTool(),
#         ]
    
class WikiToolkit(BaseToolkit):
    """Toolkit for interacting with Wikipedia"""

    # sync_browser: Optional["SyncBrowser"] = None
    # async_browser: Optional["AsyncBrowser"] = None
    wikienv: Optional[WikiEnv] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @root_validator
    def validate_wikienv_provided(cls, values: dict) -> dict:
        """Check that the arguments are valid."""
        # lazy_import_playwright_browsers()
        if values.get("wikienv") is None:
            raise ValueError("WikiEnv must be specified.")
        return values

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        tool_classes: List[Type[BaseWikiTool]] = [
            SearchTool,
            LookupTool,
        ]

        tools = [
            tool_cls.from_wikienv(wikienv=self.wikienv)
            for tool_cls in tool_classes
        ]
        return cast(List[BaseTool], tools)

    @classmethod
    def from_wikienv(
        cls,
        wikienv: Optional[WikiEnv] = None,
        # async_browser: Optional[AsyncBrowser] = None,
    ) -> WikiToolkit:
        """Instantiate the toolkit."""
        # This is to raise a better error than the forward ref ones Pydantic would have
        # lazy_import_playwright_browsers()
        return cls(wikienv=wikienv
                #    , async_browser=async_browser
                   )