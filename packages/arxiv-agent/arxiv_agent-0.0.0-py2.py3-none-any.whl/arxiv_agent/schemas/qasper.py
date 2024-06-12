from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field

from ..tools.paper import (ArxivIdentifierInput,
                           ArxivSectionInput)

class Action(BaseModel):
    """QASPER action schema"""
    tool: str = Field(
        description="name of the tool to use, use final_answer if you have the answer."
    )
    argument: Union[ArxivIdentifierInput, ArxivSectionInput, str] = Field(
        description="input argument of the tool, or the final answer if tool is final_answer."
    )

class Answer(BaseModel):
    """QASPER answer schema."""

    Thought: str = Field(description="Intermediate thoughts on the question.")
    Actions: List[Action] = Field(
        description="a list of actions we need to take to answer the question. " \
            "If the answer is found, use final_answer as tool, and the argument is the answer"
    )

class Answer_w_Notes(BaseModel):
    """Answer the question."""
    Notes: str = Field(
        description="""Write a one sentence note for your future self to summarize if your last action and tool output was helpful in answering the question 
                       in the following format:
                       Action: What tool/action did you use in the last round
                       Helpful_or_not: Whether or not the actions are helpful
                       Reason: In one sentence say what you found helpful and what you found not helpful.
                       Example: 
                       I used arxiv_navigation(arxiv_id); helpful; I found the datasets are described in S3.SS3
                       I used arxiv_lookup(arxiv_id, keyword); not helpful; because I didn't find relevant information.""")

    Thought: str = Field(description="Intermediate thoughts on the question.")

    Actions: List[Action] = Field(
        description="a list of actions we need to take to answer the question. " \
            "If the answer is found, use final_answer as tool, and the argument is the answer"
    )
