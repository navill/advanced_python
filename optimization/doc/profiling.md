# Profiling

### Profiling은 따로 공부가 필요함(pstats, profile, cProfile, timeit, ...)

- profile: 파이썬 기본 프로파일
- cProfile: C 기반 프로파일(profile보다 오버헤드가 적다)

```python
import time


def medium():
    time.sleep(0.01)


def light():
    time.sleep(0.001)


def heavy():
    for i in range(100):
        light()
        medium()
        medium()
    time.sleep(2)


def main():
    for i in range(2):
        heavy()


if __name__ == '__main__':
    main()
```



![image-20200526162134294](/Users/jh/Desktop/Python/advanced/optimization/doc/image-20200526162134294.png)

- ncalls: 전체 호출 수 
- tottime: 전체 소요 시간(하위 함수 호출 제외)
- cumtime: 전체 소요 시간(호위 함수 호출 포함)

- percall(첫 번째): tottime / ncalls
- percall(두 번째): cumtime / ncalls





### Macro-Profile:  프로그램 전체를 실행시켜 성능 검사

```python
import pstats
import cProfile
from optimization.myapp import main

profile = cProfile.run('main()', 'myapp.stats')
stats = pstats.Stats('myapp.stats')
# stats.total_calls

stats.sort_stats('time').print_stats(3)
stats.print_callees('medium')
stats.print_callees('light')
"""
Tue May 26 16:45:11 2020    myapp.stats

         1208 function calls in 9.004 seconds

   Ordered by: internal time
   List reduced from 8 to 3 due to restriction <3>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      602    8.993    0.015    8.993    0.015 {built-in method time.sleep}
      400    0.005    0.000    4.711    0.012 optimization/myapp.py:4(medium)
        2    0.004    0.002    9.003    4.502 optimization/myapp.py:12(heavy)

   Ordered by: internal time
   List reduced from 8 to 1 due to restriction <'medium'>

Function                called...
                        ncalls  tottime  cumtime
myapp.py:4(medium)  ->     400    4.707    4.707  {built-in method time.sleep}


   Ordered by: internal time
   List reduced from 8 to 1 due to restriction <'light'>

Function               called...
                       ncalls  tottime  cumtime
myapp.py:8(light)  ->     200    0.284    0.284  {built-in method time.sleep}



Process finished with exit code 0
"""
```

- pstats & cProfile 사용법에 대한 공부가 필요함



```python
$ gprof2dot -f pstats myapp.stats | dot -Tpng -o output.png
```

<img src="/Users/jh/Desktop/Python/advanced/optimization/output.png" alt="output" style="zoom:50%;" />





```python
import time
import tempfile
import cProfile
import pstats


def profile(column='time', list=3):
    def parametrized_decorator(function):
        def decorated(*args, **kw):
            s = tempfile.mktemp()

            profiler = cProfile.Profile()
            profiler.runcall(function, *args, **kw)
            profiler.dump_stats(s)

            p = pstats.Stats(s)
            print("=" * 5, f"{function.__name__}() profile", "=" * 5)
            p.sort_stats(column).print_stats(list)

        return decorated

    return parametrized_decorator


def medium():
    time.sleep(0.01)


@profile('time')
def heavy():
    for i in range(100):
        medium()
        medium()
    time.sleep(2)


@profile('time')
def main():
    for i in range(2):
        heavy()


if __name__ == '__main__':
    main()
    
    
"""
===== heavy() profile =====
Tue May 26 16:52:43 2020    /var/folders/p8/7tt65m7j1pn0vvwpjgb0n5wh0000gn/T/tmp7391ky3e

         403 function calls in 4.348 seconds

   Ordered by: internal time
   List reduced from 4 to 3 due to restriction <3>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      201    4.344    0.022    4.344    0.022 {built-in method time.sleep}
      200    0.002    0.000    2.344    0.012 .../optimization/profiling.py:43(medium)
        1    0.002    0.002    4.348    4.348 .../optimization/profiling.py:47(heavy)


===== heavy() profile =====
Tue May 26 16:52:47 2020    /var/folders/p8/7tt65m7j1pn0vvwpjgb0n5wh0000gn/T/tmpsys5lee6

         403 function calls in 4.356 seconds

   Ordered by: internal time
   List reduced from 4 to 3 due to restriction <3>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      201    4.352    0.022    4.352    0.022 {built-in method time.sleep}
      200    0.002    0.000    2.352    0.012 .../optimization/profiling.py:43(medium)
        1    0.002    0.002    4.356    4.356 .../optimization/profiling.py:47(heavy)


===== main() profile =====
Tue May 26 16:52:47 2020    /var/folders/p8/7tt65m7j1pn0vvwpjgb0n5wh0000gn/T/tmpgcv258u3

         69 function calls in 8.710 seconds

   Ordered by: internal time
   List reduced from 27 to 3 due to restriction <3>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    8.710    8.710    8.710    8.710 {method 'enable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 {built-in method posix.lstat}
        8    0.000    0.000    0.000    0.000 .../python3.7/random.py:224(_randbelow)



Process finished with exit code 0
"""

```

