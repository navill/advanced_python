# list

from bisect import bisect_left
from collections import defaultdict
from timeit import timeit


def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError


def list_indexing_test():
    li = ['a', 'b', 'c', 'd', 'e', 'f', 'g', ]
    idx = index(li, 'c')
    print(idx)


# unique list = O(n^2)
def unique_value_list():
    sequence_ = ['a', 'a', 'b', 'c', 'c', 'd']
    result = []
    for element in sequence_:
        if element not in result:
            result.append(element)
    print(result)
    # ['a', 'b', 'c', 'd']


# set = O(n)
def set_test():
    sequence = ['a', 'a', 'b', 'c', 'c', 'd']
    unique = set(sequence)
    print(unique)
    # {'a', 'c', 'b', 'd'}


# deque
import timeit


def timeit_test():
    # 단순 append + pop은 list와 deque의 차이가 크지 않음
    print(timeit.timeit(stmt='seq.append(0); seq.pop();', setup='seq=list(range(100));'))
    # 0.132167799
    print(
        timeit.timeit(stmt='seq.append(0); seq.pop();', setup='from collections import deque; seq=deque(range(100));'))
    # 0.109020510

    # insert를 통해 sec[0]에 값을 입력할 경우 큰 차이를 보임
    print(timeit.timeit(stmt='seq.insert(0, 0); seq.pop();', setup='seq=list(range(10000))'))
    # 7.241453971
    print(timeit.timeit(stmt='seq.appendleft(0); seq.pop();',
                        setup='from collections import deque; seq=deque(range(10000));'))
    # 0.114893928


def defaultdict_test():
    s = 'mississippi'
    d = defaultdict(int)
    for k in s:
        d[k] += 1

    print(list(d.items()))
    # [('i', 4), ('p', 2), ('s', 4), ('m', 1)]


# defaultdict_test()

from collections import namedtuple


def namedtuple_test():
    Customer = namedtuple('Customer', 'firstname lastname')
    c = Customer('Tarek', 'Ziadé')
    print(c.firstname)  # class의 속성처럼 호출
    # Tarek

    first, last = c  # 일반 tuple 처럼 unpacking
    print(first, last)
    # Tarek Ziadé

    d = c._asdict()  # dictionary로 변환
    print(d['firstname'])
    # Tarek


namedtuple_test()
