# coding=utf-8
''''''
'''
Словарь, можно сказать что это структура данных с возможностью нахождения нужной ячейки по ключу
'''

def f():
    print('patric functional')

dic = {
    'name': 'Patric',
    'role': 1,
    'functional': f
}

print(dic['name'])
print(dic['role'])

'''
после выполнения dic['functional'] мы получили функцию и выполнили ее добавив ()
'''
dic['functional']()