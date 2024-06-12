"""
Unused in refactor
Can delete
"""

from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .base import (ResponderWithRetries, 
                   get_llm, 
                   render_text_description)
from ..tools.paper import (ArxivIdentifierInput,
                           ArxivSectionInput)

# this version of the prompt would put empty human message in the first place
# prompt v1 
# actor_prompt_template = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """You are a PhD student trying to answer the following research question {question}. 
#         1. sketch a plan to answer the following question. 
#         2. You should answer the tool you use and the input argument for the tool. 
#         If you know the final answer to the user's question, then set the Actions field to "final_answer".
#         Moreover, if the question is a yes/no question, please respond with Yes or No;
#         You have access to the following tools:

#         {list_of_tools} 

#         You have also received a note from the last student who has worked on this problem about what they tried and whether that was helpful"""
#     ),
#     MessagesPlaceholder(variable_name="messages"),
#     ("human", "{instructions}")
# ])

# prompt v2 516
# actor_prompt_template = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """You are a PhD student trying to answer the following research question {question}. 
#         1. sketch a plan to answer the following question. 
#         2. You should answer the tool you use and the input argument for the tool. 
#         If you know the final answer to the user's question, then set the Actions field to "final_answer".
#         Moreover, if the question is a yes/no question, please respond with Yes or No;
#         You have access to the following tools:

#         {list_of_tools} 

#         You have also received a note from yourself from the past about what you have tried 

#         {List_of_actions}

#         and the following output from the tools you used in last round
#         """
#     ),
#     MessagesPlaceholder(variable_name="messages"),
#     ("human", "{instructions}")
# ])

actor_prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a PhD student trying to answer the following research question {question}. 
        1. sketch a plan to answer the following question. 
        2. You should answer the tool you use and the input argument for the tool. 
        If you know the final answer to the user's question, then set the Actions field to "final_answer".
        Moreover, if the question is a yes/no question, please respond with Yes or No;
        You have access to the following tools:

        {list_of_tools} 

        You have also received a note from yourself from the past about what you have tried

        {Reflexion}
        
        and the following output from the tools you used in the last round
        """
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])

class Action(BaseModel):
    tool: str = Field(
        description="name of the tool to use, or `final_answer` if you have the answer."
    )
    argument: Union[ArxivIdentifierInput, ArxivSectionInput, str] = Field(
        description="input argument of the tool, or the final answer if tool is `final_answer`."
    )

class Answer(BaseModel):
    """Answer the question."""

    Thought: str = Field(
        description="Intermediate thoughts on the question."
    )
    Actions: List[Action] = Field(
        description="a list of actions we need to take to answer the question. " \
            "If the answer is found, use final_answer as tool, and the argument is the answer"
    )

# class Answer_w_Reflexion(BaseModel):
#     """Answer the question."""
#     Lessons_learned: str = Field(
#         description="""Write a one sentence note for your future self in the following format about the last action you took:
#                        Action: What tool/action did you use in the last round
#                        Helpful_or_not: Whether or not the actions are helpful
#                        Reason: In one sentence say what you found helpful and what you found not helpful.""")

#     Thought: str = Field(description="Intermediate thoughts on the question.")

#     Actions: List[Action] = Field(
#         description="a list of actions we need to take to answer the question. " \
#             "If the answer is found, use final_answer as tool, and the argument is the answer"
#     )


def create_actor(
        tools: List,
        get_function = None,
        model_name: str = "gpt-3.5-turbo",
        history: bool = False,
        reflexion: bool = False):
    
    
    prompt = actor_prompt_template.partial(
        list_of_tools=render_text_description(tools)
    )
    if not reflexion:
        validator = PydanticToolsParser(tools=[Answer])
        llm = get_llm(model_name).bind_tools(tools=[Answer], tool_choice="Answer")
    else:
        validator = PydanticToolsParser(tools=[Answer_w_Reflexion])
        llm = get_llm(model_name).bind_tools(tools=[Answer_w_Reflexion], tool_choice="Answer_w_Reflexion")


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

