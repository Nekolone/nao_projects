# coding=utf-8
""""""
"""
Функции работают также как и в других языках программирования
"""

def fun1():
    print('fun1')


def fun2(a):
    print('fun2 and {}'.format(a))


def fun3(a):
    res = a * 100
    print('fun3 returns {}'.format(res))
    return res


fun1()

fun2('Mark')

a = 5
fun3res = fun3(a)
print(fun3res)
