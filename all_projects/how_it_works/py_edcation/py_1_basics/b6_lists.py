# coding=utf-8
""""""
'''
Списки в python, это проиндексированная коллекция элементов как одного так и различных типов.

Грубо говоря это массив в котором можно хранить различные типы данных. 
'''


def my_func():
    pass


list_one = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list_two = [1, '2', my_func]


"""
.append() - добавляет элемент в конец списка
.pop() - возвращает последний элемент
len() - возвращает длину списка
"""
list_one.append(10)
list_one.pop()
len(list_one)