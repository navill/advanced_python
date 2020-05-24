class InitOnAccess:
    def __init__(self, klass, *args, **kwargs):
        self.klass = klass
        self.args = args
        self.kwargs = kwargs
        self._initialized = None

    def __get__(self, instance, owner):
        if self._initialized is None:
            print('initialized!')
            self._initialized = self.klass(*self.args,
                                           **self.kwargs)
        else:
            print('cached!')
        return self._initialized


# list("argument")의 초기화는 lazily_initailized에 접근할 때 진행된다.
class MyClass:
    lazily_initialized = InitOnAccess(list, "arguments")


def test_a():
    m = MyClass()
    print(m.lazily_initialized)
    # initialized!
    # ['a', 'r', 'g', 'u', 'm', 'e', 'n', 't']
    print(m.lazily_initialized)
    # cached!
    # ['a', 'r', 'g', 'u', 'm', 'e', 'n', 't']


test_a()


##############################################################

def lazy_property(fn):
    """
    Decorator that makes a property lazy-evaluated.
    """
    attr_name = '_lazy_' + fn.__name__  # _lazy_relatives

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property


class Person:
    def __init__(self, name, occupation):
        self.name = name
        self.occupation = occupation

    @lazy_property
    def relatives(self):  # function name
        # Get all relatives
        relatives = self.name + self.occupation
        return relatives


p = Person('jihoon', 'hi')
print(p.relatives)
# jihoonhi
print(dir(p))
# [..., '_lazy_relatives', ...]
