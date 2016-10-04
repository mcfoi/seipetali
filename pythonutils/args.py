__all__ = ('Argument', 'Positional', 'Keyword')


class Argument(object):

    def __init__(self, val):
        self.val = val

    def __call__(self, args=[], kwargs={}):
        return self.val


class Positional(object):

    def __init__(self, pos):
        self.pos = pos

    def __call__(self, args=[], kwargs={}):
        return args[self.pos]


class Keyword(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, args=[], kwargs={}):
        return kwargs[self.name]
