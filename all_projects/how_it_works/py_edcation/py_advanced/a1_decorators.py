# coding=utf-8
a = 1
'''
Декоратор - функция которая принимает функцию над которой была поставлена анотация и вовзвращает функцию которая будет
в итоге запущена.
подробнее тут https://tproger.ru/translations/demystifying-decorators-in-python/

selfloop - декоратор который выполняет функцию 10 раз

также в selfloop используется замыкание. А так как в питухоне нету ссылок, используется список zaloop, который можно
использовать как ссылку, в питухоне 3 есть способ обойти костыль со списком.
'''


def main():
    oh_hi_mark()


def selfloop(f):
    zaloop = [10]

    def decorator():
        ''''''
        '''
        В python3 можно использовать параметр nonlocal и обращатся напрямую к переменной zaloop
        Например
        nonlocal zaloop
        zaloop = 22
        '''
        while zaloop[0] > 0:
            f()
            zaloop[0] -= 1

    return decorator


@selfloop
def oh_hi_mark():
    print('Oh hi Mark!')


main()
