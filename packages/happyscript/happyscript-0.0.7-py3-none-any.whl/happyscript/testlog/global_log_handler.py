import logging, traceback
import queue
class LogData():
    msg = ""
    levelno = 0
    levelname = "[?]"
    exc_info = None
class PanelFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
    def format(self, record):
        if len(record.args) > 0:
            try:
                msg = record.msg % record.args
            except TypeError:
                msg = record.msg + " !!! BAD PARAMETERS !!! " + str(record.args)
        else:
            msg = record.msg
        return msg
class GlobalLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(None)
        formatter = PanelFormatter()
        self.setFormatter(formatter)
        self._callbacks = list()
        self._queue = queue.Queue()
    def add_callback(self, func):
        self._callbacks.append(func)
    def run_callbacks(self):
        while not self._queue.empty():
            data = self._queue.get()
            for func in self._callbacks:
                try:
                    func(data)
                except:
                    pass
    def emit(self, record):
        data = LogData()
        data.levelname = record.levelname
        data.levelno = record.levelno
        data.msg = self.format(record)
        if record.exc_info and str(record.exc_info[1])!="'Stopping parent script...'":
            exc_info = None
            tb = traceback.format_exception(record.exc_info[0], record.exc_info[1], record.exc_info[2])
            for line in tb[:-1 or None]:
                if line.startswith("Traceback "):
                    continue
                if "in execute_threadfunc" in line:
                    continue
                if exc_info is None:
                    exc_info = line
                else:
                    exc_info += "\r\n" + line
            data.exc_info = exc_info
        self._queue.put(data)
    def add_line_from_print(self, msg, level):
        data = LogData()
        data.levelno = level
        data.levelname = logging.getLevelName(level)
        data.msg = msg
        self._queue.put(data)
