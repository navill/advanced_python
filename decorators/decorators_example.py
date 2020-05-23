# Checking arguments

from functools import wraps

rpc_info = {}


def xmlrpc(in_=(type(None)), out=(type(None),)):
    """
    데커레이터에 매개변수를 사용하고자 할 경우 함수를 세개 이용한다.

    :param in_: 데커레이터에서 검증할 데이터 타입 지정
    :param out: 예상 결과의 타입
    :return: decorator의 중간 함수(_xmlrpc)
    """

    def _xmlrpc(function):
        # registering the signature
        func_name = function.__name__
        rpc_info[func_name] = (in_, out)

        # check types
        def _check_types(elements, types):
            """Subfunction that checks the types."""
            if len(elements) != len(types):
                raise TypeError('argument count is wrong')
            typed = enumerate(zip(elements, types))
            for index, couple in typed:
                arg, of_the_right_type = couple
                if isinstance(arg, of_the_right_type):
                    continue
                raise TypeError(
                    'arg #%d should be %s' % (index,
                                              of_the_right_type))

        # wrapped function
        @wraps(function)
        def __xmlrpc(*args):  # no keywords allowed
            # checking what goes in
            checkable_args = args[1:]  # removing self
            _check_types(checkable_args, in_)
            # running the function
            res = function(*args)

            # checking what goes out
            if not type(res) in (tuple, list):
                checkable_res = (res,)
            else:
                checkable_res = res
            _check_types(checkable_res, out)
            # the function and the type
            # checking succeeded
            return res

        return __xmlrpc

    return _xmlrpc


class RPCView:
    @xmlrpc(in_=(int, int))  # two int -> None
    def accept_integers(self, int1, int2):
        print('received %d and %d' % (int1, int2))

    @xmlrpc(in_=(str,), out=(int,))  # string -> int
    def accept_phrase(self, phrase):
        print('received %s' % phrase)
        return 12

    @xmlrpc(out=(int,))  # string -> int
    def accept_phrase2(self):
        print('received ?')
        return 12


def check_args_func():
    print(rpc_info)
    # {'accept_integers': ((<class 'int'>, <class 'int'>), (<class 'NoneType'>,)),
    # 'accept_phrase': ((<class 'str'>,), (<class 'int'>,)), 'accept_phrase2': (<class 'NoneType'>, (<class 'int'>,))}
    my = RPCView()
    my.accept_integers(1, 2)
    # received 1 and 2
    # my.accept_phrase(2)
    # Traceback (most recent call last):
    #  File "<input>", line 1, in <module>
    #  File "<input>", line 26, in __xmlrpc
    #  File "<input>", line 20, in _check_types
    # TypeError: arg #0 should be <class 'str'>
    print()


# check_args_func()

####################################################################################
# Caching
"""This module provides simple memoization arguments
that is able to store cached return results of
decorated function for specified period of time.
"""
import time
import hashlib
import pickle

cache = {}


def is_obsolete(entry, duration):
    """Check if given cache entry is obsolete"""

    return time.time() - entry['time'] > duration


def compute_key(function, args, kwargs):
    """Compute caching key for given value"""

    # pickle에 사용되는 인자가 thread 또는 socket 데이터일 경우 에러가 발생할 수 있다.
    key = pickle.dumps((function.__name__, args, kwargs))
    return hashlib.sha1(key).hexdigest()


def memoize(duration=10):
    def _memoize(function):
        def __memoize(*args, **kwargs):
            key = compute_key(function, args, kwargs)

            # 캐시에 데이터가 있거나 지정된 시간을 초과하지 않았을 경우
            if (
                    key in cache and
                    not is_obsolete(cache[key], duration)
            ):
                # cache 값 반환
                print('return value in cache')
                return cache[key]['value']

            result = function(*args, **kwargs)
            # cache 값 생성
            cache[key] = {
                'value': result,
                'time': time.time()
            }
            return result

        return __memoize

    return _memoize


@memoize()
def very_very_very_complex_stuff(a, b):
    return a + b


def cache_func():
    print(very_very_very_complex_stuff(2, 2))  # return result(4)
    print(cache)  # {'c4ba025dbed84bd8eb75d4beacf6900922117068': {'value': 4, 'time': 1590215866.793895}}
    print(very_very_very_complex_stuff(2, 2))  # return value in cache
    time.sleep(10)  # wait 10 sec
    print(very_very_very_complex_stuff(2, 2))  # return result(4)
    print()


# cache_func()

####################################################################################
# Porxy


class User(object):
    def __init__(self, roles):
        self.roles = roles


class Unauthorized(Exception):
    pass


def protect(role):
    def _protect(function):
        def __protect(*args, **kw):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("I won't tell you")
            return function(*args, **kw)

        return __protect

    return _protect


# 사용자의 role 설정
tarek = User(('admin', 'user'))
bill = User(('user',))


class RecipeVault(object):
    @protect('admin')
    def get_waffle_recipe(self):
        print('use tons of butter!')


def proxy_func():
    my_vault = RecipeVault()
    # decorator에서 globals().get('user')를 이용해 user값을 가져옴
    user = tarek
    my_vault.get_waffle_recipe()
    # use tons of butter!
    user = bill
    my_vault.get_waffle_recipe()  # -> protect('admin')에 적합하지 않으므로 raise Exception
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "<stdin>", line 7, in wrap
    # __main__.Unauthorized: I won't tell you


# proxy_func()

####################################################################################
# Context Provider

from threading import RLock

lock = RLock()


def synchronized(function):
    def _synchronized(*args, **kw):
        lock.acquire()
        try:
            return function(*args, **kw)
        finally:
            lock.release()

    return _synchronized


@synchronized
def thread_safe():  # make sure it locks the resource
    pass
