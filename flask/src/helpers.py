def cycle(ref, word):
    res = list()
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
