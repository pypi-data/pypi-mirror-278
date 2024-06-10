import functools


def compose(*functions):
    """Function composition with functools.reduce"""
    return functools.reduce(
        lambda f, g: lambda *args, **kwargs: f(g(*args, **kwargs), **kwargs), functions
    )
