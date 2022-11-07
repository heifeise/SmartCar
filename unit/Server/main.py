import queue

from action.CarTools import CarTools
from Server.Server import Server
import threading
import time
"""
命令：解析
turn-left-speedleft-speedright:左转_左轮速度_右轮速度
turn-right-speedleft-speedright:右转_左轮速度_右轮速度
straight-speed:直行_速度
stop:停止
trackline:巡线模式
manual:手动控制
open-distance-mature:开启测距模块
open-image-identy:开启图像识别
"""

list_opencv = ['open-image-identy']  # opencv相关命令
list_action = ['turn-left', 'turn-right', 'straight', 'stop', 'trackline', 'manual', 'open-distance-mature', 'close-distance-mature', 'quit']  # 行动代码


# 巡线
def trackline(tool, lock):
    while True:
        lock.acquire()
        tool.tracking()
        time.sleep(1)
        lock.release()


# 移动、巡线与手动控制的切换
def car_action(tool, lock_track, lock_distance, que_action):
    while True:
        command = que_action.get()
        command = command.split('-')
        if command[0] == list_action[0] and len(command) == 3:
            tool.left(float(command[1]), float(command[2]))
        elif command[0] == list_action[1] and len(command) == 3:
            tool.right(float(command[1]), float(command[2]))
        elif command[0] == list_action[2] and len(command) == 3:
            tool.run(float(command[1]), float(command[2]))
        elif command == list_action[3]:
            tool.brake()  # 停止运动
        elif command[0] == list_action[4]:  # 开启巡线功能
            lock_track.release()  # 释放锁
        elif command[0] == list_action[5]:  # 开启手动
            lock_track.acquire()  # 上锁,阻塞巡线线程
        elif command[0] == list_action[6]:  # 开启距离测量模块
            lock_distance.release()
        elif command[0] == list_action[7]: # 关闭距离测量模块
            lock_distance.acquire()
        elif command[0] == list_action[8]:
            tool.close()  # 退出通信控制移动
            serv.close()  # 退出通信
            break


# 测量两人之间的距离
def test_distance(tool, lock_distance):
    while True:
        if not tool.is_human(0):  # 如果此时垂直距离处的物体不是人类
            continue
        message = tool.people_distance(pos=0, spacing=1)  # pos:第一人的位置（角度），spacing:设定的两人的理想间隔
        if message[1] <= message[2]:  # 如果与第二人的距离小于理想距离
            Buzzer()  # 发出提示音

def Buzzer():
    print("to close")

def get_command(server, que_action, que_opencv):
    while True:
        com = server.command_que.get()  # 内置的消息队列
        com = com.split('-')[0]
        if com in list_action:
            que_action.put(com)
        elif com in list_opencv:
            que_opencv.put(com)
    
        
if __name__ == "__main__":
    ip = '192.168.31.79'
    port = 6666
    time_out = 3
    serv = Server(ip, port, time_out)
    serv.get_client()  # 获取套接字
    print("获取成功")
    serv.get_from_client()  # 在子线程中获取消息
    serv.check_connect()  # 在子线程中检查连接状态，可重新获取套接字
    tools = CarTools()

    track_line = 0
    lock_track = threading.Lock()  # 创建巡线同步锁，用以巡线与手动操纵之间的切换
    lock_track.acquire()  # 上锁
    th_track = threading.Thread(target=trackline, args=(tools, lock_track), daemon=True)  # 创建巡线线程
    th_track.start()

    action_que = queue.Queue()  # 小车移动控制消息队列
    opencv_que = queue.Queue()  # 图像处理命令队列
    th_command = threading.Thread(target=get_command, args=(serv, action_que, opencv_que), daemon=True)  # 创建命令接收，分类线程
    th_command.start()

    th_action = threading.Thread(target=car_action, args=(tools, lock_track, action_que), daemon=True)  # 创建小车移动控制线程
    th_action.start()

    distance = 0
    lock_distance = threading.Lock() # 创建距离测量线程同步锁, 用以开关测距功能
    lock_distance.acquire()  # 上锁
    th_distance = threading.Thread(target=test_distance, args=(tools, lockdistance), daemon=True)
    th_distance.start()
    # lock_track.release()  # 开启巡线
    # 程序循环
    while True:
        commands = ""
        if not opencv_que.empty():
            commands = opencv_que.get()
        print(commands)  # 此处放置图像处理代码
