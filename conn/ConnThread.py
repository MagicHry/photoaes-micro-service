# coding=utf-8
"""
连接处理线程
"""
import threading
class ConnWorker(threading.Thread):

    def __init__(self, conn_handler):
        threading.Thread.__init__(self)
        self.conn_handler = conn_handler
        self.setDaemon(True)

    def run(self):
        self.conn_handler.handle_conn()