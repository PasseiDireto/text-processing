import re

from ._processing import cleanText
from text_processing import pos_tagger


def getKeywords(text, text_is_clean = False):
    
    """
    Extract keywords from `text`.
    Args:
        text (str):
            String to be processed.
        text_is_clean (bool):
            If True, do not apply text preprocessing
            before keyword extraction. Defaults to False.
    Returns:
        list: Keywords as they appear in `text`.
    """
    
    tags = []
    
    if text_is_clean:
        new_text = text
    else:    
        new_text = cleanText(text, keep_accents = False)

    # Remove symbols that are not letters or spaces.    
    if isinstance(new_text, str):
        new_text = re.sub(
            r"[^a-z áâãàéêíóôõúüç-]+", "", new_text.lower()
        )

    for sentence in pos_tagger.tag(new_text):
        tokens, pos = zip(*sentence)
        for idx, expr in enumerate(pos):
            if expr in ("N", "ADJ") and len(tokens[idx]) > 2:
                tag = tokens[idx]
                tags.append(tag)

    return tags