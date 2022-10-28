# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import numpy as np

class Car_tools:
    def __init__(self):
        # 小车电机引脚定义
        self.IN1 = 20  # 左电机正转
        self.IN2 = 21  # 左电机反转
        self.IN3 = 19  # 右电机正转
        self.IN4 = 26  # 右电机反转
        # 脉宽调制
        self.ENA = 16
        self.ENB = 13
        self.pwm_ENA = None
        self.pwm_ENB = None
        self.pwm_servo = None
        # 小车按键定义
        self.key = 8
        # 超声波引脚定义
        self.EchoPin = 0  # 回馈引脚
        self.TrigPin = 1  # 触发引脚
        # 舵机引脚定义
        self.ServoPin = 23
        # 设置GPIO口为BCM编码方式
        GPIO.setmode(GPIO.BCM)
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.__initPin__()

    # 电机引脚初始化为输出模式
    # 按键引脚初始化为输入模式
    # 超声波引脚初始化
    def __initPin__(self):

        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)

        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)
        
        GPIO.setup(self.key, GPIO.IN)
        GPIO.setup(self.EchoPin, GPIO.IN)
        GPIO.setup(self.TrigPin, GPIO.OUT)
        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    # 小车前进
    def run(self, leftspeed, rightspeed):
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车后退
    def back(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车左转
    def left(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车右转
    def right(self, leftspeed, rightspeed):
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车原地左转
    def spin_left(self, leftspeed, rightspeed):
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车原地右转
    def spin_right(self, leftspeed, rightspeed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车停止
    def brake(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def key_scan(self):
        # 按键初始为高电平
        while GPIO.input(self.key):
            pass
        while not GPIO.input(self.key):
            time.sleep(0.01)
        return True

    # 超声波测距(cm)
    def distance_mature(self):
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)
        while not GPIO.input(self.EchoPin):
            pass
        t1 = time.time()
        while GPIO.input(self.EchoPin):
            pass
        t2 = time.time()
        # print("distance is %d " % (((t2 - t1) * 340 / 2) * 100))
        time.sleep(0.01)
        return ((t2 - t1) * 340 / 2) * 100
    
    # 舵机旋转到指定角度
    def servo_appointed_detection(self, pos):
        for i in range(3):
            self.pwm_servo.ChangeDutyCycle(2.5 + 10 * pos / 180)

    # 温度测量（临时）
    def temperature(self, pos):
        return 36.5
    
    # 人类判断
    def isHuman(self, pos):
        if self.temperature(pos) >= 35.5:
            return True
        return False

    # 人与人之间的距离
    def people_distance(self, pos=0):
        GPIO.setup(self.ServoPin, GPIO.OUT)
        self.pwm_servo = GPIO.PWM(self.ServoPin, 50)
        self.pwm_servo.start(0)
        self.servo_appointed_detection(pos) # the position of first people
        first_distance = self.distance_mature()
        second_distance = first_distance
        for i in range(0, 60, 3):
            if self.isHuman(i):
                self.servo_appointed_detection(i)
                temp = self.distance_mature()
                print(temp)
                if temp < second_distance:
                    second_distance = temp
                print("distance between two things:",(temp ** 2 - first_distance ** 2) ** (1 / 2))
            time.sleep(0.3)
        distance = (1 + first_distance ** 2) ** (1 / 2)
        print("first_people:", first_distance)
        print("second_people:", second_distance)
        print("should be:", distance)
        self.servo_appointed_detection(0)
        time.sleep(0.3)
        self.pwm_servo.stop()

    def stop_pwm(self):
        self.pwm_ENA.stop()
        self.pwm_ENB.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    tool = Car_tools()
    tool.people_distance()

