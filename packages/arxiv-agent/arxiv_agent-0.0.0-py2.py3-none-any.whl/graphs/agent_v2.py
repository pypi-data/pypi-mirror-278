"""
Wrapper for arXiv agent v2 
"""

from typing import Dict, List
from functools import partial

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from ..nodes.actor import create_actor
from ..nodes.expert import create_expert
from ..nodes.api import initial_tools, revisor_tools, execute_tools
from ..nodes.base import parser, str_parser
from ..utilities.print import red, blue, green

INITIAL_RESPONSE = "Initial_Response"
EXECUTE_TOOLS = "execute_tools"
REVISOR = "revisor"

def _get_num_iterations(state: List[BaseMessage]):
    # gets number of past iterations (1,2,3, etc.)
    i = 0
    for m in state[::-1]:
        if not isinstance(m, (ToolMessage, AIMessage)):
            break
        i += 1
    return i

def revise_or_continue(
    state: List[BaseMessage]
    , MAX_ITERATION: int
    ) -> str:
    num_iterations = _get_num_iterations(state)
    print('num iters', num_iterations)

    # if we have exceeded the maximum number of iterations
    if num_iterations > MAX_ITERATION:
        return "revisor"
        
    # if the initial responder knows the answer this is indicated by the tool being final_answer and we should check the second last agent
    try: 
        actions = parser.invoke(state[-2])[0]['args']['Actions']
    except: 
        return END
    
    if len(actions) == 0 or actions[0]['tool'] == 'copy_answer':
        return END 
    elif 'final_answer' in [action['tool'] for action in actions]:
        return "revisor"
    else:
        return "Initial_Response"

def end_or_continue(
    state: List[BaseMessage]
    # , MAX_ITERATION: int
    ) -> str:
    # if the initial responder knows the answer this is indicated by the tool being final_answer and we should check the second last agent
    try: 
        actions = parser.invoke(state[-1])[0]['args']['Actions']
    except: 
        print("cannot parse")
        return END

    if actions[0]['tool'] == 'copy_answer':
        return END 
    else:
        return "Initial_Response"

def get_graph(
        MODEL_NAME: str,
        MAX_ITERATION: int
    ) -> None:

    Initial_Responder = create_actor(
       tools=initial_tools, 
        model_name=MODEL_NAME
    )

    revisor = create_expert(
        tools=revisor_tools,
        get_function=None,
        model_name=MODEL_NAME
    )

    revise_or_continue_ = partial(revise_or_continue, MAX_ITERATION=MAX_ITERATION)

    builder = MessageGraph()

    # create nodes 
    builder.add_node(INITIAL_RESPONSE, Initial_Responder.respond)
    builder.add_node(EXECUTE_TOOLS, execute_tools)
    builder.add_node(REVISOR, revisor.respond)

    # build edges
    builder.add_edge(INITIAL_RESPONSE, "execute_tools")
    builder.add_conditional_edges(EXECUTE_TOOLS, revise_or_continue_)
    builder.add_conditional_edges(REVISOR, end_or_continue)

    builder.set_entry_point(INITIAL_RESPONSE)

    graph = builder.compile()

    return graph

def predict2(graph: MessageGraph,
             args: Dict,
             verbose: bool = False
) -> str:

    query = args['question']
    
    if verbose: # stream the output
        events = graph.stream(
            [HumanMessage(content=query)]
        )
        for i, step in enumerate(events):
            # import pdb; pdb.set_trace()
            node, output = next(iter(step.items()))
            blue(f"Iter #{i+1}. {node}")
            # print_wrap(str(output))
            if node == INITIAL_RESPONSE:
                red(parser.invoke(output))
            elif node == EXECUTE_TOOLS:
                # import pdb; pdb.set_trace()
                for out in output:
                    red(str_parser.invoke(out))
            print("---")
    else:
        output = graph.invoke([HumanMessage(content=query)])

    last_out = parser.invoke(output[-1])
    green(last_out)
    # import pdb; pdb.set_trace()

    # get the argument from the final_answer tool
    try: 
        final_tool = last_out[0]['args']['Actions'][0]['tool'] 
        if final_tool == 'final_answer':
            pred_answer = last_out[0]['args']['Actions'][0]['argument']
        else: 
            pred_answer = "Unanswerable"
    except: 
        pred_answer = "Unanswerable"

    return {
        "answer": pred_answer,
        "trace_length": len(output),
    }