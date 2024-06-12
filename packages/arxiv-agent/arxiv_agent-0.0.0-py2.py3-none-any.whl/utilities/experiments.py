from collections import Counter
import argparse
import pandas as pd
from langchain_community.callbacks.openai_info import OpenAICallbackHandler

def get_base_parser(boolean_flags: bool = True):
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", "-m", type=str, default="zero",
                        help="The method to use for generating the answer.",
                        choices=["zero", "qasper", "v1", "v2", "v4", "v4_", "v5", "v6", "v7", "v8", "react", "v9", "v72", "v82"])
    parser.add_argument('--output_path', '-op', type=str, default='output',
                        help='The directory to save the predictions.')
    parser.add_argument('--model_name', "-model", type=str, default='gpt-3.5-turbo',
                        help='The llm model used in the LangChain methods.',
                        choices=['gpt-3.5-turbo', 'gpt-4-turbo', 'gpt-4o'])
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument('--project', '-p', type=str)
    parser.add_argument('--max_iteration', '-max_it', type=int, default=15,
                        help='The maximum number of iterations to run.')
    parser.add_argument("--user", type=str, default="Albert")
    parser.add_argument("--batch_size", "-bs", default=10, type=int, 
                        help="batch size")
    parser.add_argument("--batch_number", "-bn", default=1 , type=int,
                        help="batch number >= 1")

    
    # boolean flags
    if boolean_flags:
        parser.add_argument('--force', '-f', action='store_true', default=False,
                            help='If set, recompute predictions (instead of using saved predictions).')
        parser.add_argument("--verbose", "-v", action="store_true", default=False,
                            help="If set, prints streaming output from LangChain.")
    return parser

def print_run_info(predicted_answers_and_evidence):
    # Print token info as a pandas dataframe
    indices = []
    data = []
    for key, value in predicted_answers_and_evidence.items():
        if value['error'] == '': # no error
            indices.append(key)
            if 'token_info_history' in value and len(value['token_info_history']) > 0:
                row = value['token_info_history'][-1]
            elif 'token_info' in value: # backward compatibility with predictions JSON files without token_info_history
                row = value['token_info']
            else:
                continue
            if 'trace_length' in value:
                row['trace_length'] = value['trace_length']
            data.append(row)
    df = pd.DataFrame(data=data, index=indices)
    print("token info per question:")
    print(df.to_string())
    print("summary:")
    print(df.describe())

def get_token_info(cb):
    token_info = {
        "total_tokens": cb.total_tokens,
        "total_cost": cb.total_cost,
        "completion_tokens": cb.completion_tokens,
        "prompt_tokens": cb.prompt_tokens,
    }
    return token_info

class TokenInfoHistory(object):
    def __init__(self, cb: OpenAICallbackHandler):
        self.cb = cb
        self.history = []
    def update(self):
        self.history.append(get_token_info(self.cb))
    def get_history(self):
        return self.history

def count_duplicates(lst):
    # count the occurences for list elements
    count = Counter(lst)

    duplicates = sum(count[item] - 1 for item in count)

    return duplicates
