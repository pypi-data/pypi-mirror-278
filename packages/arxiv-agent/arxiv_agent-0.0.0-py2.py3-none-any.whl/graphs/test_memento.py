from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage

from arxiv_agent.nodes.actor import create_actor
from arxiv_agent.nodes.summarizer import create_summarizer
from arxiv_agent.nodes.expert import create_expert
from arxiv_agent.utilities.chatmemory import InMemoryHistory

from ..nodes.actor import create_actor
from ..nodes.expert import create_expert
from ..nodes.api import initial_tools, revisor_tools, execute_tools
from ..nodes.base import parser


MAX_ITERATIONS = 10
EXPERT_FREQ = 5
MODEL_NAME = "gpt-3.5-turbo"

store={}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

student = create_actor(initial_tools, get_by_session_id, MODEL_NAME, history=True)
summarizer = create_summarizer(get_by_session_id, MODEL_NAME, history=True)
revisor = create_expert(revisor_tools, get_by_session_id, MODEL_NAME, history=True)


def student_loop(
    session_id: str,
    question: str
    ) -> List[BaseMessage]:

    # initialize a chat history
    history = []
    # first response from the student
    initial = student.invoke(
        {"history": history, "question": question},
        config={"configurable": {"session_id": session_id}}
        )
    initial_parsed = parser.invoke(initial)
    history = get_by_session_id(session_id)
    history.initialize_summary()

    while initial_parsed[0]['args']['Actions'][0]['tool'] != 'final_answer': 

        # import pdb; pdb.set_trace()
        tool_output = execute_tools([initial,])
        history.add_message(tool_output[0])

        summary = summarizer.invoke(
            {"messages": history, "question": ""},
            config={"configurable": {"session_id": session_id}}
        ) 

        # delete the summary
        history.delete_messages([-1])
        # delete the empty human message
        history.delete_messages([-1])

        initial = student.invoke(
            {"history": history, "question": ""},
            config={"configurable": {"session_id": session_id}}
        )
        initial_parsed = parser.invoke(initial)
        
        # delete empty human message
        history.delete_messages([-2])
        # insert the summary 
        history.modify_summary(summary)

        # delete the previous tool and output 
        history.delete_messages([3,2])

    return history


def student_revisor_loop(
    question: str,
    session_id: str
    ) -> List[BaseMessage]:

    # first response from the student
    initial = student.invoke(
        {"history": history, "question": question},
        config={"configurable": {"session_id": session_id}}
    )
    revision_parsed = None
    initial_parsed = parser.invoke(initial)
    history = get_by_session_id(session_id)
    history.initialize_summary()
    # keep track of who is the last responder 
    last_round = "student"

    while revision_parsed is None or (initial_parsed[0]['args']['Actions'][0]['tool'] != 'final_answer' or revision_parsed[0]['args']['Actions'][0]['tool'] != 'copy_answer'): 

        if initial_parsed[0]['args']['Actions'][0]['tool'] != 'final_answer': 

            # only add the tool output from the student if the last responder is the student
            if last_round == "student":
                tool_output = execute_tools([initial,])
                history.add_message(tool_output[0])

            summary = summarizer.invoke(
                {"messages": history, "question": ""},
                config={"configurable": {"session_id": session_id}}
            ) 

            # delete the summary
            history.delete_messages([-1])
            # delete the empty human message
            history.delete_messages([-1])

            initial = student.invoke(
                {"history": history, "question": ""},
                config={"configurable": {"session_id": session_id}}
            )
            initial_parsed = parser.invoke(initial)
            last_round = "student"
            
            # delete empty human message
            history.delete_messages([-2])
            # insert the summary 
            history.modify_summary(summary)

            # delete the previous tool and output 
            history.delete_messages([3,2])

        elif initial_parsed[0]['args']['Actions'][0]['tool'] == 'final_answer' and revision_parsed[0]['args']['Actions'][0]['tool'] != 'copy_answer':
            import pdb; pdb.set_trace() 

            # copy_answer
            tool_output = execute_tools([initial,])
            # add answer to history
            history.add_message(tool_output[0])

            # provide critique
            revision = revisor.invoke(
                    {"messages": [HumanMessage(tool_output[0].content)], "question": ""},
                    config={"configurable": {"session_id": session_id}})
            # add critique to history
            history.add_message(revision)

            last_round = "revisor"

            # copy_critique/copy_answer
            revision_parsed = parser.invoke(revision)
            tool_output = execute_tools([revision,])
            if revision_parsed[0]['args']['Actions'][0]['tool'] == 'copy_answer':
                break
            history.add_message(tool_output)

            # Now history = [Q, summary, AI (final_answer), Tool (final_answer), AI(copy_critique), Tool(copy_critique)]
            summary = summarizer.invoke(
                {"messages": history, "question": ""},
                config={"configurable": {"session_id": session_id}}
            ) 

            # Now history = [Q, summary, AI, Tool, AI, Tool, '', new summary]
            # delete the summary
            history.delete_messages(list(range(2,8)))
            history.modify_summary(summary)


    print(history)
