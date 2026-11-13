import socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect(("www.bjfu.edu.cn", 80))

request = (b"GET / HTTP/1.1\r\n" b"Host: www.bjfu.edu.cn\r\n" b"Connection: close\r\n" b"\r\n")

#发送请求
s.sendall(request)

#设置接收缓存区和recv计数
buf = []
recv_count = 0


#接收循环
content_length = None

while True:
    data = s.recv(4096) #TCP字节分区接收

    #对端关闭，退出循环
    if not data:
        break

    #正常接收后纳入缓存区和正常计数
    recv_count+=1
    buf.append(data)

    print(f"第 {recv_count} 次recv, 收到 {len(data)} 字节")

    #保存完整的http响应
    response = b"".join(buf)

    #检查响应头是否完整
    if b"\r\n\r\n" not in response:
        continue    #结束本次循环

    #开始分离响应头和正文
    header, body = response.split(b"\r\n\r\n", 1)

    #从header中找到Content-Length
    #把响应头按照换行符拆开
    for line in header.split(b"\r\n"):
    #判断行开头是不是content-length
        if line.lower().startswith(b"content-length"):
    #以冒号为分割线分别取到contnt-length和后面的实际长度，取下标1后去除空白提取数字
            content_length = int(line.split(b":", 1)[1].strip())
            break

    #判断正文是否完整接收
    if content_length is not None and len(body) >= content_length:
        print("正文接收完成")
        break

#打印完整响应
print("\n\n\n\n\n完整响应")
print(response.decode("utf-8", errors="replace"))

#T2：对HTTP响应头解析 分离header和body,这次的response是完整响应，所以不用判断
header, body = response.split(b"\r\n\r\n", 1)

#提取状态码
status_line = header.split(b"\r\n", 1)[0]
status_code = int(status_line.split()[1])

print("HTTP状态码: ", status_code)

#打印响应头
print(header.decode("utf-8", errors="replace"))
#保存正文
with open("index.html", "wb") as f:
    f.write(body)
print("网页正文保存成功")

#关闭socket连接
s.close()
print("Socket连接已关闭")
