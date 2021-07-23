import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

class Logger(object):
    def __init__(self, log_file_name, log_level, logger_name=None):
        # 创建一个logger
        self.__logger = logging.getLogger(logger_name)
        # 指定日志的最低输出级别，默认为WARN级别
        self.__logger.setLevel(log_level)
        # 创建一个handler用于写入日志文件
        file_handler = logging.FileHandler(log_file_name, mode="w", encoding='utf-8')
        # 创建一个handler用于输出控制台
        console_handler = logging.StreamHandler()
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s [%(filename)s line:%(lineno)d] - [%(levelname)s] %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # 给logger添加handler
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(console_handler)

    def get_log(self):
        return self.__logger

def job(text):
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    logger.info('{} --- {}'.format(text, t))

if __name__ == '__main__':
    logger = Logger(log_file_name='log.txt', log_level=logging.INFO).get_log()

    scheduler = BlockingScheduler()
    # 每隔 1分钟 运行一次 job 方法
    scheduler.add_job(job, 'interval', seconds=10, args=['job1'])

    scheduler.start()