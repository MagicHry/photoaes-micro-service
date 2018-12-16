# coding=utf-8
"""
连接处理者
每一个socket连接应该对应着一个连接处理者
他们负责解析参数，调用美学模型
"""

from log import LogUtils as log
from conn import Config
from conn import FileUtils
class ConnHandler():

    def __init__(self, aes_model, socket, addr):
        self.aes_model = aes_model
        self.sock = socket
        self.addr = addr

    def handle_conn(self):
        """
        连接处理
        :return:
        """
        log.info('Socket conn eastablished with %s:%s' % (self.addr))
        # 检查美学模型是否是ok的，如果不是ok的，那么告诉客户端你凉了
        if self.aes_model == None or (not self.aes_model.initFinish()):
            self.sock.send(Config.CODE_ERROR)
            self.sock.close()
            log.info('Aes not init, return CODE_ERROR')
            return

        # 美学检测通过，返回CODE_OK，进行下一步
        self.sock.send(Config.CODE_OK.encode('utf-8'))

        # 正式接受数据
        received_path = self.recv_end()
        log.info('Received path at -> %s' % (received_path))

        # 路径校验
        suc, normed_path, msg = FileUtils.valid_path(received_path, relative_path=False)
        if not suc:
            self.sock.send(Config.CODE_FILE_ERROR.encode('utf-8'))
            self.sock.close()
            log.info('Received path at -> %s is invalid!' % (received_path))
            return

        # 进行美学评估
        aesScore = self.aes_model.runModelForSingleImg(normed_path, True)
        self.sock.send(aesScore.encode('utf-8'))
        self.sock.close()
        log.info('Aes over, score = %s for img->%s' % (aesScore, normed_path))

    def recv_end(self):
        """
        数据接受
        :return:
        """
        total_data = [];
        while True:
            data = self.sock.recv(Config.BUFFER_SIZE)
            if Config.END_MARKER in data:
                total_data.append(data[:data.find(Config.END_MARKER)])
                break
            total_data.append(data)
            if len(total_data) > 1:
                # check if end_of_data was split
                last_pair = total_data[-2] + total_data[-1]
                if Config.END_MARKER in last_pair:
                    total_data[-2] = last_pair[:last_pair.find(Config.END_MARKER)]
                    total_data.pop()
                    break
        return ''.join(total_data)



