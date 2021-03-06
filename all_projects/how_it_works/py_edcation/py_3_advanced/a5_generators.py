# coding=utf-8
""""""
"""
Генератор, это объект который сразу при создании не вычисляет значения всех элементов, а только по вызову. Хранит в
памяти только последний вычисленный элемент и правило перехода к следующему. Вычисление следующего происходит по вызову
next()

(цикл for же уже включает в себя next, поэтому если мы проходимся по генератору в цикле, то прописывать next() не нужно)
"""


def f_gen(a):
    for i in range(1, a):
        yield i ** 2


a = f_gen(6)

print(a)
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))

b = (i ** 2 for i in range(1, 6))
print(b)
for i in b:
    print(i)
