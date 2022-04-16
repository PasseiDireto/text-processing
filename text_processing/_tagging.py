import re

from ._processing import cleanText
from text_processing import pos_tagger


def getKeywords(text, clean_text = True):
    
    """
    Extract keywords from `text`.
    Args:
        text (str):
            String to be processed.
        clean_text (bool):
            If True, `text` is assumed to be clean. 
            Defaults to False.
    Returns:
        list: Keywords as they appear in `text`.
    """
    
    tags = []
    
    if clean_text:
        new_text = cleanText(text, lowercase = True, drop_accents = True)
    else:    
        new_text = text.lower()

    # Remove symbols that are not letters or spaces.    
    if isinstance(new_text, str):
        new_text = re.sub(
            r"[^a-z áâãàéêíóôõúüç-]+", "", new_text
        )

    for sentence in pos_tagger.tag(new_text):
        tokens, pos = zip(*sentence)
        for idx, expr in enumerate(pos):
            if expr in ("N", "ADJ") and len(tokens[idx]) > 2:
                tag = tokens[idx]
                tags.append(tag)

    return tags