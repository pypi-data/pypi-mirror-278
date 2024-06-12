"""
StructuredTool wrapper for WikiEnv environment implemented in original ReAct code.

Scaffolding from LangChain:
https://github.com/langchain-ai/langchain/blob/master/libs/community/langchain_community/tools/playwright/click.py
"""

from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field

from .base import BaseWikiTool

class LookupToolInput(BaseModel):
    """Input for LookupTool."""

    keyword: str = Field(..., description="keyword to lookup on the page")


class LookupTool(BaseWikiTool):
    """Tool for looking up a keyword on a Wikipedia page."""

    name: str = "lookup_tool"
    # description from ReAct repo
    # https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb
    description: str = "returns the next sentence containing keyword in the current passage."
    args_schema: Type[BaseModel] = LookupToolInput

    def _selector_effective(self, selector: str) -> str:
        if not self.visible_only:
            return selector
        return f"{selector} >> visible=1"

    def _run(
        self,
        keyword: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.wikienv is None:
            raise ValueError(f"WikiEnv not provided to {self.name}")

        obs, reward, done, info = self.wikienv.step(f'lookup[{keyword}]')
        return obs
    
        # page = get_current_page(self.sync_browser)
        # # Navigate to the desired webpage before using this tool
        # selector_effective = self._selector_effective(selector=selector)
        # from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

        # try:
        #     page.click(
        #         selector_effective,
        #         strict=self.playwright_strict,
        #         timeout=self.playwright_timeout,
        #     )
        # except PlaywrightTimeoutError:
        #     return f"Unable to click on element '{selector}'"
        # return f"Clicked element '{selector}'"
