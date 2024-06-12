from typing import List
from collections import defaultdict
import json

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.prebuilt.tool_executor import ToolExecutor, ToolInvocation

from .base import parser

from ..tools.misc_tool import (
    revise,
    output_answer,
    final,
)

"""Commenting out because they're not being used
initial_tools = arxiv_toolkit.get_tools() + [final]
all_tools = initial_tools + [revise, output_answer] # + wiki_toolkit.get_tools()
# tool_executor = ToolExecutor(all_tools)

revisor_tools = [revise, output_answer]
revisor_tool_executor = ToolExecutor(revisor_tools)

tools_w_human = load_tools(['human']) + initial_tools
tool_executor_w_human = ToolExecutor(tools_w_human)
"""

class Execute_Tools(object):
    def __init__(self, tools: List):
        self.tools = tools
        if final not in self.tools:
            self.tools.append(final)
        self.tool_executor = ToolExecutor(self.tools)

    def __call__(self, state: List[BaseMessage]) -> List[BaseMessage]:
        """
        Takes in a list of messages, where the last message is an AIMessage
        containing tool calls.
        NOTE: each "tool call" can contain multiple actions, depending on 
        the data model defined in the actor implementation 
        (e.g., see Answer model in`arxiv_agent/nodes/actor.py`)

        Returns a list of ToolMessages with length equal to the number of tool calls
        """
        tool_invocation: AIMessage = state[-1]
        parsed_tool_calls = parser.invoke(tool_invocation)
        ids = []
        tool_invocations = []
        for parsed_call in parsed_tool_calls:
            # print('parsed call', parsed_call)
            for action in parsed_call["args"]["Actions"]:
                tool = action["tool"]
                # NOTE sometimes key error
                argument = action["argument"]
                
                tool_invocations.append(
                    ToolInvocation(
                        tool=tool,
                        tool_input=argument,
                    )
                )
                ids.append(parsed_call["id"])
        
        outputs = self.tool_executor.batch(tool_invocations)
        outputs_map = defaultdict(dict)
        for id_, output, invocation in zip(ids, outputs, tool_invocations):
            outputs_map[id_][str(invocation.tool_input)] = output

        return [
            ToolMessage(content=json.dumps(query_outputs), tool_call_id=id_)
            for id_, query_outputs in outputs_map.items()
        ]

# execute_tools = Execute_Tools(all_tools)
# def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
#     """
#     Takes in a list of messages, where the last message is an AIMessage
#     containing tool calls.
#     NOTE: each "tool call" can contain multiple actions, depending on 
#     the data model defined in the actor implementation 
#     (e.g., see Answer model in`arxiv_agent/nodes/actor.py`)

#     Returns a list of ToolMessages with length equal to the number of tool calls
#     """
#     tool_invocation: AIMessage = state[-1]
#     parsed_tool_calls = parser.invoke(tool_invocation)
#     ids = []
#     tool_invocations = []
#     for parsed_call in parsed_tool_calls:
#         # print('parsed call', parsed_call)
#         for action in parsed_call["args"]["Actions"]:
#             tool = action["tool"]
#             argument = action["argument"]
            
#             tool_invocations.append(
#                 ToolInvocation(
#                     tool=tool,
#                     tool_input=argument,
#                 )
#             )
#             ids.append(parsed_call["id"])
    
#     outputs = tool_executor.batch(tool_invocations)
#     outputs_map = defaultdict(dict)
#     for id_, output, invocation in zip(ids, outputs, tool_invocations):
#         outputs_map[id_][str(invocation.tool_input)] = output

#     return [
#         ToolMessage(content=json.dumps(query_outputs), tool_call_id=id_)
#         for id_, query_outputs in outputs_map.items()
#     ]
