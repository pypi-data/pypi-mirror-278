from typing import Dict, List
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from .utils import get_by_session_id
from .instructions import actor_instructions, summarizer_instructions
from ...nodes.base import parser, str_parser
# utils
from ...utilities.chatmemory import InMemoryHistory
from ...utilities.print import red, blue, green, cyan
from ...utilities.experiments import TokenInfoHistory

# the version that deletes the previous output and only use summary for the next round, not in use
def predict4_(
        agents: List[RunnableWithMessageHistory], 
        args: Dict, 
        session_id: str, 
        MAX_ITERATION: int,
        verbose=True,
        token_info_history: TokenInfoHistory = None,
    ) -> str:
    """
    Answer a question using agent v4.
    
    Args:
        agents: tuple of (student, summarizer)
        args: dict with 'question' key
        session_id: str for naming the history
    """

    # get the agents
    student, execute_tools, summarizer = agents    
    question = args['question'] # get question
    history = get_by_session_id(session_id)

    ######################## get first response ########################
    num_iterations = 1 # number of past iterations (1,2,3, etc.)
    initial = student.invoke(
        input={
            "question": question, # NOTE: this goes into the system prompt
            "messages": history, # history
            "instructions": actor_instructions # NOTE: this is automatically added to the history
        }, 
        config={
            "configurable": {
                "session_id": session_id
            }
        }
    )
    
    initial_parsed = parser.invoke(initial)
    current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]
    history.delete_messages([0]) # delete `instructions` HumanMessage, history = [AI]
    history.initialize_summary() # history = [<empty summary>, AI]

    if verbose: 
        # Question: is there an empty question
        blue(f"Iter #{num_iterations}. Student")
        red(initial_parsed)
        # history = [<empty summary>, _AI_]
        import pdb; pdb.set_trace()

    while 'final_answer' not in current_actions: 
        # precondition: history = [Summary, AI]
        ######################## Execute tools ########################
        tool_output = execute_tools([initial,]) 
        history.add_message(tool_output[0])
        if verbose:
            blue(f"Iter #{num_iterations}. execute_tools")
            for out in tool_output:
                red(str_parser.invoke(out))
            # history = [Summary, AI, _Tool_]
            import pdb; pdb.set_trace()

        ######################## Take notes for the next round ########################
        
        # delete `instructions` HumanMessage because 
        # we don't want the summarizer to summarize the instructions
        history.delete_messages([0])

        summary = summarizer.invoke(
            input={
                "question": question,
                "messages": history,
                "instructions": summarizer_instructions
            }, 
            # config={
            #     "configurable": {
            #         "session_id": session_id
            #     }
            # }
        )
        if verbose: 
            blue(f"Iter #{num_iterations}. Note taker")
            red(str_parser.invoke(summary))
            # history = [OldSummary, AI, Tool, Instructions, _NewSummary_]

        ######################## Get next response ########################
        history.clear()
        history.add_message(summary)

        num_iterations += 1 # Increment iteration counter
        initial = student.invoke(
            input={
                "messages": history, 
                "question": question, 
                "instructions": actor_instructions
            },
            config={
                "configurable": {
                    "session_id": session_id
                }
            }
        )
        initial_parsed = parser.invoke(initial)
        current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]
        if verbose: 
            blue(f"Iter #{num_iterations}. Student")
            red(initial_parsed)
            # history = [NewSummary, Instructions, _AI_]

        ######################## Exit condition ########################
        if num_iterations >= MAX_ITERATION:
            break

    last_out = parser.invoke(history.get_message(-1))
    if verbose: green(last_out)

    if last_out[0]['args']['Actions'][0]['tool'] == 'final_answer':
        pred_answer = last_out[0]['args']['Actions'][0]['argument']
    else:
        pred_answer = "Unanswerable"

    return {
        "answer" : pred_answer,
        "trace_length": num_iterations,
    }
