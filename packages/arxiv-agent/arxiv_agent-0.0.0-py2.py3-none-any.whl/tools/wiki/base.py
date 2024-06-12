"""
Functionality for stateful Wikipedia browswer

Refs:
https://api.python.langchain.com/en/latest/_modules/langchain_community/agent_toolkits/playwright/toolkit.html#PlayWrightBrowserToolkit
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Type

from langchain_core.pydantic_v1 import root_validator
from langchain_core.tools import BaseTool
from langchain_core.utils import guard_import

from .utils import WikiEnv

class BaseWikiTool(BaseTool):
    """Base class for browser tools."""

    wikienv: Optional[WikiEnv] = None
    # async_browser: Optional["AsyncBrowser"] = None

    # @root_validator
    # def validate_browser_provided(cls, values: dict) -> dict:
    #     """Check that the arguments are valid."""
    #     lazy_import_playwright_browsers()
    #     if values.get("async_browser") is None and values.get("sync_browser") is None:
    #         raise ValueError("Either async_browser or sync_browser must be specified.")
    #     return values

    @classmethod
    def from_wikienv(
        cls,
        wikienv: Optional[WikiEnv] = None,
        # async_browser: Optional[AsyncBrowser] = None,
    ) -> BaseWikiTool:
        """Instantiate the tool."""
        # lazy_import_playwright_browsers()
        return cls(wikienv=wikienv)  # type: ignore[call-arg]