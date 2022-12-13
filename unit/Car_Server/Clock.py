import time
import threading


# 计时器
class Clock:
    def __init__(self):
        self.__length = 0  # 需要计时的时间长度
        self.__current = 0  # 当前已经累加的计时
        self.__stop = True  # 是否已经停止,True表示已经停止

    # 开始计时
    def start(self, length):
        if not self.__stop:  # 如果计时未停止，放弃原有计时
            self.__stop = True  # 原计时线程结束
        self.__length = length
        self.__current = 0
        th = threading.Thread(target=self.increase)
        self.__stop = False
        th.setDaemon(True)  # 把主线程设置为守护线程
        th.start()

    # 累计计时,默认精度为0.1s
    def increase(self, accuracy=0.1):
        while not self.__stop:
            time.sleep(accuracy)
            self.__current += accuracy
            if self.__current >= self.__length:  # 计时时间到，停止计时
                self.__stop = True

    # 查询计时器状态
    def is_stop(self):
        return self.__stop


if __name__ == '__main__':
    tim = Clock()
    tim.start(1)
    i = 0
    while True:
        if tim.is_stop():
            i += 1
            print(i)
            tim.start(1)
