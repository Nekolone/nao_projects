# coding=utf-8
""""""
"""
Локальные и глобальные переменные

Локальные переменные относятся к какой-либо функции и только внутри это функции могут быть изменены. Однако если внутри
функции (как пример main) будет вызвана функция (fun1) то у нее будет доступ к просмотру значения этой локальной
переменной, но не к ее изменению. Также если создать переменную внутри fun1, то для пространства main ее просто не будет
существовать

Глобальные переменные, это переменные которые видны в любой части программы и в каждой функции. Однако для из 
изменения необходимо дать доступ к изменению прописав global (var) перед изменением этой самой переменной. Однако 
использовать глобальные переменные для постоянной передачи каких-либо данных, это плохой стиль и лучше реализовать
общение каким-либо другим образом. В качестве глобальных переменных я считаю лучше использовать какие-то константы.
Число пи, экспонента или еще что-то другое
"""

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
