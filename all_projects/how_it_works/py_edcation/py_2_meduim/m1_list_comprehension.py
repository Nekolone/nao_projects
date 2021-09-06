# coding=utf-8
''''''
'''
Сокращенная и более понятная запись цикла
'''

var_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

res1 = []
for i in var_list:
    if i > 5:
        res1.append(i)

res2 = [i for i in var_list if i > 5]

print (res1)
print (res2)
