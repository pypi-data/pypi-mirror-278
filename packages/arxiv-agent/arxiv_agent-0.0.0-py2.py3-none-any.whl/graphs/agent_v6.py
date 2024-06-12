
from typing import Dict, List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from arxiv_agent.nodes.base import parser, str_parser
from arxiv_agent.nodes.api import execute_tools, initial_tools
from arxiv_agent.nodes.actor_history import create_actor
from arxiv_agent.nodes.summarizer import create_summarizer
from arxiv_agent.nodes.terminator import create_terminator

from arxiv_agent.utilities.chatmemory import InMemoryHistory

store={}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

def get_agents(
    MODELNAME: str, 
    ) -> List[RunnableWithMessageHistory]:

    student = create_actor(initial_tools, get_by_session_id, MODELNAME, history=True)
    summarizer = create_summarizer(get_by_session_id, MODELNAME, history=True)
    terminator = create_terminator(MODELNAME)
    return [student, summarizer, terminator]


def predict6(
    agents: List[RunnableWithMessageHistory], 
    args: Dict, 
    session_id: str, 
    verbose=True) -> str:

    arxiv_id = args['article_id']
    question = args['question']
    
    # construct query
    query = f"{question} in the paper with arxiv identifier {arxiv_id}"

    # get the agents
    student, summarizer, terminator = agents
    history = []

    actor_instructions = """
    1. Think about how to answer the original question. 
    2. Choose a tool and specify the input argument. Choose the "final_answer" tool if you have an answer.
    
    Remember to avoid repetitve work.
    """

    # first action from the students
    initial = student.invoke(
        {"messages": history, "question": query, "instructions": actor_instructions},
        config={"configurable": {"session_id": session_id}}
    )
    initial_parsed = parser.invoke(initial)
    current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]

    history = get_by_session_id(session_id)
    # initialize summaries
    prev_summary = summary = None
    
    iters = 0
    while 'final_answer' not in current_actions: 
        # import pdb; pdb.set_trace()

        # get tool output
        tool_output = execute_tools([initial,])
        history.add_message(tool_output[0])

        # delete first human instruction
        history.delete_messages([0])

        # store previous summary first
        prev_summary = summary
        # get current summary
        summary = summarizer.invoke(
            {"question": question, "messages": history, "instructions": "What notes would you leave for your future self? Include things you tried to avoid repetitive work in the future."},
            config={"configurable": {"session_id": session_id}}
        ) 

        # check if we should terminate
        if iters > 0:
            is_making_progress = terminator.respond({"question": question, "messages": [prev_summary, summary]})
            is_making_progress_parsed = parser.invoke(is_making_progress)
            
            if not is_making_progress_parsed[0]['args']['grade']: # get bool
                # final answer is just the summary
                break
        
        history.clear()
        history.add_message(summary)

        initial = student.invoke(
            {"messages": history, "question": query, "instructions": actor_instructions},
            config={"configurable": {"session_id": session_id}}
        )
        if verbose:
            print(history)
        initial_parsed = parser.invoke(initial)
        current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]
        
        iters += 1

    if 'final_answer' in current_actions: 
        for action in current_actions:
            if action['tool'] != 'final_answer':
                continue    
            final_answer = action['argument']
    else:
        # if terminated by terminator
        final_answer = str_parser.invoke(summary)
    return final_answer
