from typing import List
from semanticscholar import SemanticScholar
# import argparse
# import csv
import os
from requests import Session
from typing import Generator, TypeVar

S2_API_KEY = os.environ.get('S2_API_KEY', '')

T = TypeVar('T')


sch = SemanticScholar()

def get_citation_counts(arxiv_ids: List[str]) -> List[int]:
    """
    Get the number of citations for a paper given an arxiv identifier.
    """
    # print('arxiv', arxiv_ids)
    s2_ids = [arxiv_to_s2(arxiv_id) for arxiv_id in arxiv_ids]
    # print('s2', s2_ids)
    
    # Implementation #1: semanticscholar package
    # # NOTE: for some reason it doesn't handle invalid arxiv ids
    # results = sch.get_papers(
    #     s2_ids, 
    #     fields=['citationCount',],
    #     return_not_found=True
    # )
    # print('results', results)
    # return [result['citationCount'] for result in results]

    # Implementation #2: S2 API
    results = [paper['citationCount'] if paper else 0 for paper in get_papers(s2_ids, fields='citationCount')]
    return results


######### Helper functions #########

def arxiv_to_s2(arxiv_id: str) -> str:
    """
    Convert an arxiv identifier to a Semantic Scholar identifier.
    """
    # remove the version number
    base_arxiv_id = arxiv_id.split('v')[0]
    return f"arxiv:{base_arxiv_id}"


# Ref: https://github.com/allenai/s2-folks/blob/main/examples/python/bulk_get_papers_by_pmid/get_papers.py

def batched(items: list[T], batch_size: int) -> list[T]:
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]

def get_paper_batch(session: Session, ids: list[str], fields: str = 'paperId,title', **kwargs) -> list[dict]:
    params = {
        'fields': fields,
        **kwargs,
    }
    headers = {
        'X-API-KEY': S2_API_KEY,
    }
    body = {
        'ids': ids,
    }

    # https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/post_graph_get_papers
    with session.post('https://api.semanticscholar.org/graph/v1/paper/batch',
                       params=params,
                       headers=headers,
                       json=body) as response:
        response.raise_for_status()
        return response.json()


def get_papers(ids: list[str], batch_size: int = 100, **kwargs) -> Generator[dict, None, None]:
    # use a session to reuse the same TCP connection
    with Session() as session:
        # take advantage of S2 batch paper endpoint
        for ids_batch in batched(ids, batch_size=batch_size):
            yield from get_paper_batch(session, ids_batch, **kwargs)

