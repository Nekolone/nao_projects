# coding=utf-8
""""""
"""
ООП, Объектно ориентированное программирование - это стиль написания кода, для обеспечения понятности кода и возможности
поддержек и или изменения его в будущем. 
"""


class MyClass:
    def __init__(self, my_var=1, my_var2=2):
        """"""
        """
        __init__ - конструктор класса
        """
        self.my_var = my_var
        self.my_var2 = my_var2

    def __add__(self, other):
        """"""
        """
        операторная функция, вызывается при складывании двух экземпляров. В итоге возвращает новый экземпляр
        """
        return MyClass(self.my_var + other.my_var, self.my_var2 + other.my_var2)

    def my_method(self):
        """"""
        """
        my_method - созданный нами метод, который выводит значение my_var, привязанного к экземпляру класса
        """
        print(self.my_var)
        print(self.my_var2)

    def print_my_text(self, text):
        print(self.my_var, self.my_var2, text)

"""
var22 - экземпляр класса MyClass
var22 = MyClass(22, 10) - создаем экземпляр класса MyClass, передавая значение 22 и 10 в конструктор
.my_method - метод класса MyClass
var22.my_method() - вызов метода экземпляра класса MyClass.

new_var = var22 + var55 - суммирование двух экземпляров класса благодаря реализованной операторной функции
"""

var22 = MyClass(22, 10)
var22.my_method()
var22.print_my_text('Hi Mark1')

var55 = MyClass(55, 27)
var55.my_method()
var55.print_my_text('Hi Mark2')

new_var = var22 + var55
new_var.my_method()
new_var.print_my_text('Hi Mark SUM')