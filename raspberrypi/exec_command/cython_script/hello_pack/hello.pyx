# coding=utf-8
import wiringpi

cdef test_1():
    for i in range(0, 4):
        t1 = wiringpi.micros()
        wiringpi.delayMicroseconds(20)
        t2 = wiringpi.micros()
        print t2 - t1

def print_hello(name):
    test_1()
test_1()
