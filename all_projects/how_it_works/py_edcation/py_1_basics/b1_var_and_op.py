# coding=utf-8
""""""
"""
Python это язык с динамической типизацией, это значит что переменные сами понимают какого типа они будут в данный 
момент, а не строго задаются как в том же C++
"""

a = 10 + 20.55
print(a)

a = 'Oh, ' + 'hi Mark!'
print(a)

a = 'one = ' + str(1)
print(a)

mem = 'python makes '
print(mem + 'br' * 50)


"""
Также есть несколько вариантов форматирования текста, но лично мне больше всего нравится .format
"""
one = 1
two = 2
print('one, two, three = {},{},{}'.format(one, two, 3))
