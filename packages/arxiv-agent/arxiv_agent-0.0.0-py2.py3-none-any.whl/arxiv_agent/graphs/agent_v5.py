
from typing import Dict, List

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage


from arxiv_agent.nodes.base import parser
from arxiv_agent.nodes.api import execute_tools, initial_tools, revisor_tools
from arxiv_agent.nodes.actor_history import create_actor
from arxiv_agent.nodes.summarizer import create_summarizer
from arxiv_agent.nodes.expert import create_expert
from arxiv_agent.utilities.chatmemory import InMemoryHistory

store={}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

def get_agents(
        MODELNAME: str, 
        revisor: bool = False
    ) -> List[RunnableWithMessageHistory]:

    student = create_actor(initial_tools, get_by_session_id, MODELNAME, history=True)
    summarizer = create_summarizer(get_by_session_id, MODELNAME, history=True)
    if not revisor:
        return [student, summarizer]
    else:
        revisor = create_expert(revisor_tools, get_by_session_id, MODELNAME, history=True)
        return [student, summarizer, revisor]


def predict5(
        agents: List[RunnableWithMessageHistory], 
        args: Dict, 
        session_id: str, 
        verbose: bool = False
    ) -> str:

    arxiv_id = args['article_id']
    question = args['question']
    
    # construct query
    query = f"{question} in the paper with arxiv identifier {arxiv_id}"

    # get the agents
    student, summarizer, revisor = agents
    history = []

    actor_instructions = """1. sketch a plan to answer the following question. 2. You should answer the tool you use and the input argument for the tool. If you know the final answer to the user's question, then set the Actions field to "final_answer". You should avoid repetitve work."""


    # import pdb; pdb.set_trace()

    # first response from the student
    initial = student.invoke(
        {"messages": history, "question": query, "instructions": actor_instructions},
        config={"configurable": {"session_id": session_id}}
    )
    revision_parsed = None
    initial_parsed = parser.invoke(initial)
    current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]

    history = get_by_session_id(session_id)
    # history.initialize_summary()
    # keep track of who is the last responder 
    last_round = "student"

    while revision_parsed is None or ('final_answer' not in current_actions or revision_parsed[0]['args']['Actions'][0]['tool'] != 'copy_answer'): 

        if 'final_answer' not in current_actions: 

            # only add the tool output from the student if the last responder is the student
            if last_round == "student":
                tool_output = execute_tools([initial,])
                history.add_message(tool_output[0])

                history.delete_messages([0])

            summary = summarizer.invoke(
                {"messages": history, "question": question, "instructions": "What notes would you leave for your future self? Include things you tried to avoid repetitive work in the future."},
                config={"configurable": {"session_id": session_id}}
            ) 

            history.clear()
            history.add_message(summary)

            initial = student.invoke(
            {"messages": history, "question": query, "instructions": actor_instructions},
            config={"configurable": {"session_id": session_id}}
            )
            
            initial_parsed = parser.invoke(initial)
            current_actions = [action['tool'] for action in initial_parsed[0]['args']['Actions']]
            last_round = "student"
            
            # delete empty human message
            history.delete_messages([-2])
            # insert the summary 
            history.modify_summary(summary)

            # delete the previous tool and output 
            history.delete_messages([3,2])

        elif 'final_answer' not in current_actions and (revision_parsed is None or revision_parsed[0]['args']['Actions'][0]['tool'] != 'copy_answer' ):

            # copy_answer
            tool_output = execute_tools([initial,])
            # add answer to history
            history.add_message(tool_output[0])

            # provide critique
            revision = revisor.invoke(
                    {"messages": [HumanMessage(tool_output[0].content)], "question": ""},
                    config={"configurable": {"session_id": session_id}})
            # add critique to history
            # history.add_message(revision)
            # delete the empty HumanMessage
            history.delete_messages([4])

            last_round = "revisor"

            # copy_critique/copy_answer
            revision_parsed = parser.invoke(revision)
            tool_output = execute_tools([revision,])

            # import pdb; pdb.set_trace()
            if revision_parsed[0]['args']['Actions'][0]['tool'] == 'copy_answer':
                last_message = history.get_message(-1)
                parsed = parser.invoke(last_message)
                return parsed[0]['args']['Actions'][0]['argument']
            history.add_message(tool_output[0])

            # Now history = [Q, summary, AI (final_answer), Tool (final_answer), AI(copy_critique), Tool(copy_critique)]
            summary = summarizer.invoke(
                {"messages": history, "question": ""},
                config={"configurable": {"session_id": session_id}}
            ) 

            # some bug here that the summary does not make sense 
            # Now history = [Q, summary, AI, Tool, AI, Tool, '', new summary]
            # delete the summary
            history.delete_messages(list(reversed(list(range(2,8)))))
            history.modify_summary(summary)

    return 
