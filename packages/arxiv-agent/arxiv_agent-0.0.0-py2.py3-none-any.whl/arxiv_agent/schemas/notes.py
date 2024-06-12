from typing import List, Union

from langchain_core.pydantic_v1 import BaseModel, Field

class Lessons_learned(BaseModel):
    """"""
    past_action: str = Field(
        description="""one action taken in the last round"""
                    )
    helpful_or_not: str = Field(
        description="""whether or not the action helps to answer the question"""
                    )
    Reason: str = Field(
        description="""Reason why the action is helpful or not helpful. Explain in one sentence"""
                    )

class Reflexion1(BaseModel):
    """Lessons learned from the past work"""
    Thought: List[Lessons_learned] = Field(
        description="""a list of lessons_learned on actions taken in the past, whether they are helpful
                       for answering the question and why"""
                    )

# from arxiv_agent.nodes.actor import Action

# class Lessons_learned(BaseModel):
#     """"""
#     past_action: Action = Field(
#         description="""one action taken in the last round"""
#                     )
#     helpful_or_not: str = Field(
#         description="""whether or not the action helps to answer the question"""
#                     )
#     Reason: str = Field(
#         description="""Reason why the action is helpful or not helpful. Explain in one sentence"""
#                     )

# class Reflexion1(BaseModel):
#     """Lessons learned from the past work"""
#     Thought: List[Lessons_learned] = Field(
#         description="""a list of lessons_learned on actions taken in the past, whether they are helpful
#                        for answering the question and why"""
#                     )
