
def filter_with_allow_keys(dict:dict={},allow_keys=[]):
    for k in dict.copy():
        if k not in allow_keys:
            dict.pop(k)
    return dict

def filter_with_not_allow_keys(dict:dict={},not_allow_keys=[]):
    for k in dict.copy():
        if k in not_allow_keys:
            dict.pop(k)
    return dict