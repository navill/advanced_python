from __future__ import annotations

from typing import Any, NewType

NewInstance = NewType('InstanceCountingClass', Any)


class InstanceCountingClass:
    instances_created = 0

    def __new__(cls, *args: Any, **kwargs: Any) -> NewInstance:
        print('__new__() called with:', cls, args, kwargs)
        instance: NewInstance = super().__new__(cls)
        instance.number: int = cls.instances_created
        cls.instances_created += 1

        return instance

    def __init__(self, attribute: Any) -> None:
        print('__init__() called with:', self, attribute)
        self.attribute: Any = attribute


def test_func() -> None:
    instance: NewInstance = InstanceCountingClass('attr')
    instance2: NewInstance = InstanceCountingClass('attr')
    instance3: NewInstance = InstanceCountingClass('attr')
    print(instance.number, instance.instances_created)
    print(instance2.number, instance2.instances_created)
    print(instance3.number, instance3.instances_created)


# test_func()

# int instance를 생성하기 전 new 메서드를 이용해 객체 생성 조건을 설정
class NonZero(int):
    def __new__(cls, value):
        return super().__new__(cls, value) if value != 0 else None

    def __init__(self, skipped_value):
        # implementation of __init__ could be skipped in this case
        # but it is left to present how it may be not called
        print("__init__() called")
        super().__init__()  # int(Integer class)를 상속받기 때문에 super().__init__() 필요함


def func_test2():
    print(type(NonZero(10)))
    print(type(NonZero(0)))


func_test2()
