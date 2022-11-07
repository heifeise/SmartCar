import threading
from socket import *
from Clock import Clock


# 枚举报文类型
class MessType:
    REACTION = "reaction"
    COMMAND = "command"
    STATUS = "connect"
    BEGIN = "begin"
    END = "end"


"""
报文格式：
开始符_信息标识_信息_信息类别_结束符
"""

# list_opencv = ['open-image-identy']  # opencv相关命令
# list_action = ['turn-left', 'turn-right', 'straight', 'stop', 'trackline', 'manual', 'open-distance-mature', 'close-distance-mature', 'quit']  # 行动代码
class Client:
    def __init__(self, server_ip: str, server_port: int, time_out: 'int > 0' = 5):
        # 创建socket
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        # 目的信息
        self.server_ip = server_ip  # ip地址
        self.server_port = server_port  # 端口号
        self.time_out = time_out  # 响应超时
        self.close = True  # 是否关闭连接

    """
    功能：向服务端发送一次命令
    param:
    command: 发送的命令
    time_out: 服务端响应超时时间(s), 默认10s
    """
    def get_connect(self):
        # 获取连接
        self.tcp_client_socket.connect((self.server_ip, self.server_port))
        self.close = False

    def send_command(self, tag: str, command: str):
        # 获取正确格式的命令
        send_mess = self.get_command(tag, command)
        self.tcp_client_socket.send(send_mess.encode('UTF-8'))
        receive_data = self.get_from_server()
        tim = Clock()
        response = self.get_reaction(tag)  # 获取预想的回应
        # 接收对方发送过来的数据，最大接收1024个字节
        tim.start(self.time_out)  # 开始计时
        # 等待接收反馈信息
        while not tim.is_stop() and response != receive_data:
            receive_data = self.get_from_server()
        if tim.is_stop():
            return "timeout"
        return "send success"

    """
    格式正确的发送报文
    信息标识符，信息
    """
    @staticmethod
    def get_command(tag, mess):
        ls = tuple((MessType.BEGIN, tag, mess, MessType.COMMAND, MessType.END))
        return str.join('_', ls)

    """
    得到格式正确的接收报文（反馈）
    tag:信息标识
    """
    @staticmethod
    def get_reaction(tag):
        ls = tuple((MessType.BEGIN, tag, "SUCCESS", MessType.REACTION, MessType.END))
        back = str.join('_', ls)
        return back

    # 获取服务端发送的报文
    def get_from_server(self):
        return self.tcp_client_socket.recv(1024).decode('UTF-8')

    #  每隔1.5s发送一段信息，让服务端确认连接状态
    def check_connect(self):
        tim = Clock()
        send_mess = self.get_command('check', MessType.STATUS)

        # 每隔1.5秒发送一条信息
        def loop_check():
            while not self.close:
                if tim.is_stop():
                    self.tcp_client_socket.send(send_mess.encode('UTF-8'))
                    tim.start(1.5)
        th = threading.Thread(target=loop_check)
        th.setDaemon(True)  # 把主线程设置为守护线程
        th.start()

    # 关闭嵌套字
    def _close(self):
        self.tcp_client_socket.close()
        self.close = True
