import re
from socket import *
import queue
import threading


# 枚举报文类型
class MessType:
    REACTION = "reaction"
    COMMAND = "command"
    BEGIN = "begin"
    END = "end"


# 服务端接受信息
class Server:
    def __init__(self, server_ip: str, server_port: int):
        # 本地信息
        self.server_ip = server_ip  # 服务端ip地址
        self.server_port = server_port  # 服务端的端口号
        self.command_patten = MessType.BEGIN + "_[a-zA-Z]+_[a-zA-Z]+_" + MessType.COMMAND + "_" + MessType.END  # 接收的命令格式
        self.reaction_patten = MessType.BEGIN + "_[a-zA-Z]+_[a-zA-Z]+_" + MessType.REACTION + "_" + MessType.END  # 返回给客户机的反馈信息
        # 创建socket
        self.tcp_server_socket = socket(AF_INET, SOCK_STREAM)
        # 绑定
        self.tcp_server_socket.bind((self.server_ip, self.server_port))
        # 使用socket创建的套接字默认的属性是主动的，使用listen将其变为被动的，这样就可以接收别人的链接了
        # listen里的数字表征同一时刻能连接客户端的程度.
        self.tcp_server_socket.listen(1)
        self.client_socket = None
        self.client_address = None
        self.command_que = queue.Queue()  # 命令队列
        self.close = True

    def get_client(self):
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
        # client_socket用来为这个客户端服务
        # tcp_server_socket就可以省下来专门等待其他新客户端的链接
        # client_address 是元组（ip，端口）
        self.client_socket, self.client_address = self.tcp_server_socket.accept()
        self.close = False

    def get_from_client(self):
        t = threading.Thread(target=self.loop)
        t.start()

    # 持续接收报文
    def loop(self):
        while not self.close:
            # 接收1024个字节
            receive = self.client_socket.recv(1024).decode('UTF-8')
            if self.check_command(self.command_patten, receive):  # 如果是命令
                print("接收到一条命令")
                self.command_que.put(receive.split('_')[2])
                self.send_to_client(self.get_reaction(receive))  # 向客户端发送反馈反馈

    """
    由接收到的信息得到应该返回给客户端的反馈信息
    receive:来自客户端的接受信息
    """

    @staticmethod
    def get_reaction(receive):
        receive = receive.split('_')
        ls = tuple((MessType.BEGIN, receive[1], "SUCCESS", MessType.REACTION, MessType.END))
        back = str.join('_', ls)
        return back

    # 向客户端发送信息
    def send_to_client(self, message):
        # 发送消息
        self.client_socket.send(message.encode('UTF-8'))

    # 字符串校验
    @staticmethod
    def check_command(patten, mess):
        return re.fullmatch(patten, mess) is not None

    def close(self):
        # 关闭为这个客户端服务的套接字，只要关闭了，就意味着为不能再为这个客户端服务了，如果还需要服务，只能再次重新连接
        self.client_socket.close()
        self.close = True  # 结束线程
