import re
import unicodedata


def rSub(text, repl, flags = 0, **kwargs):
    
    """
    Recursive string replacement by multiple regex patterns.
    Args:
        text (str):
            Text to be processed.
        repl (str):
            replacement value.            
        pattern1, pattern2, ... (str):
            regex patterns to lookout for 
            (first is mandatory, rest is optional).
        flags (int, optional):
            flags to be passed to the regex engine. 
            Defaults to 0.    
    Example:
        Input:
            >> text = 'O rato roeu a roupa do rei de Roma.'
            >> result = rSub(text, repl=r"-", pattern1=r'(roupa)', pattern2=r'([aeiou])')
            >> print(result)
        Output:
            >> 'O rato roeu a r--p- do rei de Roma.'
        The first pattern found a match for the word 'roupa'.
        The second pattern found vowels inside the word 'roupa'.
        Replacement for the final matches took place, replacing 
        vowels in 'roupa' by '-'.
    Obs.: Always encapsulate patterns within parentheses.  
    """    
    
    kwargs.update(
        {
            k: re.compile(v, flags)
            for k, v in kwargs.items()
            if k.startswith("pattern")
        }
    )

    kwargs["pos"] = 0
    
    pats = [
        kwargs[k] 
        for k in sorted(kwargs.keys()) 
        if k.startswith("pattern")
    ]
    
    def _sub(match):
        kwargs["pos"] += 1
        if kwargs["pos"] == len(pats) - 1:
            kwargs["pos"] = 0
            return pats[-1].sub(repl, match.groups()[0])
        return pats[pos].sub(_sub, match.groups()[0])
    
    def sub(text):
        if len(pats) == 1:
            return pats[0].sub(repl, text)
        return pats[kwargs["pos"]].sub(_sub, text)

    return sub(text)


def removeBadChars(text):
    
    pattern = r"([^a-z\s0-9&#@=><\+\/\*\^,\.;:!?_\-\)\(\]\[\}\{áâãàéêíóôõúç]+)"
    chars = re.compile(pattern, flags = 2)
    
    def _repl(match):
        return chars.sub(
            " ",
            unicodedata.normalize("NFKD", match.groups()[0])
            .encode("ascii", errors="ignore")
            .decode("utf-8", errors="ignore"),
        )

    return chars.sub(_repl, text)


def removeRepetitions(text):

    # Repetitions of non-alphanumerical chars.
    pattern = r"([^a-záâãàéêíóôõúç0-9\s])\1+"
    new_text = rSub(
        text, repl = r"\1", pattern1 = pattern, flags = 2
    )

    # Repetitions of words separated by a space.
    pattern = r"\b(\w+)( \1\b)+"

    return rSub(
        new_text, repl = r"\1", pattern1 = pattern, flags = 2
    )


def replaceEmails(text, by = " "):
    pattern = re.compile(
        r"([A-Z0-9_.+-]+@[A-Z0-9-]+(?:\.[A-Z0-9-]+)+)", flags = 2
    )
    return pattern.sub(by, text)


def replaceUrls(text, by = " "):
    pattern = re.compile(
        r"((https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))",
        flags = 2,
    )
    return pattern.sub(by, text)


def reformatAbbreviations(text):
    return rSub(
        text, repl = r"", pattern1 = r"((:?[A-Z]+\.)+)", pattern2 = r"(\.)"
    )


def adjustSpacing(text):

    # Spacing around punctuation.
    new_text = rSub(
        text, repl = r" \1 ", pattern1 = r"([^\w\d\s]+)", flags = 2
    )

    # Collapse multiple spaces into one.
    new_text = rSub(
        new_text, repl = r" ", pattern1 = r"(\s+)", flags = 2
    )
    
    return new_text.strip()


def removeAccents(text):
    """
    Replace accented characters from `text`.
    Args:
        text (str):
            String to be processed.
    Returns:
        str: processed `text`.
    """    
    return "".join(
        c for c in unicodedata.normalize("NFD", text) 
        if unicodedata.category(c) != "Mn"
    )


def cleanText(text, lowercase = True, drop_accents = True):
    """
    Regex-based text processing.
    Args:
        text (str):
            String to be processed.
        lowercase (bool):
            If True, output will be in lowercase.
            Defaults to True.
        drop_accents (bool, optional):
            If True, normalize accented characters. 
            Defaults to True.
    Returns:
        str: processed `text`.
    """
    
    new_text = adjustSpacing(
            replaceUrls(
                replaceEmails(
                    removeRepetitions(
                        reformatAbbreviations(
                            removeBadChars(text.lower() if lowercase else text)
                        )
                    )
                )
            )
        )

    new_text = new_text.replace(
        "\r", " "
    ).replace(
        "\t", " "
    ).replace(
        "\n", " "
    )

    if drop_accents:
        return removeAccents(new_text)
    
    return new_text
