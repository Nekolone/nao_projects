# coding=utf-8
""""""
"""
Момоизация это один из способов оптимизации кода, путем запоминания результатов некоторых функций и при последующем
вызове которых будут получены уже известные результаты. Другими словами можно сказать что мемоизация это кэширование, 
но в более узком понятии этого слова

В нашем случае это будет функция по поиску числа Фибоначчи.

А для получения времени исполнения используется декоратор @clock
"""

import time


def clock(func):
    def clocked(*args, **kwargs):
        t0 = time.time()

        result = func(*args, **kwargs)  # вызов декорированной функции

        elapsed = time.time() - t0
        name = func.__name__
        arg_1st = []
        if args:
            arg_1st.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_1st.append(', '.join(pairs))
        arg_str = ', '.join(arg_1st)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked

@clock
def simp_fib(n):
    if n<2:
        return n
    return simp_fib(n-2) + simp_fib(n-1)



print('fib(20) = ', simp_fib(25))
# print('fib(20) = ', simp_fib(40))

_fib_cache = {1:1, 2:1}

@clock
def mem_fib(n):
    result = _fib_cache.get(n)
    if result is None:
        result = mem_fib(n-2) + mem_fib(n-1)
        _fib_cache[n] = result
    return result

print ('mem_fib(100) =', mem_fib(100))