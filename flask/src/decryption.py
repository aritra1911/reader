from typing import List, Optional, Callable

def cycle(ref: str, word: str) -> List[str]:
    res: List[str] = list()
    i = 0

    for c in ref:
        if c.isalpha():
            res.append(word[i])
            i += 1
            if i == len(word):
                i = 0
        else:
            res.append('')
    return res

def get_decrypt_func(key: str) -> Callable[[str], str]:
    return lambda msg: ''.join([
        chr((ord(c) - (65 if not c.islower() else 97) - (ord(s) - 97)) % 26
        + (65 if not c.islower() else 97)) if c.isalpha() else c
        for c, s in zip(msg, cycle(msg, key))
    ])
