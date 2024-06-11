import logging
from colorlog import ColoredFormatter


def init_log():
    # 日志记录器
    logger = logging.getLogger()

    # 设置日志级别，只有大于等于这个级别的日志才能输出
    logger.setLevel(logging.INFO)

    # 设置日志格式
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s %(white)s[%(asctime)s]%(reset)s "
        "%(blue)s[%(filename)s:%(lineno)d]%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    # 输出到控制台
    to_console = logging.StreamHandler()
    to_console.setFormatter(formatter)
    logger.addHandler(to_console)

