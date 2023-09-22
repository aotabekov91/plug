from functools import wraps

def register(key=None, modes=[], **kwargs):

    def _register(func):

        @wraps(func)
        def inner(self, *args, **kwargs): 
            return func(self, *args, **kwargs)

        inner.key=key
        inner.func=func
        inner.modes=modes
        inner.kwargs=kwargs
        inner.name=func.__name__

        return inner

    return _register
