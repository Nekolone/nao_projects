# coding=utf-8
''''''
'''
В случае если нужно передавать большое количество данных, структуры в функцию, лучше из запаковать.
Функция которая принимает чрезмерное количество аргументов, это плохой стиль, который приводит к плохой читабельности
кода.
'''


def bad_foo(a, b, c, d, e, f, g, h, i):
    print a


'''
ЭКВИВАЛЕН
'''


def good_foo(args):
    print (args[0])


def good_foo_2(*args):
    print (args[0])


def good_foo_3(**kwargs):
    print (kwargs['a'])
    print (kwargs['c'])


bad_foo(1, 2, 3, 4, 5, 6, 7, 8, 9)
params = [1, 2, 3, 4, 5, 6, 7, 8, 9]

good_foo(params)

good_foo_2(1, 2, 3, 4, 5, 6, 7, 8, 9)
good_foo_2(*params)

m = {'a': 1, 'b': 2, 'c': 3}
good_foo_3(c=3, b=2, a=1)
good_foo_3(**m)

'''
----------------------------------
'''

list_one = [1, 2, 3]
l1, l2, l3 = list_one

tuple_one = (1, 2, 3)
t1, t2, t3 = tuple_one
