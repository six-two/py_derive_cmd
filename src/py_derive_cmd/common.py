from typing import Sequence, List
from collections import OrderedDict

def pluralize(count: int, word: str) -> str:
    plural = '' if count == 1 else 's'
    return f'{count} {word}{plural}'

def remove_duplicates(list_with_duplicates: Sequence[str]) -> List[str]:
    as_tuples = [(n, None) for n in list_with_duplicates]
    return list(OrderedDict(as_tuples).keys())
