def method(self):
    return 1


# 인자에 해당하는 클래스를 생성한다.
# 세번째 인자의 key: 생성될 method 이름, value: 기존의 method
MyClass = type('MyClass', (object,), {'method_': method, 'attr': None})


# 위 코드는 아래 클래스와 동일한 구문
# class MyClass(object):
#     def method_(self):
#         return 1
def func_test():
    my = MyClass()
    print(my.method_())  # <__main__.MyClass object at 0x103993c88>
    print(type(my))
    print(MyClass.__mro__)


# func_test()


# 일반적으로 metaclass는 함수형이 아닌 type을 상속하는 클래스로 사용된다.
class Metaclass(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


# metaclass example
class RevealingMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(mcs, "__new__ called")
        namespace['var'] = 0
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print(mcs, "__prepare__ called")
        # return super().__prepare__(name, bases, **kwargs)
        return {'a': 10}

    def __init__(cls, name, bases, namespace):
        print(cls, "__init__ called")
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        print(cls, "__call__ called")
        return super().__call__(*args, **kwargs)


class RevealingClass(metaclass=RevealingMeta):
    def __new__(cls):
        print(cls, "__new__ called")
        return super().__new__(cls)

    def __init__(self):
        print(self, "__init__ called")
        super().__init__()


inst = RevealingClass()


class SameRevealingClass:
    var = 0

    def __init__(self):
        self.a = 10


print(dir(inst))
print(inst.a, inst.var)
