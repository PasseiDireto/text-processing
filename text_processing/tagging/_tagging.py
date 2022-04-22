from typing import Dict, List, Union

from polyglot.text import Text


def get_keywords(
    text: str,
    consider: List[str] = ["NOUN", "ADJ", "VERB", "PROPN"],
    min_size: int = 3,
    as_bow: bool = False,
    lang: str = "pt",
) -> Union[List[str], Dict]:

    """Extract keywords from `text`.
    Args:
        text (str): string to be processed.
        consider (List, optional): Part-of-speech (PoS) elements considered to be keywords.
        Defaults to ["NOUN", "ADJ", "VERB", "PROPN"].
        min_size (int, optional): Minimum length of output tokens. Defaults to 3.
        as_bow (bool, optional): If True, computes keyword frequencies and returns a dict;
        returns list of extracted keywords otherwise.
        Defaults to False.
    Returns:
        List or Dict: List of extracted keywords or dict with keyword frequencies.
    """

    text_obj = Text(text, hint_language_code=lang)

    def search(text_obj, consider, min_size, as_bow):
        pos_tags, counts = text_obj.pos_tags, {}
        for token, tag in pos_tags:
            if tag in consider and len(token) >= min_size:
                if as_bow:
                    counts[token] = counts.get(token, 0) + 1
                else:
                    yield token
        if as_bow:
            yield counts

    if as_bow:
        return next(search(text_obj, consider, min_size, as_bow))

    return list(search(text_obj, consider, min_size, as_bow))
