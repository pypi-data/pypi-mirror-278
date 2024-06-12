from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langgraph.prebuilt.tool_executor import ToolExecutor

from .base import ResponderWithRetries, get_llm, render_text_description
from ..tools.misc_tool import revise, output_answer


terminator_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a postdoc researcher, trying to help a PhD student to answer the following research question: {question}.
               You have access to the notes they made over time.
            """,
        ),
        MessagesPlaceholder(variable_name="messages"),
        (  
            "human", 
            "Respond True if the student is making progress between the two notes, and False otherwise."
        )
    ]
)

class Grade(BaseModel):
    grade: bool = Field(description="Whether the student is making progress between the two notes.")

def create_terminator(
        model_name: str = "gpt-3.5-turbo",
    ):
    
    validator = PydanticToolsParser(tools=[Grade])
    
    llm = get_llm(model_name).bind_tools(tools=[Grade], tool_choice="Grade")
    
    chain = terminator_prompt_template | llm
    
    Terminator = ResponderWithRetries(
        runnable=chain, validator=validator
    )
    return Terminator


