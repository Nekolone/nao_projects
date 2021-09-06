# coding=utf-8
""""""
"""
Map используется для применения какой-либо функции к массиву(ам) данных

Как пример домножить массив из N элементов на какое-то значение. В базовой библиотеке просто написать M(nm)*3,
не получится, поэтому можно использовать map.

В python3 немного меняется синтаксис и такие функции как map и filter больше не возвращают значение типа List, поэтому
необходимо преобразовать в него
"""


def my_func(*args):
    return sum(filter(lambda x: x is not None, args))


x = map(my_func, [1,2], [2,3], [3,4], [4, 1], [5, 9])
# x = list(map(my_func, [1,2], [2,3], [3,4], [4, 1], [5, 9]))
print(x)

ess = map(lambda i: i.swapcase(), ['lowertext', 'mIxEdTeXt', 'UPPERTEXT'])
# ess = list(map(lambda i: i.swapcase(), ['lowertext', 'mIxEdTeXt', 'UPPERTEXT']))
print(ess)
