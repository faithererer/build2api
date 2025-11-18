import logging

def setup_logging(log_file, prefix=None, level=logging.INFO):
    """
    配置日志记录器，使其输出到文件和控制台。
    支持一个可选的前缀，用于标识日志来源。

    每次调用都会重新配置处理器，以适应多进程环境。

    :param log_file: 日志文件的路径。
    :param prefix: (可选) 要添加到每条日志消息开头的字符串前缀。
    :param level: 日志级别。
    """
    logger = logging.getLogger('my_app_logger') 
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    base_format = '%(asctime)s - %(process)d - %(levelname)s - %(message)s'

    if prefix:
        log_format = f'%(asctime)s - %(process)d - %(levelname)s - {prefix} - %(message)s'
    else:
        log_format = base_format

    fh = logging.FileHandler(log_file)
    fh.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    
    logger.propagate = False
    
    return logger