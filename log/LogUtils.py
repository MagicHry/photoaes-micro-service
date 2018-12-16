# coding=utf-8
import logging
"""
Flask-Logger
简易的封装与配置
"""
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

def register_logger():
    """
    注册本地输出日志
    :return:
    """
    logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)


def error(msg):
    logging.error(msg)
    print(msg)

def info(msg):
    logging.info(msg)
    print(msg)



