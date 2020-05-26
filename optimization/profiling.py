import pstats
import cProfile
from optimization.myapp import main


# macro-profile: 프로그램(앱) 전체를 실행시켜 성능 측정


# stats.total_calls
def profile_test():
    profile_ = cProfile.run('main()', 'myapp.stats')
    stats = pstats.Stats('myapp.stats')
    stats.sort_stats('time').print_stats(3)
    stats.print_callees('medium')
    stats.print_callees('light')


# micro-profile: 프로그램의 일부(코드)를 실행시켜 성능 측정
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
