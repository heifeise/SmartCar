import server
if __name__ == "__main__":
    ip = '192.168.31.79'
    port = 6666
    time_out = 3
    serv = server.Server(ip, port, time_out)
    serv.get_client()  # 获取套接字
    print("获取成功")
    serv.get_from_client()  # 在子线程中获取消息
    serv.check_connect()  # 在子线程中检查连接状态，可重新获取套接字
    command = ""
    # 模拟程序循环
    while True:
        # 其它功能代码
        # queue线程安全，如果在队列为空时使用get会一直等待直到不为空
        if not serv.command_que.empty():
            command = serv.command_que.get()
            print(command)  # 获取队列中的第一条命令
        if command == "quit":
            serv.close()
            break
        # 其它功能代码
