from typing import Dict, List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ..nodes.base import parser, str_parser
from ..nodes.actor import create_actor_history
from ..nodes.api import Execute_Tools
from ..utilities.chatmemory import InMemoryHistory
from ..utilities.print import red, blue, green, cyan
from ..utilities.experiments import TokenInfoHistory, count_duplicates


store={}
def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]

'''
%%%%%%%%%%%%%%%%%%%% Agent Prompts %%%%%%%%%%%%%%%%%%%%
'''
# QASPER PROMPTS
qasper_actor_prompt_template_w_Notes = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer the following research question {question}. 
1. Describe what your action was in last round and evaluate in one sentence whether it was helpful and why.
2. sketch a plan to answer the following question. 
3. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".
Moreover, if the question is a yes/no question, please respond with Yes or No;
You have access to the following tools:

{list_of_tools} 

You have also received a note from yourself from the past about what you have tried 

{Notes}

and the following output from the tools you used in last round
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])
qasper_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer the following research question {question}. 
1. sketch a plan to answer the following question. 
2. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".
Moreover, if the question is a yes/no question, please respond with Yes or No;
You have access to the following tools:

{list_of_tools} 

"""),
    ("human", "{instructions}")
])

# HOTPOT PROMPTS
hotpot_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer the following research question:

{question}

1. Sketch a plan to answer the following question
2. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".

You have access to the following tools:

{list_of_tools} 

{few_shot_demonstrations}

"""
    ),
    ("human", "{instructions}")
])

hotpot_actor_prompt_template_w_Notes = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer the following research question:

{question}

1. Sketch a plan to answer the following question
2. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".

You have access to the following tools:

{list_of_tools} 

{few_shot_demonstrations}

"""
    ),
    ("human", """

You have also received a note from yourself from the past about what you have tried 

{Notes}

and the following output from the tools you used in last round
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])

# hotpot_actor_prompt_template_w_Notes = ChatPromptTemplate.from_messages([
#     ("system", """
# You are a PhD student trying to answer the following research question:

# {question}

# 1. Sketch a plan to answer the following question
# 2. You should answer the tool you use and the input argument for the tool. 
# If you know the final answer to the user's question, then set the Actions field to "final_answer".

# You have access to the following tools:

# {list_of_tools} 
# """
#     ),
#     ("human", """
#     You have also received a note from yourself from the past about what you have tried 

# {Notes} 
# """
#     ),
#     ("human","""
#     and the following output from the tools you used in last round
# """
#     ),
#     MessagesPlaceholder(variable_name="messages"),
#     ("human", "{instructions}")
# ])

def get_agents(
        MODELNAME: str, 
        temperature: float,
        ACTOR_TYPE: str = 'qasper',
    ) -> List[RunnableWithMessageHistory]:

    if ACTOR_TYPE == 'qasper':
        from ..schemas.qasper import Answer_w_Notes
        from ..schemas.qasper import Answer
        from ..toolkits.arxiv import ArXivToolkit

        toolkit = ArXivToolkit()
        actor_w_Notes_prompt_template = qasper_actor_prompt_template_w_Notes
        actor_prompt_template = qasper_actor_prompt_template
        few_shot = False

    elif ACTOR_TYPE == 'hotpot':
        from ..schemas.hotpot import Answer
        from ..schemas.hotpot import Answer_w_Notes
        from ..toolkits.wiki import WikiEnv, WikiToolkit

        wiki_env = WikiEnv()
        toolkit = WikiToolkit.from_wikienv(wiki_env)
        actor_prompt_template = hotpot_actor_prompt_template
        actor_w_Notes_prompt_template = hotpot_actor_prompt_template_w_Notes
        few_shot = True
    else: 
        raise ValueError(f"ACTOR_TYPE {ACTOR_TYPE} is not recognized.")  

    # initialize actor
    tools = toolkit.get_tools()

    from ..prompts.hotpot_few_shot import V8_FEW_SHOT_PROMPT_3, V8_FEW_SHOT_PROMPT_3_w_Notes

    student_w_Notes = create_actor_history(
        actor_prompt_template=actor_w_Notes_prompt_template,
        tools=tools,
        get_function=get_by_session_id, 
        model_name=MODELNAME, 
        temperature=temperature,
        schema_class=Answer_w_Notes,
        few_shot=few_shot,
        few_shot_prompt=V8_FEW_SHOT_PROMPT_3_w_Notes
    )

    student = create_actor_history(
        actor_prompt_template=actor_prompt_template,
        tools=tools,
        get_function=get_by_session_id, 
        model_name=MODELNAME, 
        temperature=temperature,
        schema_class=Answer,
        few_shot=True,
        few_shot_prompt=V8_FEW_SHOT_PROMPT_3
    )
    # initialize tool executor
    execute_tools = Execute_Tools(tools)
    
    return [student, execute_tools, student_w_Notes]

