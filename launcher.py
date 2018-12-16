# coding=utf-8
"""
美学微服务
启动器
"""
from log import LogUtils as log
from conn import Config
from conn.ConnectionHadle import ConnHandler
from conn.ConnThread import ConnWorker
import socket
import threading

def launch_model():
    """
    启动美学模型
    :return:
    """
    from core.PhotoAesModel import aes_model
    aes_model.initModel()
    log.info('Init aes_model over')
    return aes_model

def start_listen():
    """
    开启端口监听
    :return:
    """
    # 使用ipV4
    socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 本机服务，端口8848
    socket_conn.bind((Config.LISTEN_IP, Config.LISTEN_PORT))
    # 并发连接数目为4
    socket_conn.listen(Config.CONCURRENT_NUM)
    log.info('Start to listener at port %d' % (Config.LISTEN_PORT))
    return socket_conn

def handle_conn(conn_handler):
    """
    连接处理
    :param conn_handler:
    :return:
    """
    conn_handler.handle_conn()

def main():
    """
    美学微服务的入口
    :return:
    """
    # log注册
    log.register_logger()
    # 初始化美学模型
    aes_model = launch_model()
    # 开启端口监听
    socket_conn = start_listen()
    # TODO:这边其实用一个线程池来进行维护会比较好
    try:
        while True:
            # 接受一个新连接:
            sock, addr = socket_conn.accept()
            # 处理连接
            conn_handler = ConnHandler(aes_model, sock, addr)
            worker = ConnWorker(conn_handler)
            worker.start()

    finally:
        socket_conn.close()



if __name__ == '__main__':
    main()