from typing import Union, Callable
import functools

from pydantic import validate_call

from returns.result import safe
from returns.pointfree import bind
from returns.pipeline import pipe


def tidyworkflow(section: str = None):
    """
    Tidyworkflow is a functional programming paradigm with extra built-in sugar.

    Examples
    ========
    @tidyworkflow(section="String Processing")
    def preprocess_string(s: str, **kwargs) -> str:

        def normalize_string(s: str) -> str:
            '''Strip ends of string and replace intermediate puncutation, spaces with single space.'''
            s = re.compile(f"^[{string.punctuation}]+").sub("", s)
            s = re.compile(f"[{string.punctuation}]+$").sub("", s)
            s = re.compile(f"[{string.punctuation}{string.whitespace}]+").sub(" ", s)
            return s

        def replace_string(s: str) -> str:
            '''Replace instances of `char` with `repl`'''
            char: str = kwargs.get("char", "-")
            repl: str = kwargs.get("repl", "_")
            return re.sub(re.compile(re.escape(char)), repl, s)

        def string_to_case(s: str) -> str:
            '''Convert string to specified case'''
            case: str = kwargs.get("case", "lower")
            return getattr(str, case)(s)

        return locals()


    ### run tidyworkflow examples
    >>> preprocess_string("something here")
    >>> preprocess_string("something here", case="lower")
    >>> preprocess_string("something here", char="he", repl="+", case="capitalize")

    ### obtain context from tidyworkflow
    >>> tidyworkflow.context
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # get locals() dictionary from decorated function
            func_locals = func(*args, **kwargs)
            # separate components into respective categories
            func_args = [
                v
                for v in func_locals.values()
                if not isinstance(v, Union[dict, Callable])
            ]
            func_callables = [
                safe(validate_call(v, config=dict(arbitrary_types_allowed=True)))
                for v in func_locals.values()
                if isinstance(v, Callable)
            ]
            # compose, call functions
            func_queue = pipe(func_callables[0], *map(bind, func_callables[1:]))
            result = func_queue(*func_args)
            # create context given successful result
            if section is not None:
                if not hasattr(tidyworkflow, "context"):
                    tidyworkflow.context = dict()
                tidyworkflow.context[section] = [fc.__doc__ for fc in func_callables]

            return result

        return wrapper

    return decorator
