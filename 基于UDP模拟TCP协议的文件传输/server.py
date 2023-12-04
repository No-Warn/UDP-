from socket import *
serverPort = 34343
serverSocket = socket(AF_INET, SOCK_DGRAM)  # Use SOCK_DGRAM for UDP
serverSocket.bind(("", serverPort))
print("The server is ready to receive")
# 等待第一次握手
data, clientAddress = serverSocket.recvfrom(2048)
if data == b'SYN':
    # 发送第二次握手,此次建立必须在第一次连接建立的基础上
    serverSocket.sendto(b'SYN-ACK', clientAddress)
    data, _ = serverSocket.recvfrom(2048)
    if data == b'ACK':
        # 发送第三次握手确认，这次建立必须在第一二次连接已经建立的基础上建立
        serverSocket.sendto(b'ACK', clientAddress)
        buffer_size = 1024
        # 保存文件，此次实验测试用的数据均为txt文件，其他文件类型的文件在传输过来显示源文件丢失
        with open('received_file.txt', 'wb') as file:
            while True:
                # 接收数据，以设置的最大文件大小来接收文件
                data, client_address = serverSocket.recvfrom(buffer_size)
                # 若内容最后为空，则将结束传输
                if not data:
                    break
                # 写入数据到文件
                file.write(data)
        print("文件传输成功！")
        # 模拟TCP连接释放的挥手过程
        serverSocket.sendto(b'FIN', clientAddress)
        print("等待客户端关闭连接...")
        data, _ = serverSocket.recvfrom(2048)
        if data == b'ACK':
            print("客户端已关闭连接")
# 关闭套接字
serverSocket.close()