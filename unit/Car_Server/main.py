import queue

from CarTools import CarTools
from Server import Server
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
list_action = ['turnleft', 'turnright', 'straight', 'stop', 'trackline', 'manual', 'openDistanceMature',
               'closeDistanceMature', 'quit']  # 行动代码


# 巡线
def trackline(tool, lock, lock_dist):
    while True:
        lock_dist.acquire()
        lock.acquire()
        tool.tracking()
        time.sleep(1)
        lock.release()
        lock_dist.release()


# 移动、巡线与手动控制的切换
def car_action(tool, lock_dist, lock_track, que_action):
    while True:
        lock_dist.acquire()
        time.sleep(0.3)
        command = que_action.get()
        command = command.split('-')
        if command[0] == list_action[0] and len(command) == 3:
            tool.left(float(command[1]), float(command[2]))
        elif command[0] == list_action[1] and len(command) == 3:
            tool.right(float(command[1]), float(command[2]))
        elif command[0] == list_action[2] and len(command) == 3:
            tool.run(float(command[1]), float(command[2]))
        elif command[0] == list_action[3]:
            tool.brake()  # 停止运动
        elif command[0] == list_action[4]:  # 开启巡线功能
            lock_track.release()  # 释放锁
        elif command[0] == list_action[5]:  # 开启手动
            lock_track.acquire()  # 上锁,阻塞巡线线程
        # elif command[0] == list_action[6]:  # 开启距离测量模块
        # lock_distance.release()
        # elif command[0] == list_action[7]: # 关闭距离测量模块
        # lock_distance.acquire()
        elif command[0] == list_action[8]:
            tool.close()  # 退出通信控制移动
            serv.close()  # 退出通信
            break
        lock_dist.release()


# 测量两人之间的距离
def test_distance(tool, lock_dist):
    if not tool.is_human(0):  # 如果此时垂直距离处的物体不是人类
        print("not human")
    message = tool.people_distance(lock_dist, pos=0, spacing=100)  # pos:第一人的位置（角度），spacing:设定的两人的理想间隔
    if message[1] < message[2]:  # 如果与第二人的距离小于理想距离
        Buzzer()  # 发出提示音
    else:
        print("normal")


def Buzzer():
    print("too close")


def get_command(server, lock_dist, que_action, que_opencv):
    while True:
        lock_dist.acquire()
        time.sleep(0.3)
        coms = server.command_que.get()  # 内置的消息队列
        print(coms)
        com = coms.split('-')[0]
        if com in list_action:
            que_action.put(coms)
            # print("action:", com, sep="\t")
        elif com in list_opencv:
            que_opencv.put(coms)
            # print("opencv:", com, sep="\t")
        lock_dist.release()


if __name__ == "__main__":
    ip = '192.168.43.88'
    port = [5555, 6666, 7777]
    time_out = 3
    print("等待连接")
    i = 0
    serv = None
    while i != 2:
        try:
            serv = Server(ip, port[i], time_out)
            print("使用端口：", port[i])
            serv.get_client()  # 获取套接字
            break
        except OSError as error:
            i += 1
    print("获取成功")
    serv.get_from_client()  # 在子线程中获取消息
    serv.check_connect()  # 在子线程中检查连接状态，可重新获取套接字
    tools = CarTools()

    distance_lock = 0
    lock_distance = threading.Lock()  # 创建距离测量线程锁
    th_distance = threading.Thread(target=test_distance, args=(tools, lock_distance), daemon=True)

    track_line = 0
    lock_track = threading.Lock()  # 创建巡线同步锁，用以巡线与手动操纵之间的切换
    lock_track.acquire()  # 上锁
    th_track = threading.Thread(target=trackline, args=(tools, lock_track, lock_distance), daemon=True)  # 创建巡线线程

    action_que = queue.Queue()  # 小车移动控制消息队列
    opencv_que = queue.Queue()  # 图像处理命令队列
    # 创建命令接收、分类线程
    th_command = threading.Thread(target=get_command, args=(serv, lock_distance, action_que, opencv_que), daemon=True)

    # 创建小车移动控制线程
    th_action = threading.Thread(target=car_action, args=(tools, lock_distance, lock_track, action_que), daemon=True)

    th_command.start()
    th_distance.start()
    th_track.start()
    th_action.start()

    # lock_track.release()  # 开启巡线
    # 程序循环
    #
    while True:
        commands = ""
        if not opencv_que.empty():
            commands = opencv_que.get()
            print(commands)  # 此处放置图像处理代码
        # time.sleep(3)  # 模拟图像处理所耗费的时间
        lock_distance.acquire()
        camera = cv2.VideoCapture(0)

        is_got_image, image = camera.read()
        if is_got_image:
            detector = ColorDetector(image_input=image)

            if detector.frame() is not None:
                result = detector.get_result()
                print(result)

        camera.release()
        lock_distance.acquire()
