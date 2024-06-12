"""
@Time    : 2024/1/9 16:04
@Author  : LuTuo
@report :allure generate ./report -o reports --clean

"""
# 获取本地路径
import datetime
import logging
import os

path = os.path.dirname(os.path.realpath(__file__))
# log_path是存放日志的路径
log_path = os.path.join(path, '../logs')
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log:
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, './%s.log' % datetime.datetime.now().strftime("%Y-%m-%d"))
        log_time = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        self.logger = logging.getLogger("".join(["\033[1;33m{}  \033[0m".format(log_time), '\033[1;33mISV_LuTuo\033[0m']))
        self.logger.setLevel(logging.INFO)
        # 日志输出格式
        self.formatter = logging.Formatter("%(asctime)s|%(levelname)s| %(message)s")

    def __console(self, level, message):
        # 创建一个fileHander，用于写入本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 避免日志重复
        self.logger.removeHandler(fh)
        # 关闭打开文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)
