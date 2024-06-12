'''
%%%%%%%%%%%%%%%% Summarizer Instructions %%%%%%%%%%%%%%%%
'''

# prompt v1 
# summarizer_instructions = """
# You and several other agents are working to answer the question. 
# Write one sentence that you want to pass on to the next agent based on this observation.
# """

#prompt v2 
# summarizer_instructions = """
# You and several other agents are working to answer the question. 
# Write one sentence that you want to pass on to the next agent to tell them what actions to take or not to take based on your work.
# """

#prompt v3 
# summarizer_instructions = """
# You and several other agents are working to answer the question. 
# Write one sentence that you want to pass on to the next agent to tell them what you did was useful and what was not.
# """

#prompt v4 
#prompt v1 516
# summarizer_instructions = """
# You and several other students are working together to answer the question. 
# Write a note for the next student to summarize what you did in the following format:
# Action: What you did in the last round
# Helpful_or_not: Whether or not they are helpful
# Reason: what information did you find that made it helpful or what you failed to find that it was not helpful.
# """

# prompt v2 516
summarizer_instructions = """
Write a note for your future self to summarize what you did in the following format because you are gonna lose the original working history:
Action: What you did in the last round
Helpful_or_not: Whether or not the actions are helpful
Reason: In one sentence say what you found helpful and what you found not helpful.
"""

# summarizer_instructions = """
# What notes would you leave for your future self? 
# Include things you tried to avoid repetitive work in the future.
# """

'''
%%%%%%%%%%%%%%%% Actor Instructions %%%%%%%%%%%%%%%%
'''
# actor_instructions = """
# 1. sketch a plan to answer the following question. 
# 2. You should answer the tool you use and the input argument for the tool. 
# If you know the final answer to the user's question, then set the Actions field to "final_answer". 
# if the question cannot be answered with the given context, please respond with Unanswerable.

# Remember to avoid repetitive work.
# """
actor_instructions = "What should you do next to answer the question?"
# Moreover, if the question is a yes/no question, please respond with Yes or No;
