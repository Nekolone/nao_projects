# coding=utf-8
""""""
"""
К встроенным функциям высшего порядка, которые можно использовать без импорта сторонних библиотек, относятся
map и filter, которые мы разобрали ранее

Функция высшего порядка = Higher Order Function = HOF
Это функция которая может принимать в качестве аргумента и/или возвращать функцию как результат работы

Примеры встроенных функций filter и map уже разобрали, поэтому напишу свою небольшую функцию
"""


def pprint(text):
    print ('text - ', text)


def another_pprint(text):
    print ('another pprint - ', text)


def call_with_five(function):
    function(5)


"""
Принимает любую функцию, выполняет ее и возвращает функцию another_print, которую в последствии мы вызывает с 
аргументом 'another text'
"""


def call_foo_return_another_print(fun):
    fun()
    return lambda x: another_pprint(x)


call_with_five(pprint)

call_foo_return_another_print(lambda: pprint("some text"))('another text')
#
# def mutiplier(op1):
#     return lambda op2: op1 * op2
#
#
# three_mul = mutiplier(3)
#
# print(three_mul(2))
# print(mutiplier(5)(3))
#
