"""
Unused in refactor
Can delete
"""
from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .base import ResponderWithRetries, get_llm, render_text_description
from ..tools.paper import (
    ArxivIdentifierInput,
    ArxivSectionInput,
    ArxivBibitemInput,
)

# this version of the prompt would put empty human message in the first place
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a PhD student trying to answer the following research question {question}. 
               You have access to the following tools:
                {list_of_tools}
            1. sketch a plan to answer the question
            2. You should answer the tool you use and the input argument for the tool. 
            If you know the final answer to the user's question, then set the Actions field to "final_answer".
            Moreover, if the question is a yes/no question, please respond with Yes or No;
            Always use arxiv_navigation first to get the correct format before using arxiv_section. 
            DO NOT try the following tool again because you already tried them: {List_of_actions}"""
        ) , 
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{instructions}")
    ]
)

class Action(BaseModel):
    tool: str = Field(
        description="name of the tool to use, use final_answer if you have the answer."
    )
    argument: Union[ArxivIdentifierInput, ArxivSectionInput, str] = Field(
        description="input argument of the tool, or the final answer if tool is final_answer."
    )

class Answer(BaseModel):
    """Answer the question."""

    Thought: str = Field(description="Intermediate thoughts on the question.")
    # description="The information you need and what tool you should use to get the information."
    # Thought: str = Field(description="Intermediate thoughts on the question.")
    Actions: List[Action] = Field(
        description="a list of actions we need to take to answer the question. " \
            "If the answer is found, use final_answer as tool, and the argument is the answer"
    )


def create_actor(
        tools: List,
        get_function = None,
        model_name: str = "gpt-3.5-turbo",
        history: bool = False):
    
    validator = PydanticToolsParser(tools=[Answer])

    prompt = actor_prompt_template.partial(
        list_of_tools=render_text_description(tools)
    )
    llm = get_llm(model_name).bind_tools(tools=[Answer], tool_choice="Answer")

    initial_answer_chain = prompt | llm

    if not history:
        Initial_Responder = ResponderWithRetries(
            runnable=initial_answer_chain, validator=validator
        )
        return Initial_Responder
    
    else:
        chain_with_history = RunnableWithMessageHistory(
        initial_answer_chain,
        get_function,
        history_messages_key="messages",
        input_messages_key="instructions"
        )
        return chain_with_history

