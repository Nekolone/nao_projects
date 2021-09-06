# coding=utf-8
''''''
'''
Продолжая тему функций первого класса, к ним также относится lambda
Lambda это небольшая анонимная функция
'''


def simp_fun(var):
    return var + 1337


x = simp_fun

print(x(98))
'''
ЭКИВАЛЕНТ
'''

y = lambda var: var + 1337

print(y(98))

'''
Примеры использования
'''
x = lambda a: a + 10
print(x(22))

d = lambda a, b, c: a + b + c
print(d(1, -6, 9))


def test(a):
    print(a())


var = 1337
get_new_var = lambda: var
test(get_new_var)
var = 111
test(get_new_var)
