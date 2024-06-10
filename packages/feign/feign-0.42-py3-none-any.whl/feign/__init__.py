from copy import copy
from inspect import Signature
from types import FunctionType
from typing import Callable


def copy_function(func: FunctionType):
    ret = FunctionType(code=func.__code__, globals=func.__globals__,
                       name=func.__name__, argdefs=func.__defaults__,
                       closure=func.__closure__)
    ret.__kwdefaults__ = copy(func.__kwdefaults__)
    ret.__dict__ = copy(func.__dict__)
    return ret


def feign(obj: Callable, signature: Signature):
    obj.__signature__ = signature
    return obj
