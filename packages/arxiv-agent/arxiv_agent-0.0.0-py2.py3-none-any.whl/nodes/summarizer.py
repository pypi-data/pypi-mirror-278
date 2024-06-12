from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.output_parsers.openai_tools import (
    PydanticToolsParser
)
from .base import ResponderWithRetries, get_llm, str_parser

def create_summarizer(
    summarizer_prompt_template: ChatPromptTemplate,
    model_name: str = "gpt-3.5-turbo",
    temperature: float =0
    ):

    # llm = get_llm(model_name).with_structured_output(Reflexion1)
    llm = get_llm(model_name, temperature=temperature)

    summarizer_answer_chain = summarizer_prompt_template | llm

    validator = str_parser
                                      
    # if not history:
    Summarizer = ResponderWithRetries(runnable=summarizer_answer_chain, validator=validator)
    return Summarizer

    # else:
    #     summarizer_with_history = RunnableWithMessageHistory(
    #     summarizer_answer_chain,
    #     get_function,
    #     input_messages_key="instructions",
    #     history_messages_key="messages",
    #     )
    #     return summarizer_with_history

def create_summarizer_history(
    summarizer_prompt_template: ChatPromptTemplate,
    get_function = None,
    model_name: str = "gpt-3.5-turbo",
    temperature: float = 0
    ):

    # llm = get_llm(model_name).with_structured_output(Reflexion1)
    llm = get_llm(model_name, temperature=temperature)

    summarizer_answer_chain = summarizer_prompt_template | llm

    summarizer_with_history = RunnableWithMessageHistory(
        summarizer_answer_chain,
        get_function,
        input_messages_key="instructions",
        history_messages_key="messages",
    )
    return summarizer_with_history