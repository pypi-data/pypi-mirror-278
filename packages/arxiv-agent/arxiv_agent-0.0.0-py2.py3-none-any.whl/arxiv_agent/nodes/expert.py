from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langgraph.prebuilt.tool_executor import ToolExecutor

from .base import ResponderWithRetries, get_llm, render_text_description
# from ..utilities.chatmemory import get_by_session_id
from ..tools.misc_tool import revise, output_answer

revisor_tools = [revise, output_answer]
revisor_tool_executor = ToolExecutor(revisor_tools)

revisor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a postdoc researcher, trying to help a PhD student with a research problem. \
                    You have access to the following tools:
            
{list_of_tools}

1. "Criticize the previous answer from the PhD student, find out what is missing/superflous to answer the question. Give suggestions on what can be done as a next step, be constructive but not too demanding"
2. You should answer the tool you use and the input argument for the tool. 
If the answer is satisfactory or doesn't differ from the previous answer, then set the Actions field to "copy_answer", otherwise use "copy_critique".

""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        # ("human", "{question}"),
    ]
)

class Feedback(BaseModel):
    tool: str = Field(description="copy_revision if the answer provided is not good enough as the final answer, otherwise copy_answer")
    argument:  str = Field(description="the reason the answer got rejected if the tool is copy_revision, the original answer from the first responder if the tool is copy_answer")

class Reflexion(BaseModel):
    """Critique on the answer provided."""

    Thought: str = Field(description="How would you judge the answer ")
    Actions: List[Feedback] = Field(description="The judge on the answer from the first responder")

def create_expert(
        tools: List,
        get_function = None,
        model_name: str = "gpt-3.5-turbo",
        history: bool = False):
    
    validator = PydanticToolsParser(tools=[Reflexion])
    
    prompt = revisor_prompt_template.partial(
        list_of_tools=render_text_description(tools)
    )
    
    llm = get_llm(model_name).bind_tools(tools=[Reflexion], tool_choice="Reflexion")
    
    revisor_chain = prompt | llm
    
    if not history:
        Initial_Responder = ResponderWithRetries(
        runnable=revisor_chain, validator=validator
        )
        return Initial_Responder

    else:
        revisor_with_history = RunnableWithMessageHistory(
        revisor_chain,
        get_function,
        input_messages_key="question",
        history_messages_key="messages",
        )
        return revisor_with_history