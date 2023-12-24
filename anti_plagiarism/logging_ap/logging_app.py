import logging as lg
from datetime import datetime


class MyFormatter(lg.Formatter):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)

    def format(self, record):
        log_msg = f"{datetime.now()} {record.funcName}_function {record.levelname.upper()} {record.msg}"
        return log_msg

class DebugAndInfoFilter(lg.Filter):
    def filter(self, record):
        return record.levelno <= lg.INFO

class CriticalAndErrorFilter(lg.Filter):
    def filter(self, record):
        return record.levelno >= lg.WARNING



my_logger = lg.getLogger("logger")
my_logger.setLevel(lg.DEBUG)


debug_and_info_handler = lg.FileHandler("logging_de.log")
debug_and_info_handler.addFilter(DebugAndInfoFilter())
debug_and_info_handler.setLevel(lg.DEBUG)
debug_and_info_handler.setFormatter(MyFormatter())

critical_and_error_handler = lg.FileHandler("errors.log")
critical_and_error_handler.addFilter(CriticalAndErrorFilter())
critical_and_error_handler.setLevel(lg.ERROR)
critical_and_error_handler.setFormatter(MyFormatter())


# добавила обработчики в логеры
my_logger.addHandler(debug_and_info_handler)
my_logger.addHandler(critical_and_error_handler)