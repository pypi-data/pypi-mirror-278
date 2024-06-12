from langchain.tools import StructuredTool, BaseTool

def copy_answer(query: str) -> str:
    answer = query
    return answer

def copy_critique(critique: str) -> str:
    return critique

final = StructuredTool.from_function(
    func=copy_answer,
    name='final_answer',
    # description="""
    # A dummy tool that outputs the same answer if the output from the PhD student is final_answer

    # Args: 
    #     query: The final answer from the PhD student
    # """ 
    # description = """Tool for outputing the final answer."""
    # From ReAct original repo:
    description="returns the answer and finishes the task"
)

# TODO: Implementation of final_answer tool using BaseTool subclass
# class FinalAnswer(BaseTool):
#     def __init__

output_answer = StructuredTool.from_function(
    func=copy_answer,
    name='copy_answer',
    description="""
    A dummy tool that copies the answer from the PhD student after the approval of the postdoc

    Args: 
        query: The satisfacotry answer from the PhD student
    """ 
)

revise = StructuredTool.from_function(
    func=copy_critique,
    name='copy_critique',
    description="""
    A dummy tool that copys the revision suggestion from the postdoc 

    Args: 
        critique: What is missing or superfluous in the answer of the PhD student
    """ 
)

def do_nothing(*args, **kwargs):
    return ""

human_tool = StructuredTool.from_function(
    func=do_nothing,
    name='human_tool',
    description="""
    A placeholder tool that does nothing. This is used to represent the human in the loop.
    """ 
)