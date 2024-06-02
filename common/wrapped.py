

from typing import Callable


class Wrapped(object):
    func:Callable
    ext:dict
    
    def __init__(self,func:Callable,**kwargs) -> None:
        self.func = func
        self.ext = kwargs

    def __call__(self,*args,**kwargs):
        return self.func(*args,**kwargs)
    
    def __str__(self):
        return f"Wrapped({self.func.__name__},{self.ext})"
    

def jsonGetter(func:Callable):
    return Wrapped(func,json=True)

