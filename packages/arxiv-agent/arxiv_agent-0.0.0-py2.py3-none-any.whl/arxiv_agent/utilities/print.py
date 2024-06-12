from termcolor import colored
import textwrap

WRAPPER = textwrap.TextWrapper(width=80)

def print_wrap(output):
    """
    Print the output with text wrapping (80 characters per line).
    """
    word_list = WRAPPER.wrap(text=output)
    for element in word_list: 
        print(element)

# 
# Colorful print
# See possible colors here: https://pypi.org/project/termcolor/
# 
def red(text):
    print(colored(text, 'red'))
def blue(text):
    print(colored(text, 'blue'))
def green(text):
    print(colored(text, 'green'))
def yellow(text):
    print(colored(text, 'yellow'))
def cyan(text):
    print(colored(text, 'cyan'))