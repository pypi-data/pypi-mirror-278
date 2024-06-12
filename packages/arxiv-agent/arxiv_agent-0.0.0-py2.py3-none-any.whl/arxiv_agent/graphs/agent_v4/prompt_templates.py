from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

'''
%%%%%%%%%%%%%%%%%%%% Agent Prompts %%%%%%%%%%%%%%%%%%%%
'''

"""HotPotQA prompts"""
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

You have also received a note from yourself from the past about what you have tried 

{Notes}

and the following output from the tools you used in last round
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}")
])
hotpot_summarizer_prompt_template = ChatPromptTemplate.from_messages([
    (
    # "system",
    # """You are a PhD student doing research who leaves notes for your future self, at next turn you can only see the previous notes from yourself. 
    #    Summarize what you did from the previous chat history and function output. Try to be concise.""",
    # "system",
    # """You are a PhD student doing research, what notes or advice would be helpful for your future self based on the following observation?""",
    "system", """
You are a PhD student trying to answering the following research question:

{question}

Here is what you tried last and the output:
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}"),
])

"""From previous file: `actor_history.py`"""
# this version of the prompt would put empty human message in the first place
# prompt v1 
# actor_prompt_template = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """You are a PhD student trying to answer the following research question {question}. 
#         1. sketch a plan to answer the following question. 
#         2. You should answer the tool you use and the input argument for the tool. 
#         If you know the final answer to the user's question, then set the Actions field to "final_answer".
#         Moreover, if the question is a yes/no question, please respond with Yes or No;
#         You have access to the following tools:

#         {list_of_tools} 

#         You have also received a note from the last student who has worked on this problem about what they tried and whether that was helpful"""
#     ),
#     MessagesPlaceholder(variable_name="messages"),
#     ("human", "{instructions}")
# ])

# prompt v2 516
qasper_actor_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answer the following research question {question}. 
1. sketch a plan to answer the following question. 
2. You should answer the tool you use and the input argument for the tool. 
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
qasper_summarizer_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
You are a PhD student trying to answering the following research question:

{question}
     
Here is what you tried last and the output:
"""
    ),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{instructions}"),
])

'''
%%%%%%%%%%%%%%%%%%%% Prompt template from commit 9364e6aa2c04773447b0a17c096bcb007e726f24 %%%%%%%%%%%%%%%%%%%%
'''
summarizer_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            # "system",
            # """You are a PhD student doing research who leaves notes for your future self, at next turn you can only see the previous notes from yourself. 
            #    Summarize what you did from the previous chat history and function output. Try to be concise.""",
            # "system",
            # """You are a PhD student doing research, what notes or advice would be helpful for your future self based on the following observation?""",
            "system",
            """You are a PhD student trying to answering the following research question {question}. Here is what you tried last and the output:"""
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{instructions}"),
    ]
)