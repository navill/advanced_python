from __future__ import annotations
from typing import ClassVar, Callable


# 일반 class decorator
def short_repr(cls: ClassVar) -> ClassVar:
    cls.__repr__: str = lambda self: super(cls, self).__repr__()[10:20]
    return cls


@short_repr
class ClassWithRelativelyLongName:
    var: str = 'class name is long'


cl = ClassWithRelativelyLongName()

print(cl)
print(cl.var)


########################################################################
# 매개변수를 이용한 가변 class decorator

def parametrized_short_repr(max_width: int = 8) -> Callable:
    """Parametrized decorator that shortens representation"""

    def parametrized(cls: 'ClassWithRelativelyLongName2') -> 'ShortlyRepresented':
        """Inner wrapper function that is actual decorator"""

        class ShortlyRepresented(cls):
            """Subclass that provides decorated behavior"""

            def __repr__(self) -> str:
                return super().__repr__()[:max_width]

        return ShortlyRepresented

    return parametrized


@parametrized_short_repr(max_width=10)
class ClassWithRelativelyLongName2:
    var: str = 'class name is long'


cl2 = ClassWithRelativelyLongName2()
print(cl2.__repr__())
print(cl2.var)
