from typing import Dict, List, Union

from text_processing.download import download
from text_processing.tagging import get_keywords as _get_keywords

download("pos2", "pt")
download("embeddings2", "pt")


def get_keywords(
    text: str,
    consider: List = ["NOUN", "ADJ", "VERB"],
    min_size: int = 3,
    as_bow: bool = False,
) -> Union[List, Dict]:
    return _get_keywords(text, consider, min_size, as_bow, "pt")


get_keywords.__doc__ = _get_keywords.__doc__
