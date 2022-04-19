import re

import nlpnet

from ._processing import cleanText


def getKeywords(text, clean_first=True):

    """
    Extract keywords from `text`.
    Args:
        text (str):
            String to be processed.
        clean_first (bool):
            If True, `text` is to be cleaned.
            Defaults to True.
    Returns:
        list: Keywords as they appear in `text`.
    """

    if not "__pos_tagger__" in globals():
        __pos_tagger__ = nlpnet.POSTagger(language="pt")

    tags = []

    if clean_first:
        new_text = cleanText(text, lowercase=True, drop_accents=True)
    else:
        new_text = text.lower()

    # Remove symbols that are not letters, numbers or spaces.
    if isinstance(new_text, str):
        new_text = re.sub(r"[^a-z0-9 áâãàéêíóôõúüç-]+", "", new_text)

    for sentence in __pos_tagger__.tag(new_text):
        tokens, pos = zip(*sentence)
        for idx, expr in enumerate(pos):
            if expr in ("N", "ADJ") and len(tokens[idx]) > 2:
                tag = tokens[idx]
                tags.append(tag)

    return tags
