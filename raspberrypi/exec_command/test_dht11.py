# -*- coding: utf-8 -*-
import wiringpi2 as gpio
owpin=29     #第8脚为1-wire脚
tl=[]       #存放每个数据位的时间
gpio.wiringPiSetup()        #初始化wiringpi库
gpio.pinMode(owpin,1)       #设置针脚为输出状态
gpio.digitalWrite(owpin,1)  #输出高电平
gpio.delay(1)
###发开始指令，要求DHT11传输数据
gpio.digitalWrite(owpin,0)  #拉低25ms开始指令
gpio.delay(25)
gpio.digitalWrite(owpin,1)  #输出高电平，开始指令结束
gpio.pinMode(owpin,0)       #设针脚为输入状态
###开始指令发送完毕，把管脚设置为高电平，并等待DHT11拉低管脚。传输数据
while(gpio.digitalRead(owpin)==1): pass #如果管脚一直是1，则一直等待。
###若被拉低，说明传输开始，应答信号+40位数据+结束标志共42位
###下边共循环45次，故意多循环几次看结果。
for i in range(45):   #测试每个数据周期的时间（包括40bit数据加一个发送开始标志
    tc=gpio.micros()  #记下当前us数（从初始化开始算起，必要时重新初始化）
    '''
    一个数据周期，包括一个低电平，一个高电平，从DHT11第一次拉低信号线开始
    到DHT11发送最后一个50us的低电平结束（然后被拉高，一直维持高电平，所以
    最后的完成标志是一直为高，超过500ms）
    '''
    while(gpio.digitalRead(owpin)==0):pass  #一位数据由一个低电平
    while(gpio.digitalRead(owpin)==1):      #加一个高电平组成
        if gpio.micros()-tc>500:    #如果超过500us就结束了本次循环,传输结束后
            break                   #会被上拉电阻拉成高电平，防止进入死循环
    tl.append(gpio.micros()-tc) #记录每个周期时间的us数，存到tl这个列表

print(tl)