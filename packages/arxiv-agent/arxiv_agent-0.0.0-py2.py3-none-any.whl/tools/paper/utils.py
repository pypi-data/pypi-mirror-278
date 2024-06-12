from functools import cache
import requests
import bs4
import re
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import ToolException


ARXIV_IDENTIFIER_DESCRIPTION = """
In general, the form is YYMM.number{vV}, where
- YY is the two-digit year (07=2007 through 99=2099, and potentially up to 06=2106)
- MM is the two-digit month number (01=Jan,...12=Dec)
- number is a zero-padded sequence number of 4- or 5-digits. From 0704 through 1412 it is 4-digits, starting at 0001. From 1501 on it is 5-digits, starting at 00001. 5-digits permits up to 99999 submissions per month. We cannot currently anticipate more than 99999 submissions per month although extension to 6-digits would be possible.
- vV is a literal v followed by a version number of 1 or more digits starting at v1.
"""

# https://docs.pydantic.dev/latest/concepts/fields/#string-constraints
ARXIV_IDENTIFIER_PATTERN = r"^\d{2}(0[1-9]|1[0-2])\.\d{4,5}(v\d+|)|\d{7}.*$"

@cache
def get_soup(arxiv_id):
    """
    Get the html of a paper given an arxiv identifier.

    Args:
        arxiv_id: valid arxiv identifier
    """
    # get month and year from arxiv_id
    year = int(arxiv_id[:2])
    month = int(arxiv_id[2:4])

    # Cutoff date for new HTML is Dec 1, 2023
    if year > 23 or (year == 23 and month == 12):
        url = f"https://arxiv.org/html/{arxiv_id}"
    else:
        url = f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}"

    response = requests.get(url)
    # handle error if the paper is not found
    if response.status_code != 200:
        raise ToolException(f"Could not find paper with arxiv id {arxiv_id}")
    # TODO: add more fine grained error handling

    html = response.text
    soup = bs4.BeautifulSoup(html, 'html.parser')

    # replace all the math tags with their alttext
    for math in soup.find_all('math', class_='ltx_Math'):
        math.replace_with(math['alttext'])

    return soup

class ArxivIdentifierInput(BaseModel):
    """Input for the Arxiv tool."""

    arxiv_id: str = Field(
        description="arxiv identifier" + ARXIV_IDENTIFIER_DESCRIPTION,
        pattern=ARXIV_IDENTIFIER_PATTERN,
    )

def get_section_title(el):
    """Get the title of a section element
    NOTE: remove tags from the title (e.g., '4.1 Results and Analysis' -> 'Results and Analysis')"""
    s = ''
    if header := el.find([f'h{i}' for i in range(1,7)]):
        # header found
        if tag := header.find('span', class_='ltx_tag'):
            # tag found (sometimes this isn't enough to remove the tag)
            tag.extract() # NOTE: this removes the tag from the original soup
        s = header.text.strip()

        # remove the section number using regex
        # \u00a0 is used a non-breaking space
        # import pdb; pdb.set_trace()
        s = re.sub(r'^.*\u00a0', '', s)
        
    return s