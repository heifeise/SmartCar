import server
if __name__ == "__main__":
    ip = '192.168.31.79'
    port = 6666
    serv = server.Server(ip, port)
    serv.get_client()
    serv.get_from_client()
    #
    while True:
        # 其它功能代码
        # queue线程安全，如果在队列为空时使用get会一直等待直到不为空
        if not serv.command_que.empty():
            print(serv.command_que.get())  # 获取队列中的第一条命令
        # 其它功能代码