# new version adding few_shot_demonstrations and moving notes outside system prompt  
def predict82(
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
        agents: [student]
        args: dict with 'question' key
        session_id: str for naming the history
    """

    # get the agents
    student, execute_tools, student_w_Notes = agents    
    question = args['question'] # get question

    history = get_by_session_id(session_id) # history =[H, AI1]
    List_of_Notes = []
    List_of_actions = []

    ######################## get first response ########################
    # NOTE: 'instructions' is automatically added to the history when student.invoke is called
    iter = 1 #number of past iterations (1,2,3, etc.)

    actor_instructions = "What should you do next to answer the question?"
    
    if verbose: blue(f"Iter #{iter}. Student")
    initial = student.invoke(
        {"messages": history, "question": question, "Notes": str(List_of_Notes), "instructions": actor_instructions},
        config={"configurable": {"session_id": session_id}}
    )
    initial_parsed = parser.invoke(initial)

    # record token info
    token_info_history.update()

    # NOTE: we don't want the summarizer to summarize the instructions
    history.delete_messages([0]) # delete `instructions` HumanMessage history =[AI1]
    
    initial_parsed = parser.invoke(initial)
    if verbose: red(initial_parsed)

    current_actions=initial_parsed[0]['args']['Actions']
    current_tools = [action['tool'] for action in current_actions]

    while 'final_answer' not in current_tools:
        # pre-condition: history = [AI1]
        # after first round: history = [AI1, Tool1, AI2]
        ######################## Execute tools ########################
        # post-condition: history = [AI1, Tool1]
        # after first round: history = [AI1, Tool1, AI2, Tool2]
        List_of_actions.extend(current_actions)

        tool_output = execute_tools([initial,])
        if token_info_history: token_info_history.update()
        if verbose:
            blue(f"Iter #{iter}. execute_tools") 
            for out in tool_output:
                red(str_parser.invoke(out))      
        history.add_message(tool_output[0]) # history = [AI1, Tool1]
        
        # pre-condition: history = [AI1, Tool1]
        # after first round: history = [AI1, Tool1, AI2, Tool2]
        ######################## Get next response ########################
        # post-condition: history = [AI1, Tool1, AI2]
        # after first round: history = [AI2, Tool2, AI3]
        iter += 1
        if verbose: 
            blue(f"Iter #{iter}. Student")
            cyan(List_of_actions)
        # history = [AI1, Tool1] 
        initial = student_w_Notes.invoke(
            {"messages": history, "question": question, "Notes": str(List_of_Notes[:-2]), "instructions": actor_instructions},
            config={"configurable": {"session_id": session_id}}
        ) # history = [AI1, Tool1, Ins, AI2]

        history_len = history.get_length()
        if history_len == 6:
            # pre-condition: history = [AI1, Tool1, AI2, Tool2, H, AI3]
            history.delete_messages([4,1,0])
            # post-condition: history = [AI2, Tool2, AI3]
        elif history_len == 4:
            # pre-condition: history = [AI1, Tool1, H, AI2]
            history.delete_messages([-2]) 
            # post-condition: history = [AI1, Tool1, AI2]
        else:
            raise ValueError(f"should not get here, len(history)={history_len}, history={history}")

        initial_parsed = parser.invoke(initial)

        current_actions=initial_parsed[0]['args']['Actions']
        current_tools = [action['tool'] for action in current_actions]

        Note = initial_parsed[0]['args']['Notes']  # Note1 = N (AI1, Tool1)
        if verbose:
            cyan(Note)
        # import pdb; pdb.set_trace()

        if verbose: red(initial_parsed)

        List_of_Notes.append(Note)

        if iter >= MAX_ITERATION:
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
        "trace_length": iter,
        "duplicated_actions": duplicated_actions
    }
