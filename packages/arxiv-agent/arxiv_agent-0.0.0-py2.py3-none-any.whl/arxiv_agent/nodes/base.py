from typing import List
from langchain_core.pydantic_v1 import ValidationError
from langchain_core.tools import BaseTool
from langchain_core.messages import BaseMessage, HumanMessage

from langsmith import traceable
from langchain_openai import ChatOpenAI
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import BaseTool


def render_text_description(tools: List[BaseTool]) -> str:
    """Render the tool name and description in plain text.

    Output will be in the format of:

    .. code-block:: markdown

        1) search: This tool is used for search

        Args:
            query: The search query

        ================================

        2) calculator: This tool is used for math

        Args:
            query: The math query
    """
    s = ""
    for i, tool in enumerate(tools):
        s += f"{i+1}) {tool.name}: {tool.description}\n" + "\n\n"
    return s

class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    @traceable
    def respond(self, state: List[BaseMessage]):
        # print('state', [type(s).__name__ for s in state])
        response = []
        for attempt in range(3):
            try:
                response = self.runnable.invoke(state) #{"messages": state})
                self.validator.invoke(response)
                return response
            except ValidationError as e:
                state = state + [HumanMessage(content=repr(e))]
        return response
    
def get_llm(model_name="gpt-3.5-turbo", temperature=0):
    llm = ChatOpenAI(model=model_name,temperature=temperature)
    return llm

parser = JsonOutputToolsParser(return_id=True)

str_parser = StrOutputParser()