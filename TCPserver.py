import socket
import threading


def handle_cline(new_cline):
    # 接收客户端请求数据
    rec_date = new_cline.recv(4096)
    # 判断接收的数据是否为0
    if len(rec_date) == 0:
        new_cline.close()
        return
    # 解码接收到客户端请求数据
    rec_content = rec_date.decode('utf-8')
    # 对请求行按照空格进行分割
    request_link = rec_content.split(" ", 2)
    # 获取资源路径
    request_path = request_link[1]
    # 切片：所用浏览器分割出的reqiest_path为 "/index/";此处只需"/index.html"
    paths = request_path[0:-1]
    print(paths)
    print(request_path)

    # favicon.ico为请求小图标，此处未添加，if用来当请求非小图标时反馈html
    if paths != '/favicon.ic':
        # 判断访问是否为根目录，当访问为根目录是指定返回首页面
        if request_path == '/' or request_path == ' ':
            paths = '/index'
        try:
            with open('status' + paths + '.html') as file:
                file_date = file.read()

        except Exception as e:
            # 执行到此说明没有请求的该文件，应该返回404
            # 响应行
            request_line = 'http/1.1 404 not found\r\n'
            # 响应头
            request_header = 'server:pws/1.1\r\n'
            # 响应体
            request_body = file_date
            # 把响应数据包装成http协议报文格式
            response = (request_line + request_header + request_body).encode('utf-8')
            new_cline.send(response)
        else:
            # 执行到此说明有请求的该文件，应该返回200
            # 响应行
            request_line = 'http/1.1 200 ok\r\n'
            # 响应头
            request_header = 'server:pws/1.1\r\n'
            # 响应体
            request_body = file_date
            # 把响应数据包装成http协议报文格式
            response = (request_line + request_header + request_body).encode('utf-8')
            new_cline.send(response)
        finally:
            new_cline.close()


def word1():
    # 静态web建设
    # 创建套接字
    tcp_sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用
    # SOL_SOCKET表示当前套接字
    # 第二个参数表示： 设置端口号复用选项
    tcp_sever_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_sever_socket.bind(("", 8000))
    # 监听客户端访问数量
    tcp_sever_socket.listen(128)
    while True:
        # 等待客户端连接
        new_cline, ip_port = tcp_sever_socket.accept()
        print('客服端的端口号和ip是：', ip_port)
        # 创建子线程
        new_thread = threading.Thread(target=handle_cline, args=(new_cline,))
        # 守护主线程，当子线程超长工作时，主线程要关闭则能关闭子线程
        new_thread.setDaemon(True)
        # 启动子线程
        new_thread.start()


if __name__ == '__main__':
    word1()
