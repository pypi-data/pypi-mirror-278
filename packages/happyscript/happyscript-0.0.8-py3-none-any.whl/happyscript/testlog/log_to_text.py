import logging
import time
import os
class LogToText(object):
    def __init__(self):
        self.logfilename = "happyscript.log"
        self.tempfilename = self.logfilename
        self.handle = None
        self.last_flush_time = time.time()
    def set_filename(self, filename, /, use_temp=False):
        self.close()
        self.logfilename = filename
        if use_temp:
            self.tempfilename = os.path.splitext(filename)[0] + ".tmp"
        else:
            self.tempfilename = filename
    def open(self):
        if self.handle is not None:
            return
        self.handle = open(self.tempfilename, "a+")
        self.last_flush_time = time.time()
        self.handle.write("****** STARTING log FILE ********\n")
    def close(self):
        if self.handle is None:
            return
        self.handle.write("****** CLOSING log FILE ********\n")
        self.handle.close()
        if self.logfilename!=self.tempfilename:
            if os.path.isfile(self.logfilename):
                os.remove(self.logfilename)
            if os.path.isfile(self.tempfilename):
                os.rename(self.tempfilename, self.logfilename)
        self.handle = None
    def handle_log(self, logdata):
        self.open()
        msg = logdata.msg.strip()
        if logdata.levelno >= logging.WARN:
            self.handle.write(f"{logdata.levelname}: {msg}\n")
        else:
            self.handle.write(msg+"\n")
        if logdata.exc_info is not None:
            self.handle.write(logdata.exc_info)
        t = time.time()
        if t - self.last_flush_time > 5:
            self.handle.flush()
            self.last_flush_time = t
