# coding=utf-8
#   __author__:lenovo
#   2020/5/13

import os,socket
import socket

# s1.创建socket对象
sk = socket.socket()
# s2.绑定ip地址与端口号
sk.bind(('127.0.0.2',13001))
# s3. 监听
sk.listen()
#

def get_file(sk_obj):
    '''
    接受文件
    :param sk_obj: socket对象
    :return:
    '''
    # 设置两个接受 '文件' 和‘名称’ 是为了 '避免粘包'，不间断的传输（意思是，如果我传的文件小于1024，
    # 我第二次传的文件还是会传到 第一个recv未存满的文件里[本应该存到第二个文件的recv]）
    # 接受文件大小
    file_size = int(sk_obj.recv(1024).decode("utf8"))  #str类型要转换 int 才能知道文件大小
    sk_obj.sendall(b"ok")  #代表的意思是 接受完文件 发过去一个ok 解除阻塞了

    # 接受文件名称
    file_name = sk_obj.recv(1024).decode("utf8")   # recv过来也是byte，也要解码
    sk_obj.sendall(b"ok")

    # 接受文件内容   ( %s: 站位符)
    #前面是 路径./， 后面是文件名称 （接收的文件，就不想给它重命名了）
    with open("./%s" %file_name,"wb") as f:
        while file_size > 0:                # 每次循环都接受1024
            f.write(sk_obj.recv(1024))      #将1024个字节，写进去
            file_size -= 1024
            # file_size = file_size - 1024



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
            file_size -= 1024      # 每发送1024字节，就减去读的这个1024字节

# s4.对应  客户端套接字
conn, addr = sk.accept()

# 由于是 '客户端' 发送文件给 '服务端'， 所以用'conn'传输进去（不是sk）
# 'conn'具体负责与'客户端'的 '逻辑业务'  get_file

# s5.接受文件 （文件的逻辑写在了get-file 里面了）
get_file(conn)   #到这里就没有其它的工作了 （该写客户端了，把post_file复制过去）

conn.close()
sk.close()
