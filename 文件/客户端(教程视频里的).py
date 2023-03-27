# coding=utf-8

import socket,os
# 创建对象
sk = socket.socket()
# 绑定ip地址
sk.connect(('127.0.0.2', 13001))  #链接成功之后就发送，调用post_file文件
#到41行


def post_file(sk_obj,file_path):
    '''
    发送数据
    :param sk_obj:  socket对象
    :param file_path: 文件的路径
    :return:
    '''

    # 发送文件大小 首先要知道 file_path文件大小，才能够发送数据     # 导入 'os' 模块
    ''' os.stat 只要把文件的路径传输 进去，就会返回一系列的，数据和参数  '''
    file_size = os.stat(file_path).st_size  # 需要的是这个st_size 帮助获取文件的 大小
    # 由于 file_size 是整型， (整型也要进行转换byet，不具备decode方法）,
    # 1.先把整型转成 str（字符串  2.再调用encode的方法
    sk_obj.sendall(str(file_size).encode('utf-8')  )
    sk_obj.recv(1024)  #避免粘包

    # 发送文件名字 （知道文件大小之后）
    # os.path.spliy，作用是跟字母意思一样， 把路径分割开来
    file_name = os.path.split(file_path)[1]
    sk_obj.sendall(file_name.encode('utf-8'))
    sk_obj.recv(1024)  #避免粘包  # 这边也要阻塞状态，就可以保证下边的代码不会执行

    # 发送文件内容 （大于1024字节，要循环发几次?）
    # 这里f.read()读出来是  字符串， 发送的时候 还要将字符串 转换byet。（麻烦）
    # 干脆读的时候就用 rb模式 ，直接读出来是 byet，发过去也是byet类型
    with open(file_path,'rb',) as f:
        while file_size > 0 :      # 大于0就继续发
            sk_obj.sendall(f.read(1024)) #每次去读 1024个字节
            file_size -= 1024

# post_file，接受两个参数，（第一个是sk对象，第二个是文件路径）
# 变颜色了，要转义
path = 'E:\python pc 练习文件\淘宝买的自动化测试课程及内容\课程安排\\2 Python进阶\day4 socket编程\\2文件上传与下载\服务器\\a.png'
post_file(sk,path)

sk.close()