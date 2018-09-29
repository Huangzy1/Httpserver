#coding=utf-8
'''
name:Huang
time:2018.9.29
'''
import re                       #正则表达式
import sys                      #进程的退出
import time                     #睡眠时间
from socket import *            #通信
from setting import *           #导入配置文件
from threading import Thread    #多线程

class HttpServer(object):
    def __init__(self,addr=('0.0.0.0',80)):    #初始化
        self.sockfd=socket()    #创建套接字
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.addr=addr

    def bind(self,addr):        #绑定
        self.ip=addr[0]
        self.port=addr[1]
        self.sockfd.bind(addr)

    #HTTP服务器启动
    def serve_forever(self):
        self.bind(self.addr)
        self.sockfd.listen(10)
        print('Listen the port %d...'%self.port)
        while True:
            connfd,addr=self.sockfd.accept()
            print('Connect from',self.addr)
            handle_client=Thread(target=self.handle_request,args=(connfd,))
            handle_client.setDaemon(True)    #父进程退出后　子进程也跟着退出
            handle_client.start()


    def handle_request(self,connfd):
        #接受浏览器请求
        request=connfd.recv(4096)
        request_lines=request.splitlines()
        
        #获取请求行
        request_line=request_lines[0].decode()

        #正则提取请求方法和请求内容
        pattern=r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env=re.match(pattern,request_line).groupdict()
        except:
            response_headlers='HTTP/1.1 500 Server Error\r\n'
            response_headlers+='\r\n'
            response_body='Server Error'
            response=response_headlers+response_body
            connfd.send(response.encode())
            return

        #将请求发送给frame得到返回数据结果
        status,response_body=self.send_request(env['METHOD'],env['PATH'])
        #根据响应码组织响应头内容
        response_headlers=self.get_headlers(status)
        #将结果组织为http　response 发送给客户端
        response=response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()

    #和frame交互　发送request获取response
    def send_request(self,method,path):
        s=socket()
        s.connect(frame_addr)

        #向webframe发送method和path
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status=s.recv(128).decode()
        response_body=s.recv(4096*100).decode()
        s.close()
        return status,response_body


    def get_headlers(self,status):
        if status =='200':
            response_headlers='HTTP/1.1 200 OK\r\n'
            response_headlers+='\r\n'
        elif status=='404':
            response_headlers='HTTP/1.1 404 Not Found\r\n'
            response_headlers+='\r\n'
        return response_headlers


if __name__ == '__main__':
    httpd=HttpServer(ADDR)
    httpd.serve_forever()