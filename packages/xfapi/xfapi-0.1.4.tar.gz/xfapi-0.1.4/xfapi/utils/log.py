import logging
import logging.handlers
import time
import datetime

class LoggingTool:
    def __init__(self, log_path):
        self.log_path = log_path

    def setup_logger(self):
        # 格式化时间
        datetime_now = time.strftime("%Y-%m-%d")

        # 创建logger实例对象
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 文件处理器
        fh = logging.handlers.TimedRotatingFileHandler(f"{self.log_path}/app.log", when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        fh.setFormatter(logging.Formatter(
            '%(asctime)s  %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        fh.setLevel(level="INFO")

        logger.addHandler(fh)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level="DEBUG")
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(console_handler)

        return logger