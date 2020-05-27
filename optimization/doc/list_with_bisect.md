# Data Structure & Collections

[list](#list---bisect)

[set](set)

[deque](deque)

[defaultdict](defaultdict)

[namedtuple](namedtuple)



### List - Bisect

- 정렬된 순서를 유지하는 리스트를 다른 타입으로 변경하기 어려운 상태에서 검색('in' 또는 indexing)을 사용하고자 할 때 bisect를 이용할 수 있다.

  ```python
  from bisect import bisect_left
  
  
  def index(a, x):
      'Locate the leftmost value exactly equal to x'
      i = bisect_left(a, x)
      if i != len(a) and a[i] == x:
          return i
      raise ValueError
  
  
  li = ['a', 'b', 'c', 'd', 'e', 'f', 'g', ]
  idx = index(li, 'c')
  print(idx)  # 2
  ```

  

### Set

- 순서를 유지하면서 값의 중복을 허용하지 않을 때 set을 사용할 수 있다.

  ```python 
  # unique list
  sequence = ['a', 'a', 'b', 'c', 'c', 'd']
  result = []
  for element in sequence:
      if element not in result:
          result.append(element)
  print(result)
  # ['a', 'b', 'c', 'd']
  
  # set
  sequence = ['a', 'a', 'b', 'c', 'c', 'd']
  unique = set(sequence)
  print(unique)
  # {'a', 'c', 'b', 'd'} 
  ```

  

## Collections

### deque

- double-linked list 형태의 배열

- append(끝에 값 추가)가 아닌 insert(해당 인덱스에 값 추가)에서 list보다 더 좋은 성능

- 임의의 index에 접근할 경우 나쁜 성능

  ```python
  import timeit
  
  # 단순 append + pop은 list와 deque의 차이가 크지 않음
  print(timeit.timeit(stmt='seq.append(0); seq.pop();', setup='seq=list(range(100));'))
  # 0.132167799
  print(timeit.timeit(stmt='seq.append(0); seq.pop();', setup='from collections import deque; seq=deque(range(100));'))
  # 0.109020510
  
  # insert를 통해 sec[0]에 값을 입력할 경우 큰 차이를 보임
  print(timeit.timeit(stmt='seq.insert(0, 0); seq.pop();', setup='seq=list(range(10000))'))
  # 7.241453971
  print(timeit.timeit(stmt='seq.appendleft(0); seq.pop();',
                      setup='from collections import deque; seq=deque(range(10000));'))
  # 0.114893928
  ```

  

### defaultdict

- dict.setdefault() 보다 더 좋은 성능

- 값이 없을 경우 매개변수에 전달된 값으로 초기화

  ```python
  s = 'mississippi'
  d = defaultdict(int)
  for k in s:
      d[k] += 1
  
  print(list(d.items()))
  # [('m', 1), ('i', 4), ('s', 4), ('p', 2)]
  ```

  

### namedtuple

- class factory 일종

- tuple과 동일한 특성: 불변 객체이면서 초기화 시 배열의 저장 크기가 지정됨

- dict 보다 더 좋은 메모리 효율

  ```python
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
  ```

  