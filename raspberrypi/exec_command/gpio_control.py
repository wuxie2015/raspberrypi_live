#! /usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

def init_gpio_list(output_list=None,input_list=None):
    # BOARD编号方式，基于插座引脚编号
    GPIO.setmode(GPIO.BOARD)
    if output_list:
        for channel in output_list:
            GPIO.setup(channel, GPIO.OUT)
    if input_list:
        for channel in input_list:
            GPIO.setup(channel, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)# 默认低电平
            #or GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def clean():
    GPIO.cleanup()

def set_channel_list(channel_list,status_tuple):
    # chan_list = [11,12]
    # GPIO.output(chan_list, GPIO.LOW)
    # GPIO.output(chan_list, (GPIO.HIGH, GPIO.LOW))
    if isinstance(channel_list,list) and isinstance(status_tuple,tuple):
        set_channel(channel_list,status_tuple)
        return True
    else:
        return False

def set_channel(channel,status):
    if status not in [GPIO.LOW,GPIO.HIGH]:
        return False
    else:
        GPIO.output(channel,status)
        return True

def read_channel(channel):
    status = GPIO.input(channel)
    return status

def query_channel(channel,status,interval=0.1):
    if status == GPIO.LOW:
        while read_channel(channel) == GPIO.HIGH:
            time.sleep(interval)
    else:
        while read_channel(channel) == GPIO.LOW:
            time.sleep(interval)

def read_edge_join(channel,type,timeout=5000):
    if type in [GPIO.RISING,GPIO.FALLING]:
        status = GPIO.wait_for_edge(channel, GPIO.RISING, timeout=timeout)
        if status is None:
            print('Timeout occured')
            return False
        else:
            return True
    else:
        return False

def read_edge_none_join(channel,type):
    if type in [GPIO.RISING, GPIO.FALLING]:
        GPIO.add_event_detect(channel, type)
        #之后在线程中循环执行
        # if GPIO.event_detected(channel):
        #     print('Button pressed')
        return True
    else:
        return False

def read_edge_callback(channel,type,callback_func_list):
    if type in [GPIO.RISING, GPIO.FALLING]:
        GPIO.add_event_detect(channel, type)
        for func in callback_func_list:
            GPIO.add_event_callback(channel, func)
        return True
    else:
        return False

def set_pwm(channel,frequence,dutycycle):
    p = GPIO.PWM(channel, frequence)
    if dutycycle in range(0,101):
        p.start(dutycycle)
        return p
    else:
        return None

def modify_pwm(p,dutycycle):
    if dutycycle in range(0, 101):
        p.ChangeDutyCycle(dutycycle)
        return True
    else:
        return False

def stop_pwm(p):
    p.stop()
