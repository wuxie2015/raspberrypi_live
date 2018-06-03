#! /usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import datetime
from optparse import OptionParser
from gpio_control import *
import wiringpi2 as gpio_wiringpi

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)


def get_data(channel):
    j = 0
    data_list = []
    count_list = []
    laststat = GPIO.HIGH
    GPIO.setup(channel, GPIO.OUT)
    # 发送高-低，低持续18ms以上，然后转为输入加上拉电阻拉高
    GPIO.output(channel, GPIO.HIGH)
    GPIO.output(channel, GPIO.LOW)
    gpio_wiringpi.delayMicroseconds(20)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # 开始接受数据,50us低 + 26-28us高=0，50us低 + 70us高 = 1
    # 如果什么都不写的话，循环一次0.000001088左右
    edge_result = True
    while True:
        t1 = gpio_wiringpi.micros()
        if edge_result is not True:
            break
        read_edge_join(channel,GPIO.FALLING,timeout=1)
        t2 = gpio_wiringpi.micros()
        edge_result = read_edge_join(channel, GPIO.RISING, timeout=1)
        t3 = gpio_wiringpi.micros()
        data_list.append((t1,t2,t3))
    return data_list


def judge_bit(status):
    (t1,t2,t3) = status
    interval1 = t2 - t1
    interval2 = t3 - t2
    if interval2 <40:
        bit = 0
    else:
        bit = 1
    return bit

def process_data(data_tuple_list):
    data_list = []
    for data in data_tuple_list:
        data_list.append(judge_bit(data))
    humidity_bit = data_list[0:8]
    humidity_point_bit = data_list[8:16]
    temperature_bit = data_list[16:24]
    temperature_point_bit = data_list[24:32]
    check_bit = data_list[32:40]

    humidity = 0
    humidity_point = 0
    temperature = 0
    temperature_point = 0
    check = 0
    for i in range(8):
        humidity = humidity + humidity_bit[i] * (2 ** (7 - i))
        humidity_point = humidity_point + \
            humidity_point_bit[i] * (2 ** (7 - i))
        temperature = temperature + temperature_bit[i] * (2 ** (7 - i))
        temperature_point = temperature_point + \
            temperature_point_bit[i] * (2 ** (7 - i))
        check = check + check_bit[i] * (2 ** (7 - i))

    tmp = humidity + humidity_point + temperature + temperature_point
    print("humidity %s.%s temperature %s.%s" %
          (humidity, humidity_point, temperature, temperature_bit))
    if tmp == check:
        result_dict = {
            'humidity': humidity,
            'humidity_point': humidity_point,
            'temperature': temperature,
            'temperature_point': temperature_point,
        }
    else:
        result_dict = {
            'humidity': '',
            'humidity_point': '',
            'temperature': '',
            'temperature_point': '',
        }
    return result_dict


def main(channel):
    channel = int(channel)
    init()
    data_list = get_data(channel)
    result_dict = process_data(data_list)
    print(result_dict)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        "-c",
        "--channel",
        dest="channel",
        help="GPIO CHANNEL",
        metavar="CHANNEL")
    (options, args) = parser.parse_args()
    if options.channel is None:
        parser.error("please input the channel")
    main(options.channel)
