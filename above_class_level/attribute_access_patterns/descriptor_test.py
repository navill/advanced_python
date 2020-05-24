class MyClass:
    secret_value = 1


mc = MyClass()


def func_test():
    # 인스턴스 속성에 접근하기 위한 방법
    print(mc.__dict__)  # None
    print(MyClass.__dict__)
    print(mc.__getattribute__('secret_value'))
    # instance의 속성이 descriptor인지 검증 -> if False: __dict__에서 해당 속성을 검색
    # -> non-data descriptor(__get__만 구현된 descriptor)인지 확인
    # data descriptor > __dict__ > non-data descriptor 순으로 해당 속성을 검색한다.
    print(getattr(mc, 'secret_value'))


# func_test()
print()


######################################################################

class RevealAccess:
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val  # value를 반환

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val


class MyClass2:
    x = RevealAccess(10, 'var "x"')
    y = 5

    def __getattr__(self, item):
        print('call __getattr__')
        return item

    # call __getattribute__
    def __getattribute__(self, item):
        print('call __getattribute__')
        return item

    # raise AttributeError -> __getattr__ 메서드를 호출한다.
    # def __getattribute__(self, item):
    #     print('raise AttributeError')
    #     raise AttributeError


def func_test2():
    def func():
        pass

    # 일반 함수(+ lambda)는 non-data descriptor
    print(hasattr(func, '__get__'))  # True
    print(hasattr(func, '__set__'))  # False
    print(hasattr(lambda: None, '__get__'))  # True
    print(hasattr(lambda: None, '__set__'))  # False


# func_test2()

def func_test3():
    mc = MyClass2()

    mc.x  # MyClass2.__getattribute__()
    mc.y  # MyClass2.__getattribute__()

    # [Notice: 속성(attribute)과 속성이 갖고 있는 값(value)의 차이]
    # mc.x -> attribute(MyClass2.__getattribute__() 호출)
    print(mc.x)  # x (attribute name)

    # MyClass2.x -> value(RevealAcess.__get__() 호출)
    print(MyClass2.x)  # 10 (value)


func_test3()
