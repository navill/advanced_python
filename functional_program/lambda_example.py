import math
from itertools import count

lm = lambda radius: math.pi * radius ** 2

# lambda 식을 변수에 할당하고 이를 함수처럼 사용할 수 있다.
print(lm(10))
print(map(lambda x: x ** 2, range(10)))
# <map object at 0x10ea09cf8>

print(list(map(lambda x: x ** 2, range(10))))
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


evens = filter(lambda number: number % 2 == 0, range(10))
odds = filter(lambda number: number % 2 != 0, range(10))
print(list(evens))
print(list(odds))

from functools import reduce

print(reduce(lambda a, b: a + b, [2, 2]))
# 4
print(reduce(lambda a, b: a + b, [2, 2, 2]))
# 6
print(reduce(lambda a, b: a + b, range(100)))
# 4950

sequence = filter(
    lambda square: square % 3 == 0 and square % 2 == 1,
    map(
        lambda number: number ** 2,
        count()
    )
)

# 위와 동일한 코드 - generator expressions
# sequence = (
#     square for square
#     in (number ** 2 for number in count())
#     if square % 3 == 0 and square % 2 == 1
# )

print([next(sequence) for _ in range(10)])
# [9, 81, 225, 441, 729, 1089, 1521, 2025, 2601, 3249]


# 무한 루프
def sq(square, square2):
    if square % 3 == 0 and square % 2 == 1:
        return square
