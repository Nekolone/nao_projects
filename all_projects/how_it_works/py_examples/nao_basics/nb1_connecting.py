# coding=utf-8
""""""
import qi

"""
Подключение к интерфейсу нао по его IP, узнать который можно узнать нажав на центральную кнопку
"""

# ip = "NAO_IP"
ip = "192.168.252.250"

session = qi.Session()
session.connect("tcp://" + ip + ":" + "9559")
