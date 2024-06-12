"""
LangChain implementation of single-agent Memento.
"""

from typing import Dict, List
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from ...nodes.actor import create_actor_history
from ...nodes.summarizer import create_summarizer

from .utils import get_by_session_id
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
        from ...schemas.qasper import Answer
        from ...toolkits.arxiv import ArXivToolkit
        from .prompt_templates import (qasper_actor_prompt_template, 
                                               qasper_summarizer_prompt_template)
        toolkit = ArXivToolkit()
        actor_prompt_template = qasper_actor_prompt_template
        summarizer_prompt_template = qasper_summarizer_prompt_template
        few_shot = False
        few_shot_prompt=None
    elif ACTOR_TYPE == 'hotpot':
        from ...schemas.hotpot import Answer
        from ...toolkits.wiki import WikiEnv, WikiToolkit
        from ...prompts.hotpot_few_shot import FEW_SHOT_PROMPT_3
        from .prompt_templates import (hotpot_actor_prompt_template,
                                               hotpot_summarizer_prompt_template)
        wiki_env = WikiEnv()
        toolkit = WikiToolkit.from_wikienv(wiki_env)
        actor_prompt_template = hotpot_actor_prompt_template
        summarizer_prompt_template = hotpot_summarizer_prompt_template
        few_shot = True
        few_shot_prompt=FEW_SHOT_PROMPT_3
    else: 
        raise ValueError(f"ACTOR_TYPE {ACTOR_TYPE} is not recognized.")  

    # initialize actor
    tools = toolkit.get_tools()
    student = create_actor_history(
        actor_prompt_template=actor_prompt_template,
        tools=tools,
        get_function=get_by_session_id, 
        model_name=MODELNAME, 
        temperature=temperature,
        schema_class=Answer,
        few_shot=few_shot,
        few_shot_prompt=few_shot_prompt
    )
    # initialize tool executor
    from ...nodes.api import Execute_Tools
    execute_tools = Execute_Tools(tools)
    
    # initialize summarizer
    summarizer = create_summarizer(
        summarizer_prompt_template=summarizer_prompt_template,
        model_name=MODELNAME, 
        temperature=temperature
    )
    return [student, execute_tools, summarizer]
