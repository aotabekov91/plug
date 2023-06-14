def register(key=None, info=None, command=True):
    def _key(func):
        def inner(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        inner.key=key
        inner.info=info
        inner.command=command
        inner.__name__=func.__name__
        return inner
    return _key
