
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

# this version of the prompt would put empty human message in the first place
qasper_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a PhD student trying to answer the following research question: 
{question}
     
You have access to the following tools:
     
{list_of_tools}
     
1. Sketch a plan to answer the question
2. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".
Moreover, if the question is a yes/no question, please respond with Yes or No;
Always use arxiv_navigation first to get the correct format before using arxiv_section. 
DO NOT try the following tool again because you already tried them: 
{List_of_actions}
"""
    ), 
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])

# this version of the prompt would put empty human message in the first place
hotpot_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a PhD student trying to answer the following research question:
{question}
     
1. Sketch a plan to answer the question
2. You should answer the tool you use and the input argument for the tool. 
If you know the final answer to the user's question, then set the Actions field to "final_answer".

You have access to the following tools:
     
{list_of_tools}

{few_shot_demonstrations}

DO NOT try the following tool again because you already tried them: 
{List_of_actions}
"""
    ), 
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])

'''
%%%%%%%%%%%%%%%%%%%% Agent Initialization %%%%%%%%%%%%%%%%%%%%
'''

def get_agents(
    MODELNAME: str,
    temperature: float,
    ACTOR_TYPE: str = 'qasper',
    few_shot: bool = False
    ) -> List[RunnableWithMessageHistory]:

    if ACTOR_TYPE == 'qasper':
        from ..schemas.qasper import Answer
        from ..toolkits.arxiv import ArXivToolkit
        toolkit = ArXivToolkit()
        actor_prompt_template = qasper_actor_prompt_template
        few_shot = False

    elif ACTOR_TYPE == 'hotpot':
        from ..schemas.hotpot import Answer
        from ..toolkits.wiki import WikiEnv, WikiToolkit

        wiki_env = WikiEnv()
        toolkit = WikiToolkit.from_wikienv(wiki_env)
        actor_prompt_template = hotpot_actor_prompt_template
        few_shot = True

    else:
        raise ValueError(f"Unknown ACTOR_TYPE: {ACTOR_TYPE}")

    tools = toolkit.get_tools()
    
    from ..prompts.hotpot_few_shot import FEW_SHOT_PROMPT_3

    student = create_actor_history(
        actor_prompt_template=actor_prompt_template,
        tools=tools,
        get_function= get_by_session_id,
        model_name=MODELNAME,
        temperature=temperature,
        schema_class=Answer,
        few_shot=few_shot,
        few_shot_prompt=FEW_SHOT_PROMPT_3
    )
    execute_tools = Execute_Tools(tools)
    return [student, execute_tools]

'''
%%%%%%%%%%%%%%%%%%%% Agent Prediction %%%%%%%%%%%%%%%%%%%%
'''

def predict7(
    agents: List[RunnableWithMessageHistory], 
    args: Dict, 
    session_id: str, 
    MAX_ITERATION: int,
    verbose: bool = True,
    token_info_history: TokenInfoHistory = None,
    ) -> str:
    # print('verbose', verbose)
    query = args['question']

    # current_prompt = actor_prompt_template.partial(question=query)

    # get the agents
    student, execute_tools = agents
    history = get_by_session_id(session_id)
    List_of_actions = []

    # orig_instructions = f"""1. sketch a plan to answer the following question. 2. You should answer the tool you use and the input argument for the tool. 
    #                         If you know the final answer to the user's question, then set the Actions field to "final_answer". 
    #                         Here is a list of actions you already tried. Don't repeat the following Actions:""" 
    actor_instructions = "What should you do next to answer the question?"
    
    iter = 1
    # actor_instructions = orig_instructions + str(List_of_actions)
    initial = student.invoke(
        {"messages": history, "question": query, "instructions": actor_instructions, "List_of_actions": str(List_of_actions)},
        config={"configurable": {"session_id": session_id}}
        )
    if token_info_history: token_info_history.update()
    
    # NOTE: we don't want the summarizer to summarize the instructions
    history.delete_messages([0]) # delete `instructions` HumanMessage history =[AI]
    
    initial_parsed = parser.invoke(initial)
    if verbose: 
        blue(f"Iter #{iter}. Student")
        red(initial_parsed)

    current_actions=[]
    for action in initial_parsed[0]['args']['Actions']:
        try:
            if action['tool'] != 'arxiv_navigation':
                current_actions.append(action)
        except:
            continue
    current_tools = [action['tool'] for action in current_actions]

    while 'final_answer' not in current_tools and iter < MAX_ITERATION: 
        # import pdb; pdb.set_trace()
        List_of_actions.extend(current_actions) # add (tool, argument) to action list
        
        # pre-condition: history = [AI1]
        ######################## Execute tools ########################
        # post-condition: history = [AI1, Tool1]
        tool_output = execute_tools([initial,])
        
        if verbose:
            blue(f"Iter #{iter}. execute_tools")
            for out in tool_output:
                red(str_parser.invoke(out))
        
        # index into first ToolMessage since there is only one tool call
        history.add_message(tool_output[0])

        iter += 1

        # pre-condition: history = [AI1, Tool1]
        ######################## Get next response ########################
        # post-condition: history = [AI2]
        
        # actor_instructions = orig_instructions + str(List_of_actions)
        initial = student.invoke(
        {"messages": history, "question": query, "instructions": actor_instructions, "List_of_actions": str(List_of_actions)},
        config={"configurable": {"session_id": session_id}}
        ) # history = [AI1, Tool1, H, AI2]
        if token_info_history: token_info_history.update()
        if verbose: 
            blue(f"Iter #{iter}. Student")
            cyan(List_of_actions)
            red(parser.invoke(initial))

        history.delete_messages([2,1,0])

        initial_parsed = parser.invoke(initial)
        current_actions = []
        for action in initial_parsed[0]['args']['Actions']:
            try:
                if action['tool'] != 'arxiv_navigation':
                    current_actions.append(action)
            except:
                continue
        current_tools = [action['tool'] for action in current_actions]

    last_message = history.get_message(-1)
    parsed = parser.invoke(last_message)
    if verbose: green(parsed)

    # check duplicates in List_of_actions
    # Only support hotpotQA    
    List_of_actions = [action['argument']  for action in List_of_actions if action['tool'] == 'search_tool']
    duplicated_actions = count_duplicates(List_of_actions)

    return {
        "answer":parsed[0]['args']['Actions'][0]['argument'],
        "trace_length": iter,
        "duplicated_actions": duplicated_actions
    }
