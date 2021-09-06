# coding=utf-8
""""""
"""
Примеры функционального программирования
в нему можно отнести
-map
-filter
-lambda
-reduce
-currying
-first class functions
-higher order functions
"""

pow = lambda l: reduce(lambda x1, x2: x1 ** x2, l)
l = [3, 1, 2, 3]
print(pow(l))
