# -*- coding:UTF-8 -*-
import time

import RPi.GPIO as GPIO


class CarTools:
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
        # 循迹红外传感器
        self.TrackSensorLeftPin1 = 3  # 定义左边第一个循迹红外传感器引脚为3口
        self.TrackSensorLeftPin2 = 5  # 定义左边第二个循迹红外传感器引脚为5口
        self.TrackSensorRightPin1 = 4  # 定义右边第一个循迹红外传感器引脚为4口
        self.TrackSensorRightPin2 = 18  # 定义右边第二个循迹红外传感器引脚为18口
        # 小车按键定义
        self.key = 8
        # 超声波引脚定义
        self.EchoPin = 0  # 回馈引脚
        self.TrigPin = 1  # 触发引脚
        # 舵机引脚定义
        self.ServoPin = 23
        self.camera_lr_pin = 11
        self.camera_ud_pin = 9
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

        GPIO.setup(self.TrackSensorLeftPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorLeftPin2, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin1, GPIO.IN)
        GPIO.setup(self.TrackSensorRightPin2, GPIO.IN)

        GPIO.setup(self.camera_lr_pin, GPIO.OUT)
        GPIO.setup(self.camera_ud_pin, GPIO.OUT)

        self.pwm_camera_lr = GPIO.PWM(self.camera_lr_pin, 50)
        self.pwm_camera_ud = GPIO.PWM(self.camera_ud_pin, 50)

        self.pwm_camera_lr.start(0)
        self.pwm_camera_ud.start(0)

        # 设置pwm引脚和频率为2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)

        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    # 小车前进
    def run(self, leftspeed=5, rightspeed=5):
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车后退
    def back(self, leftspeed=5, rightspeed=5):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车左转
    def left(self, leftspeed=5, rightspeed=8):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车右转
    def right(self, leftspeed=8, rightspeed=5):
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN1, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车原地左转
    def spin_left(self, leftspeed=5, rightspeed=5):
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_ENB.ChangeDutyCycle(rightspeed)

    # 小车原地右转
    def spin_right(self, leftspeed=5, rightspeed=5):
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
    def servo_appointed_detection(self, pos, pwm_servo):
        for i in range(3):
            pwm_servo.ChangeDutyCycle(2.5 + 10 * pos / 180)

    def camera_lr_appointed_detection(self, pos):
        for i in range(1):
            self.pwm_camera_lr.ChangeDutyCycle(2.5 + 10 * pos / 180)

    def camera_ud_appointed_detection(self, pos):
        for i in range(3):
            self.pwm_camera_ud.ChangeDutyCycle(2.5 + 10 * pos / 180)

    # 温度测量（临时）
    def temperature(self, pos):
        return 36.5

    # 人类判断
    def is_human(self, pos):
        if self.temperature(pos) >= 35.5:
            return True
        return False

    # 人与人之间的距离
    # pos:参照的第一人的位置（角度）
    def people_distance(self, lock_distance, pos=0, spacing=1):
        GPIO.setup(self.ServoPin, GPIO.OUT)
        pwm_servo = GPIO.PWM(self.ServoPin, 50)
        pwm_servo.start(0)
        lock_distance.acquire()  # 上锁，防止其他线程抢占处理机
        self.servo_appointed_detection(pos, pwm_servo)  # the position of first people
        time.sleep(0.3)
        lock_distance.release()  # 解锁
        first_distance = self.distance_mature()
        second_distance = first_distance
        for i in range(5, 50, 5):
            if self.is_human(i):  # 判断位置i的物体是否是人类
                lock_distance.acquire()  # 上锁，防止其他线程抢占处理机
                self.servo_appointed_detection(i, pwm_servo)  # 转动舵机
                time.sleep(0.3)
                lock_distance.release()  # 解锁
                temp = self.distance_mature()  # 测量当前方向上人类的距离
                if temp < second_distance:  # 选择记录最小的
                    second_distance = temp
        distance = (spacing + first_distance ** 2) ** (1 / 2)  # 小车与第二人的应有距离
        # self.servo_appointed_detection(0, pwm_servo)
        # time.sleep(0.3)
        pwm_servo.stop()
        return first_distance, second_distance, distance

    def stop_pwm(self):
        self.camera_ud_appointed_detection(50)
        self.camera_lr_appointed_detection(90)
        time.sleep(2)
        self.pwm_ENA.stop()
        self.pwm_ENB.stop()
        self.pwm_camera_lr.stop()
        self.pwm_camera_ud.stop()
        GPIO.cleanup()

    # 黑线导航
    def tracking(self):
        speed = 5
        time.sleep(2)
        # 检测到黑线时循迹模块相应的指示灯亮，端口电平为LOW
        # 未检测到黑线时循迹模块相应的指示灯灭，端口电平为HIGH
        TrackSensorLeftValue1 = GPIO.input(self.TrackSensorLeftPin1)
        TrackSensorLeftValue2 = GPIO.input(self.TrackSensorLeftPin2)
        TrackSensorRightValue1 = GPIO.input(self.TrackSensorRightPin1)
        TrackSensorRightValue2 = GPIO.input(self.TrackSensorRightPin2)
        # 四路循迹引脚电平状态
        # 0 0 X 0
        # 1 0 X 0
        # 0 1 X 0
        # 以上6种电平状态时小车原地右转
        # 处理右锐角和右直角的转动
        if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
            self.spin_right(speed, speed)
            time.sleep(0.08)

        # 四路循迹引脚电平状态
        # 0 X 0 0
        # 0 X 0 1
        # 0 X 1 0
        # 处理左锐角和左直角的转动
        elif TrackSensorLeftValue1 == False and (
                TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
            self.spin_left(speed, speed)
            time.sleep(0.08)

        # 0 X X X
        # 最左边检测到
        elif TrackSensorLeftValue1 == False:
            self.spin_left(speed, speed)

        # X X X 0
        # 最右边检测到
        elif TrackSensorRightValue2 == False:
            self.spin_right(speed, speed)

        # 四路循迹引脚电平状态
        # X 0 1 X
        # 处理左小弯
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
            self.left(0, speed)

        # 四路循迹引脚电平状态
        # X 1 0 X
        # 处理右小弯
        elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
            self.right(speed, 0)

        # 四路循迹引脚电平状态
        # X 0 0 X
        # 处理直线
        elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
            self.run(speed, speed)
        # 当为1 1 1 1时小车保持上一个小车运行状态


if __name__ == "__main__":
    tool = CarTools()
    # for i in range(0, 180, 18):
    # tool.camera_lr_appointed_detection(i)
    #    tool.camera_ud_appointed_detection(i)
    #    time.sleep(2)
    # tool.camera_ud_appointed_detection
    # tool.run(10,13)
    # tool.tracking()
    t1 = time.time()
    tool.people_distance(pos=0, spacing=1)
    print(time.time() - t1)
