"""
StructuredTool wrapper for WikiEnv environment implemented in original ReAct code.

Scaffolding from LangChain:
https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/tools/playwright/navigate.py
"""

from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from .base import BaseWikiTool

class SearchToolInput(BaseModel):
    """Input for NavigateToolInput."""

    entity: str = Field(..., description="entity to search for")

    # @validator("url")
    # def validate_url_scheme(cls, url: str) -> str:
    #     """Check that the URL scheme is valid."""
    #     parsed_url = urlparse(url)
    #     if parsed_url.scheme not in ("http", "https"):
    #         raise ValueError("URL scheme must be 'http' or 'https'")
    #     return url


class SearchTool(BaseWikiTool):
    """Tool for searching Wikipedia."""

    name: str = "search_tool"
    # description from ReAct repo
    # https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb
    description: str = "searches the exact entity on Wikipedia and returns the first paragraph if it exists."\
        "If not, it will return some similar entities to search. Try to search for proper nouns and be concise on the keyword."
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(
        self,
        entity: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.wikienv is None:
            raise ValueError(f"WikiEnv not provided to {self.name}")
        obs, reward, done, info = self.wikienv.step(f'search[{entity}]')
        return obs
    
        # page = get_current_page(self.sync_browser)
        # response = page.goto(url)
        # status = response.status if response else "unknown"
        # return f"Navigating to {url} returned status code {status}"
