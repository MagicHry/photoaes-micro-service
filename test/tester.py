# coding=utf-8
"""
美学微服务
启动器
"""
import socket
import os.path

LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 8848
CODE_ERROR = '500'
CODE_OK = '200'
CODE_FILE_ERROR = '400'
END_MARKER = '!EOF!'



directory = 'testimg'
imglst = []
for file in os.listdir(directory):
    imglst.append(os.path.abspath(os.path.join('testimg',file)))
for img in imglst:
    # 使用ipV4
    socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接
    socket_conn.connect((LISTEN_IP, LISTEN_PORT))
    rtn_code = (socket_conn.recv(2048)).decode('utf-8')
    if rtn_code == CODE_ERROR:
        print('Aes model not init')
    elif rtn_code == CODE_OK:
        print('Good to go')
        test_img_path = img
        test_img_path += END_MARKER
        print('Send path -> %s' % test_img_path)
        # 发送连接
        socket_conn.send(test_img_path)
        aes_score = (socket_conn.recv(2048)).decode('utf-8')
        print('The aes score is %s' % aes_score)
        socket_conn.close()
    else:
        socket_conn.close()



# directory = 'testimg'
# imglst = []
# for file in os.listdir(directory):
#     imglst.append(os.path.abspath(file))
#
# print(imglst)