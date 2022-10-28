from socket import *
import time


# 枚举报文类型
class MessType:
    REACTION = "reaction"
    COMMAND = "command"
    BEGIN = "begin"
    END = "end"


"""
报文格式：
开始符_信息标识_信息_信息类别_结束符
"""


class Client:
    def __init__(self, server_ip: str, server_port: int):
        # 创建socket
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        # 目的信息
        self.server_ip = server_ip  # ip地址
        self.server_port = server_port  # 端口号

    """
    功能：向服务端发送一次命令
    param:
    command: 发送的命令
    time_out: 服务端响应超时时间(s), 默认10s
    """
    def get_connect(self):
        # 链接服务器
        self.tcp_client_socket.connect((self.server_ip, self.server_port))

    def send_command(self, tag: str, command: str, time_out: 'int > 0' = 10):
        # 获取正确格式的命令
        send_mess = self.get_command(tag, command)
        self.tcp_client_socket.send(send_mess.encode('UTF-8'))
        receive_data = self.get_from_server()
        i = 0
        t = time.time()
        response = self.get_reaction(tag)  # 获取预想的回应
        # 接收对方发送过来的数据，最大接收1024个字节
        while i < time_out and response != receive_data:
            receive_data = self.get_from_server()
            if round(time.time() - t, 1) == 1:  # 时间过去一秒
                i += 1
        if i >= time_out:
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

    # 关闭嵌套字
    def close(self):
        self.tcp_client_socket.close()
