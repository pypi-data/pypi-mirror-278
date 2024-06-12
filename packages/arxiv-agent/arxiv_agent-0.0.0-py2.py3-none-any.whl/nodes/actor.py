from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from  ..prompts.hotpot_few_shot import FEW_SHOT_PROMPT_3

from .base import ResponderWithRetries, get_llm, render_text_description

def create_actor(
        actor_prompt_template: ChatPromptTemplate,
        tools: List,
        # get_function = None,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0, 
        schema_class: BaseModel = None,
        few_shot: bool = False
        ):
    
    validator = PydanticToolsParser(tools=[schema_class])

    prompt = actor_prompt_template.partial(
        list_of_tools=render_text_description(tools)
    )

    # adding few_shot demonstrations for hotpotQA
    if few_shot:
        prompt = prompt.partial(
            few_shot_demonstrations=FEW_SHOT_PROMPT_3
        )
    else: 
        prompt = prompt.partial(
            few_shot_demonstrations=""
        )

    llm = get_llm(model_name=model_name, temperature=temperature).bind_tools(tools=[schema_class], tool_choice="Answer")

    initial_answer_chain = prompt | llm

    # if not history:
    Initial_Responder = ResponderWithRetries(
        runnable=initial_answer_chain, validator=validator
    )
    return Initial_Responder
    

def create_actor_history(
        actor_prompt_template: ChatPromptTemplate,
        tools: List,
        get_function = None,
        model_name: str = "gpt-3.5-turbo",
        temperature: float = 0,
        schema_class: BaseModel = None,
        few_shot: bool = False,
        few_shot_prompt = str,
        ):

    prompt = actor_prompt_template.partial(
        list_of_tools=render_text_description(tools)
    )

    # adding few_shot demonstrations for hotpotQA
    if few_shot:
        prompt = prompt.partial(
            few_shot_demonstrations=few_shot_prompt
        )


    llm = get_llm(model_name=model_name, temperature=temperature).bind_tools(tools=[schema_class], tool_choice=schema_class.__name__)

    initial_answer_chain = prompt | llm

    # if not history:
    #     validator = PydanticToolsParser(tools=[Answer])

    #     Initial_Responder = ResponderWithRetries(
    #         runnable=initial_answer_chain, validator=validator
    #     )
    #     return Initial_Responder
    # else:
    chain_with_history = RunnableWithMessageHistory(
        initial_answer_chain,
        get_function,
        history_messages_key="messages",
        input_messages_key="instructions"
    )
    return chain_with_history

