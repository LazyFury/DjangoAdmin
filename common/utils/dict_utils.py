
def filter_with_allow_keys(dict:dict={},allow_keys=[]):
    for k in dict.copy():
        if k not in allow_keys:
            dict.pop(k)
    return dict