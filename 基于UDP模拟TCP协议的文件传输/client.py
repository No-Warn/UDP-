from socket import *

# 输入需要连接的主机IP地址
serverName = input("请输入你所需要连接的主机IP地址：")
serverPort = 34343
address = (serverName, serverPort)
# 创建UDP套接字
client_socket = socket(AF_INET, SOCK_DGRAM)
# 第一次握手：客户端发送SYN包（请求建立连接）
client_socket.sendto(b'SYN', address)
print("第一次连接建立...")
server_response, _ = client_socket.recvfrom(2048)
# 第二次握手：客户端发送ACK包（确认服务器的响应）
if server_response == b'SYN-ACK':
    client_socket.sendto(b'ACK', address)
    print("第二次连接建立...")
# 第三次握手：客户端发送数据包
client_socket.sendto(b'This is a test message.', address)
print("第三次连接建立...")
# 等待服务器的确认
server_confirmation, _ = client_socket.recvfrom(2048)
if server_confirmation == b'ACK':
    # 设置每个数据包的大小
    buffer_size = 1024
    # 输入需要传输的文件名称
    # !!!注意，在传输文件之前请确认接收方的接收内容那段代码中的文件类型是否与你所想传输的文件类型是否一致
    filename = input("请输入你需要传输的文件名称（保证该文件在该文件相同的目录下）:")
    # 读取要传输的文件
    with open(filename, 'rb') as file:
        while True:
            # 逐个分片读取文件数据
            data = file.read(buffer_size)
            if not data:
                break
            # 发送数据到服务器
            client_socket.sendto(data, address)
    # 发送空数据包，表示文件传输完成
    print("文件传输成功！")
    client_socket.sendto(b'', address)
    # 模拟TCP连接释放的挥手过程
    client_socket.sendto(b'FIN', address)
    server_response, _ = client_socket.recvfrom(2048)
    if server_response == b'ACK':
        print("服务器已关闭连接")
# 关闭套接字
client_socket.close()
