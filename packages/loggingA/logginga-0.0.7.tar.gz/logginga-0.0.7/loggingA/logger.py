import logging
from logging.handlers import TimedRotatingFileHandler
import inspect


class LoggerA:
    def __init__(self, level=logging.DEBUG, log_file=None, when='midnight', interval=1, backup_count=7,
                 format_str='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        formatter = logging.Formatter(format_str)

        # 添加输出到文件的处理器
        if log_file:
            file_handler = TimedRotatingFileHandler(log_file, when=when, interval=interval, backupCount=backup_count)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # 添加输出到控制台的处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, message):
        func_name = inspect.currentframe().f_back.f_code.co_name
        self.logger.debug(f"[{func_name}] {message}")

    def info(self, message):
        func_name = inspect.currentframe().f_back.f_code.co_name
        self.logger.info(f"[{func_name}] {message}")

    def warning(self, message):
        func_name = inspect.currentframe().f_back.f_code.co_name
        self.logger.warning(f"[{func_name}] {message}")

    def error(self, message):
        func_name = inspect.currentframe().f_back.f_code.co_name
        self.logger.error(f"[{func_name}] {message}")

    def critical(self, message):
        func_name = inspect.currentframe().f_back.f_code.co_name
        self.logger.critical(f"[{func_name}] {message}")

    def update_logger_extra(self, extra_info):
        """
        更新日志记录器的额外上下文
        :param extra_info: 包含额外信息的字典
        """
        for key, value in extra_info.items():
            setattr(logging.LoggerAdapter(self.logger, {}), key, value)


def example_function(logger):
    logger.debug("Inside example_function")


if __name__ == "__main__":
    # Example usage
    logger = LoggerA(level=logging.DEBUG, log_file="example.log")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Example of logging within a function
    example_function(logger)
