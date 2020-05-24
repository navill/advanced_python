class Frozen:
    __slots__ = ['ice', 'cream']


print('__dict__' in dir(Frozen))
print('ice' in dir(Frozen))
frozen = Frozen()
print(frozen.__slots__)
frozen.ice = True
frozen.cream = None
# frozen.icy = True  # -> raise error: 동적으로 속성을 추가할 수 없다.


# Monkey patch와 같은 동적 기술이 slots이 정의된 클래스의 인스턴스에 접근하려 할 때
# 동작이 어려울 수 있기 때문에 주의
class Unfrozen(Frozen):
    pass


unfrozen = Unfrozen()
unfrozen.icy = False
print(unfrozen.icy)
print(unfrozen.__dict__)  # icy는 Unfrozen의 속성이므로 동적으로 추가할 수 있다.