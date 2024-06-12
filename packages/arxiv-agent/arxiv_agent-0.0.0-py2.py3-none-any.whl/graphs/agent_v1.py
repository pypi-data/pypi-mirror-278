"""
Implementation of agent v1 (i.e., ReAct)
Based on:
https://github.com/ysymyth/ReAct/blob/master/hotpotqa.ipynb
"""

from typing import Dict, List
from functools import partial

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable.config import RunnableConfig

from ..nodes.base import parser, str_parser
from ..nodes.api import Execute_Tools
from ..nodes.actor import create_actor
from ..utilities.print import red, blue, green
from ..utilities.experiments import TokenInfoHistory, count_duplicates

INITIAL_RESPONSE = "Initial_Response"
EXECUTE_TOOLS = "execute_tools"

'''
%%%%%%%%%%%%%%%%%%%% Agent Prompts %%%%%%%%%%%%%%%%%%%%
'''

qasper_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer a research related question as best as you can. You have access to the following tools:

{list_of_tools}

1. Sketch a plan to answer the following question
2. You should answer the tool you use and the input argument for the tool. 
If you have the final answer to the user's question, then set the Actions field to "final_answer".
Moreover, if the question is a yes/no question, please respond with Yes or No.
""",
    ),
    MessagesPlaceholder(variable_name="messages"),
])

hotpot_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer a research related question as best as you can. You have access to the following tools:

{list_of_tools}

1. Sketch a plan to answer the following question
2. You should answer the tool you use and the input argument for the tool. 
If you have the final answer to the user's question, then set the Actions field to "final_answer".

{few_shot_demonstrations}
""",
    ),
    MessagesPlaceholder(variable_name="messages"),
])

# original ReAct prompt (without few-shot examples)
"""Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types: 
(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.
(2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.
(3) Finish[answer], which returns the answer and finishes the task.
Here are some examples.
"""
# few-shot examples go here (3 or 6 examples)


"""
from langchain import hub
prompt = hub.pull("hwchase17/react")
"""
"""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

'''
%%%%%%%%%%%%%%%%%%%% Agent Initialization %%%%%%%%%%%%%%%%%%%%
'''

def get_graph(
        MODEL_NAME: str,
        temperature: float,
        MAX_ITERATION: int,
        ACTOR_TYPE: str = 'qasper',
    ) -> MessageGraph:

    if ACTOR_TYPE == 'qasper':
        from ..schemas.qasper import Answer
        from ..toolkits.arxiv import ArXivToolkit
        toolkit = ArXivToolkit()
        chat_prompt_template = qasper_actor_prompt_template
        # no few-shot demonstrations for qasper
        few_shot = False

    elif ACTOR_TYPE == 'hotpot':
        from ..schemas.hotpot import Answer
        from ..toolkits.wiki import WikiEnv, WikiToolkit
        wiki_env = WikiEnv()
        toolkit = WikiToolkit.from_wikienv(wiki_env)
        chat_prompt_template = hotpot_actor_prompt_template
        few_shot = True

    else: 
        raise ValueError(f"ACTOR_TYPE {ACTOR_TYPE} is not recognized.")    
    
    tools = toolkit.get_tools()
    Initial_Responder = create_actor(
        actor_prompt_template=chat_prompt_template,
        tools=tools, 
        model_name=MODEL_NAME,
        temperature=temperature,
        schema_class=Answer,
        few_shot=few_shot
    )
    execute_tools = Execute_Tools(tools)
    
    # #### Build Graph ####
    should_continue_ = partial(should_continue, MAX_ITERATION=MAX_ITERATION)

    builder = MessageGraph()
    # create nodes 
    builder.add_node(INITIAL_RESPONSE, Initial_Responder.respond)
    builder.add_node(EXECUTE_TOOLS, execute_tools)
    # build edges
    builder.add_conditional_edges(INITIAL_RESPONSE, should_continue_)
    builder.add_edge(EXECUTE_TOOLS, INITIAL_RESPONSE)
    # set entry point
    builder.set_entry_point(INITIAL_RESPONSE)
    graph = builder.compile()

    return graph

'''
%%%%%%%%%%%%%%%%%%%% Agent Prediction %%%%%%%%%%%%%%%%%%%%
'''
config = RunnableConfig(
    recursion_limit=100,
)
def predict1(
        graph: MessageGraph, 
        args: Dict,
        verbose: bool = False,
        token_info_history: TokenInfoHistory = None,
    ) -> str:

    query = args['question']
    List_of_actions = []

    if True: # stream the output
        events = graph.stream(
            [HumanMessage(content=query)],
            config=config
        )
        length = 0
        for i, step in enumerate(events):
            node, output = next(iter(step.items()))
            
            if verbose: blue(f"Iter #{i+1}. {node}")
            if node == INITIAL_RESPONSE:
                initial_parsed = parser.invoke(output)
                current_actions=initial_parsed[0]['args']['Actions']
                List_of_actions.extend(current_actions)
                if verbose: red(initial_parsed)
                
                length += 1
                # record token info
                token_info_history.update()

            elif node == EXECUTE_TOOLS:
                for out in output:
                    if verbose: red(str_parser.invoke(out))
            if verbose: print("---")

        last_out = parser.invoke(output[-1])
        # import pdb; pdb.set_trace()
        # last_out = parser.invoke(output)
        
    else:
        output = graph.invoke([HumanMessage(content=query)])
        last_out = parser.invoke(
            output[-1], 
            config=config
        )
        length = len(output)
    if verbose: green(last_out)

    # get the argument from the final_answer tool
    try: 
        final_tool = last_out[0]['args']['Actions'][0]['tool'] 
        if final_tool == 'final_answer':
            pred_answer = last_out[0]['args']['Actions'][0]['argument']
        else: 
            pred_answer = "Unanswerable"
    except: 
        pred_answer = "Unanswerable"

    List_of_actions = [action['argument']  for action in List_of_actions if action['tool'] == 'search_tool']
    duplicated_actions = count_duplicates(List_of_actions)

    return {
        "answer": pred_answer,
        "trace_length": length,
        "duplicated_actions": duplicated_actions
    }

def _get_num_iterations(state: List[BaseMessage]):
    # gets number of AI messages (i.e., number of times the agents tried to answer the question)
    i = 0
    for m in state[::-1]:
        if not isinstance(m, (ToolMessage, AIMessage)):
            break
        if isinstance(m, AIMessage):
            i += 1
    return i

def should_continue(
        state: List[BaseMessage], 
        MAX_ITERATION: int
    ) -> str:
    # NOTE: this the number of agent responses
    num_iterations = _get_num_iterations(state)
    print('num iters', num_iterations, MAX_ITERATION)

    # if we have exceeded the maximum number of iterations
    if num_iterations == MAX_ITERATION:
        return END
    
    # if the initial responder knows the answer
    # this is indicated by the tool being final_answer
    actions = parser.invoke(state[-1])[0]['args']['Actions']
    # https://smith.langchain.com/public/bbe3d42e-3010-4dc7-99d3-6569eb8f5a18/r
    if len(actions) == 0 or 'final_answer' in [action['tool'] for action in actions]: # NOTE: sometimes we get KeyError here
        return END
    
    return "execute_tools"