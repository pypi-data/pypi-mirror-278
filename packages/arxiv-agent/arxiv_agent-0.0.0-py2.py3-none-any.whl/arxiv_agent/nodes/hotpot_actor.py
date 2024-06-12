# """
# Define actor and tool schema for hotpot actors using message stack implementation.
# """

# from typing import List, Union

# from langchain_core.pydantic_v1 import BaseModel, Field
# from langchain.output_parsers.openai_tools import PydanticToolsParser
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.prompts import ChatPromptTemplate

# from .base import ResponderWithRetries, get_llm, render_text_description

# class Action(BaseModel):
#     """HotPotQA action schema"""
#     tool: str = Field(
#         description="name of the tool to use, use final_answer if you have the answer."
#     )
#     argument:  str = Field(
#         description="input argument of the tool, or the final answer if tool is final_answer."
#     )

# class Answer(BaseModel):
#     """HotPotQA answer schema"""

#     Thought: str = Field(description="Intermediate thoughts on the question.")
#     Actions: List[Action] = Field(
#         description="a list of actions we need to take to answer the question. " \
#             "If the answer is found, use final_answer as tool, and the argument is the answer"
#     )

# def create_actor(
#         actor_prompt_template: ChatPromptTemplate,
#         tools: List,
#         # get_function = None,
#         model_name: str = "gpt-3.5-turbo",
#         # history: bool = False
#         ):
    
#     validator = PydanticToolsParser(tools=[Answer])

#     prompt = actor_prompt_template.partial(
#         list_of_tools=render_text_description(tools)
#     )
#     llm = get_llm(model_name).bind_tools(tools=[Answer], tool_choice="Answer")

#     initial_answer_chain = prompt | llm

#     # if not history:
#     Initial_Responder = ResponderWithRetries(
#         runnable=initial_answer_chain, validator=validator
#     )
#     return Initial_Responder
    
#     # else:
#     #     chain_with_history = RunnableWithMessageHistory(
#     #     initial_answer_chain,
#     #     get_function,
#     #     history_messages_key="messages",
#     #     input_messages_key="question"
#     #     )
#     #     return chain_with_history

# """
# Define actor and tool schema for hotpot actors using history implementation.
# """
# def create_actor_history(
#         actor_prompt_template: ChatPromptTemplate,
#         tools: List,
#         get_function = None,
#         model_name: str = "gpt-3.5-turbo",
#         # history: bool = False
#         ):
    
#     prompt = actor_prompt_template.partial(
#         list_of_tools=render_text_description(tools)
#     )
#     llm = get_llm(model_name).bind_tools(tools=[Answer], tool_choice="Answer")

#     initial_answer_chain = prompt | llm

#     # if not history:
#     #     validator = PydanticToolsParser(tools=[Answer])
#     #     Initial_Responder = ResponderWithRetries(
#     #         runnable=initial_answer_chain, validator=validator
#     #     )
#     #     return Initial_Responder
    
#     # else:
#     chain_with_history = RunnableWithMessageHistory(
#         initial_answer_chain,
#         get_function,
#         history_messages_key="messages",
#         input_messages_key="instructions"
#     )
#     return chain_with_history

