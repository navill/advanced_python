import time
from typing import Tuple

import requests

SYMBOLS = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')
BASES = ('USD', 'EUR', 'PLN', 'NOK', 'CZK')


def fetch_rates(base: Tuple[str]) -> None:
    response = requests.get(
        f"https://api.exchangeratesapi.io/latest?base={base}"
    )
    response.raise_for_status()
    rates = response.json()["rates"]

    # note: same currency exchanges to itself 1:1
    rates[base] = 1.

    rates_line = ", ".join(
        [f"{rates[symbol]:7.03} {symbol}" for symbol in SYMBOLS]
    )
    print(f"1 {base} = {rates_line}")


from queue import Queue, Empty
from threading import Thread

"""
thread의 limit이 없기 때문에 많은 요청이 한꺼번에 들어올 경우 process가 무한히 늘어날 수 있다.
solution -> ThreadPool + Queue
"""


# 1: Thread
def main1():
    threads = []
    for base in BASES:
        thread = Thread(target=fetch_rates, args=[base])
        thread.start()
        threads.append(thread)

    while threads:
        threads.pop().join()


# 2: ThreadPool + Queue
THREAD_POOL_SIZE = 4


def worker(work_queue):
    while not work_queue.empty():
        try:
            item = work_queue.get(block=False)
        except Empty:
            break
        else:
            fetch_rates(item)
            work_queue.task_done()


def main2():
    work_queue = Queue()
    for base in BASES:
        work_queue.put(base)

    threads = [
        Thread(target=worker, args=(work_queue,))
        for _ in range(THREAD_POOL_SIZE)
    ]

    for thread in threads:
        thread.start()

    work_queue.join()

    while threads:
        threads.pop().join()


if __name__ == "__main__":
    started = time.time()
    print('start main1')
    main2()
    elapsed = time.time() - started
    print("time elapsed: {:.2f}s".format(elapsed))
    print()

    started = time.time()
    print('start main2')
    main2()
    elapsed = time.time() - started
    print("time elapsed: {:.2f}s".format(elapsed))
