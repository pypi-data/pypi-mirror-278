from typing import Dict, List

from langchain_core.messages import AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory

from .utils import get_by_session_id
from .instructions import actor_instructions, summarizer_instructions
from ...nodes.base import parser, str_parser
# utils
from ...utilities.print import red, blue, green
from ...utilities.experiments import TokenInfoHistory, count_duplicates

'''
%%%%%%%%%%%%%%%%%%%% Agent Prediction %%%%%%%%%%%%%%%%%%%%
'''
# for gpt3.5
def predict4_35(
        agents: List[RunnableWithMessageHistory], 
        args: Dict, 
        session_id: str, 
        MAX_ITERATION: int,
        verbose: bool = True,
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

    # history = []
    history = get_by_session_id(session_id) # history = []

    ######################## get first response ########################
    # NOTE: 'instructions' is automatically added to the history when student.invoke is called
    # import pdb; pdb.set_trace()
    num_iterations = 1 #number of past iterations (1,2,3, etc.)

    # import pdb; pdb.set_trace()

    List_of_Notes = []
    List_of_actions = []
    
    # import pdb; pdb.set_trace()

    initial = student.invoke(
        {"messages": history, "question": question, "Notes": str(List_of_Notes), "instructions": actor_instructions},
        config={"configurable": {"session_id": session_id}}
    )
    # history = [H, AI]
    if token_info_history: token_info_history.update() # record token info

    # NOTE: we don't want the summarizer to summarize the instructions
    history.delete_messages([0]) # delete `instructions` HumanMessage history =[AI]
    
    initial_parsed = parser.invoke(initial)
    current_actions=initial_parsed[0]['args']['Actions']
    current_tools = [action['tool'] for action in current_actions]
    # NOTE: sometimes we get KeyError here

    if verbose: 
        blue(f"Iter #{num_iterations}. Student")
        red(initial_parsed)

    while 'final_answer' not in current_tools:
        # pre-condition: history = [AI1]
        ######################## Execute tools ########################
        # post-condition: history = [AI1, Tool1]

        List_of_actions.extend(current_actions)
        tool_output = execute_tools([initial,])
        if token_info_history: token_info_history.update()
        history.add_message(tool_output[0]) # history = [AI1, Tool1]
        
        if verbose:
            blue(f"Iter #{num_iterations}. execute_tools") 
            for out in tool_output:
                red(str_parser.invoke(out))
        
        # pre-condition: history = [AI1, Tool1]
        ######################## Take notes for the next round ########################
        # post-condition: history = [AI1, Tool1]

        # import pdb; pdb.set_trace()

        tool_call = history.get_message(-2).additional_kwargs['tool_calls'][0]['function']['arguments']
        tool_message = history.get_message(-1).content
        to_summarize = [
            AIMessage(content = tool_call), 
            AIMessage(content=tool_message)
        ]
        
        # for attempt in range(5):
        #     try:
        summary = summarizer.respond(
        {"messages": to_summarize, "question": question, "instructions": summarizer_instructions}
        ) # Sum1 = AI1 + Tool1
        if token_info_history: token_info_history.update()
            #     break
            # except:
            #     continue
        if verbose:
            blue(f"Iter #{num_iterations}. Note taker")
            red(str_parser.invoke(summary))
    
        num_iterations += 1

        # pre-condition: history = [AI1, Tool1]
        ######################## Get next response ########################
        # post-condition: history = [AI2]

        # history = [AI1, Tool1] 
        initial = student.invoke(
            {"messages": history, "question": question, "Notes": str(List_of_Notes), "instructions": actor_instructions},
            config={"configurable": {"session_id": session_id}}
        ) # history = [AI1, Tool1, Ins, AI2]
        
        history.delete_messages([-2]) # history = [AI1, Tool1, AI2]
        
        initial_parsed = parser.invoke(initial)
        # NOTE: could get KeyError here (if action doesn't have tool key)
        current_actions=initial_parsed[0]['args']['Actions']
        current_tools = [action['tool'] for action in current_actions]

        # finally update notes with summary!
        List_of_Notes.append(summary.content)
        history.delete_messages([1,0]) # history = [AI2]
        
        if verbose: 
            blue(f"Iter #{num_iterations}. Student")
            red(initial_parsed)

        ######################## Check break condition ########################
        if num_iterations >= MAX_ITERATION:
            break

    last_out = parser.invoke(history.get_message(-1))
    if verbose: green(last_out)

    if last_out[0]['args']['Actions'][0]['tool'] == 'final_answer':
        pred_answer = last_out[0]['args']['Actions'][0]['argument']
    else:
        pred_answer = "Unanswerable"

    List_of_actions = [action['argument']  for action in List_of_actions if action['tool'] == 'search_tool']
    duplicated_actions = count_duplicates(List_of_actions)

    return {
        "answer" : pred_answer,
        "trace_length": num_iterations,
        "duplicated_actions": duplicated_actions
    }


def predict4(
        agents: List[RunnableWithMessageHistory], 
        args: Dict, 
        session_id: str, 
        MAX_ITERATION: int,
        verbose: bool = True,
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

    history = []

    ######################## get first response ########################
    # NOTE: 'instructions' is automatically added to the history when student.invoke is called
    # import pdb; pdb.set_trace()
    num_iterations = 1 #number of past iterations (1,2,3, etc.)
    
    if verbose: blue(f"Iter #{num_iterations}. Student")

    # respond with retries # TODO need to fix

    initial = student.invoke(
    {"messages": history, "question": question, "instructions": actor_instructions},
    config={"configurable": {"session_id": session_id}}
    )
    if token_info_history: token_info_history.update()
    initial_parsed = parser.invoke(initial)
    history = get_by_session_id(session_id) # history = [Ins, AI]


    history.delete_messages([0]) # delete `instructions` HumanMessage history =[AI]
    history.initialize_summary() # history = [emptysummary, AI]
    
    if verbose: red(initial_parsed)
    current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]

    List_of_summary = []

    while 'final_answer' not in current_actions:
        ######################## Execute tools ########################
        if verbose: blue(f"Iter #{num_iterations}. execute_tools") 
        tool_output = execute_tools([initial,])
        if token_info_history: token_info_history.update()
        if verbose:
            for out in tool_output:
                red(str_parser.invoke(out))      
        history.add_message(tool_output[0]) # history = [emptySummary, AI, Tool]
        
        ######################## Take notes for the next round ########################

        # only take notes from the previous round output
        to_summarize = history.get_last_round() # [AI, Tool]

        if verbose: blue(f"Iter #{num_iterations}. Note taker")

        for attempt in range(5):
            try:
                summary = summarizer.invoke(
                    {"messages": to_summarize, "question": question, "instructions": summarizer_instructions},
                    config={"configurable": {"session_id": session_id}}
                )
                if token_info_history: token_info_history.update()
                break
            except:
                continue

        if verbose: red(str_parser.invoke(summary))

        List_of_summary.append(summary)
        history.modify_summary(AIMessage(content=str(List_of_summary)))
        # history =[realSummary, AI, Tool]

        ######################## Get next response ########################
        num_iterations += 1

        if verbose: blue(f"Iter #{num_iterations}. Student")
        # the current thoughts and actions depend not on the summary

        initial = student.invoke(
            {"messages": history, "question": question, "instructions": actor_instructions},
            config={"configurable": {"session_id": session_id}}
        ) # history = [Summary, AI, Tool, Ins, AI]
        if token_info_history: token_info_history.update()
        initial_parsed = parser.invoke(initial)
        history.delete_messages([-2]) # history = [Summary, AI, Tool, AI]
        
        if verbose: red(initial_parsed)
        current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]

        #replace the history with summary now
        history.delete_messages([2,1]) # history = [Summary, AI]

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