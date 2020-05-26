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
