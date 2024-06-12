import sys
import logging
class PrintRedirect:
    _redir = None
    _reerr = None
    _old_redir = None
    def __init__(self, globalloghandler, level=None):
        self.level = logging.INFO if level is None else level
        self.loghandler = globalloghandler
    def write(self,txt):
        txt = txt.strip()
        if txt=='\n' or len(txt)==0:
            return
        if self.level==logging.ERROR and txt=="^":
            return
        level = self.level
        if "[FAIL]" in txt:
            level = logging.ERROR
            txt = txt.replace("[FAIL]","").strip()
        elif "[ERROR]" in txt:
            level = logging.ERROR
            txt = txt.replace("[ERROR]","").strip()
        elif "[PASS]" in txt:
            level = logging.WARN+1
            txt = txt.replace("[PASS]","").strip()
        elif "[WARN]" in txt:
            level = logging.WARN
            txt = txt.replace("[WARN]","").strip()
        self.loghandler.add_line_from_print(txt, level)
    def flush(self):
        pass
    @classmethod
    def start_redirection(cls, handler):
        cls._redir = PrintRedirect(handler)
        cls._reerr = PrintRedirect(handler,logging.ERROR)
        cls._old_redir = ( sys.stdout, sys.stderr )
        sys.stdout=cls._redir
        sys.stderr=cls._reerr
    @classmethod
    def stop_redirection(cls):
        if cls._old_redir is not None:
            sys.stdout, sys.stderr = cls._old_redir
            cls._old_redir = None
