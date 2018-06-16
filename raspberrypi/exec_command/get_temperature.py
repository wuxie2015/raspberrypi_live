#! /usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
from optparse import OptionParser
from setting import HOST
import wiringpi2 as gpio
import time
import urllib
import urllib2

def init(channel):
    gpio.wiringPiSetup()
    gpio.pinMode(channel, gpio.OUTPUT)#设置针脚为输出状态
    gpio.piHiPri(99)

def reinit(channel):
    gpio.pinMode(channel, gpio.OUTPUT)  # 设置针脚为输出状态

def get_data(channel):
    tl = []
    gpio.digitalWrite(channel, gpio.HIGH)  # 输出高电平
    gpio.delay(1)
    ###发开始指令，要求DHT11传输数据
    gpio.digitalWrite(channel, gpio.LOW)  # 拉低25ms开始指令
    gpio.delay(25)
    gpio.digitalWrite(channel, gpio.HIGH)  # 输出高电平，开始指令结束
    gpio.pinMode(channel, gpio.INPUT)  # 设针脚为输入状态
    ###开始指令发送完毕，把管脚设置为高电平，并等待DHT11拉低管脚。传输数据
    while (gpio.digitalRead(channel) == gpio.HIGH): pass  # 如果管脚一直是1，则一直等待。
    ###若被拉低，说明传输开始，应答信号+40位数据+结束标志共42位
    ###下边共循环45次，故意多循环几次看结果。
    ###开始接受数据,50us低 + 26-28us高=0，50us低 + 70us高 = 1
    for i in range(45):  # 测试每个数据周期的时间（包括40bit数据加一个发送开始标志
        tc = gpio.micros()  # 记下当前us数（从初始化开始算起，必要时重新初始化）
        '''
        一个数据周期，包括一个低电平，一个高电平，从DHT11第一次拉低信号线开始
        到DHT11发送最后一个50us的低电平结束（然后被拉高，一直维持高电平，所以
        最后的完成标志是一直为高，超过500us）
        '''
        while (gpio.digitalRead(channel) == gpio.LOW): pass  # 一位数据由一个低电平
        while (gpio.digitalRead(channel) == gpio.HIGH):  # 加一个高电平组成
            if gpio.micros() - tc > 500:  # 如果超过500us就结束了本次循环,传输结束后
                break  # 会被上拉电阻拉成高电平，防止进入死循环
        tl.append(gpio.micros() - tc)  # 记录每个周期时间的us数，存到tl这个列表
    print(tl)
    return tl


def judge_bit(interval):
    # 50us低 + 26-28us高=0，50us低 + 70us高 = 1
    rule = 100
    if interval < rule:
        bit = 0
    else:
        bit = 1
    return bit

def process_data(data_tuple_list):
    data_list = []
    for data in data_tuple_list:
        data_list.append(judge_bit(data))
    data_list = data_list[1:]
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
          (humidity, humidity_point, temperature, temperature_point))
    if tmp%256 == check:
        result_dict = {
            'humidity': humidity,
            'humidity_point': humidity_point,
            'temperature': temperature,
            'temperature_point': temperature_point,
        }
    else:
        result_dict = None
    return result_dict


def main(channel):
    channel = int(channel)
    init(channel)
    while True:
        result_dict = None
        while result_dict is None:
            data_list = get_data(channel)
            result_dict = process_data(data_list)
            time.sleep(2)
            reinit(channel)
        post_request(result_dict)

def post_request(data,url="http://%s:/temperature/templist"%HOST):
    data_urlencode = urllib.urlencode(data)
    req = urllib2.Request(url=url, data=data_urlencode)

    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print res

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
