# coding=utf-8
a = 10
global b
b = 5
print('\n\noriginal ab')
print(a)
print(b)

'''
ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ЭТО КОСТЫЛЬ, НО ПОКА НОРМ
'''

def global_print_check():
    print('\n\nin func global_print_check ab')
    print(a)
    print(b)


global_print_check()


def local_change_global_var():
    a = 20
    b = 10
    print('\n\nin func local_change_global_var ab')
    print(a)
    print(b)


local_change_global_var()
print('\n\noriginal ab')
print(a)
print(b)


def global_change_global_var():
    global b
    a = 321
    b = 123
    print('\n\nin func global_change_global_var ab')
    print(a)
    print(b)


global_change_global_var()
print('\n\noriginal ab')
print(a)
print(b)
