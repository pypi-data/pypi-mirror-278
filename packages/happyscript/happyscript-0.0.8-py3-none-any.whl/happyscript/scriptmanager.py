import os, traceback, logging, time
import wx
from .forms.form_main import FormMain
from .panels.panel_scripts2 import PanelScripts2
from .scriptcontrol import ScriptControl
from .testlog.printredirect import PrintRedirect
from .scriptrunner import ScriptRunner
from .scriptparams import ScriptParams
from .scriptreader import ScriptReader
from .scriptgui import ScriptGui
from .scriptinfo import ScriptInfo
from .forms.form_serials import FormSerials
from .testlog.global_log_handler import GlobalLogHandler
from .testlog.log_to_text import LogToText
class TestLogHandler(logging.FileHandler):
    def __init__(self, filename):
        super().__init__(filename)
    def emit(self, record):
        if record.msg is None:
            return
        record.msg = record.msg.strip()
        if len(record.msg.rstrip())==0:
            return
        if record.exc_info and str(record.exc_info[1])!="'Stopping parent script...'":
            tb = traceback.format_exception(record.exc_info[0], record.exc_info[1], record.exc_info[2])
            for line in tb[:-1 or None]:
                if line.startswith("Traceback "):
                    continue
                if "in execute_threadfunc" in line:
                    continue
                record.msg = record.msg + "\r\n" + line
            record.exc_info = None
        super().emit(record)
class ScriptManager(object):
    dialog = None
    logger = logging.getLogger("happyscript")
    def __init__(self, title=None, colors = None, use_yaml=False):
        fixedcolors = [ (226, 239, 217), (222, 235, 246), (255, 242, 204), (237, 237, 237),
                        (251, 229, 213), (217, 226, 243) ]
        self.on_batch_start = None
        self.on_batch_end = None
        self.logfiles_defined = False
        logging.getLogger('').setLevel(logging.INFO)
        logging.addLevelName(logging.WARN+1, "PASS")
        self.loghandler = GlobalLogHandler()
        logging.getLogger('').addHandler(self.loghandler)
        paramiko_log = logging.getLogger("paramiko")
        paramiko_log.propagate = False
        self.textlogoutput = LogToText()
        self.loghandler.add_callback(self.textlogoutput.handle_log)
        self.app = wx.App()
        self.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
        self.dialog = FormMain(self)
        self.charts = self.dialog.chartsPane
        self.loghandler.add_callback(self.dialog.logPane.HandleLog)
        self.loghandler.add_callback(self.dialog.msgArea.HandleLogData)
        self.dialog.on_log_timer = self.on_log_timer
        self.ctrl = ScriptControl()
        self.gui = ScriptGui(self)
        self.dialog.on_gui_timer = self.gui.on_gui_timer
        self.info = ScriptInfo( self.dialog.pnlTests, use_yaml )
        self._script_params = ScriptParams(self.gui)
        self._script_params.on_add_object = self._on_add_object
        self._script_readers = dict()
        self._script_runner = ScriptRunner(self._script_params, self._script_readers, self.ctrl)
        self.ctrl.on_run_script = self._script_runner.run_script
        self._script_params.add_objects( ctrl=self.ctrl, gui=self.gui, info=self.info )
        self.dialog.pnlTests.on_sequence_start_callback = self.handle_batch_start
        self.dialog.pnlTests.on_sequence_end_callback = self.handle_batch_end
        self.set_logfiles()
        if title is not None:
            self.dialog.Title = title
            self.dialog.pnlTests.Label = title
        if colors is not None and colors in range(len(fixedcolors)):
            rgb = fixedcolors[colors]
            color = wx.Colour(rgb[0], rgb[1], rgb[2])
            self.dialog.pnlTests.SetBackgroundColour(color)
            self.dialog.msgArea.SetBackgroundColour(color)
        self.dialog.Show()
    def on_log_timer(self):
        self.loghandler.run_callbacks()
    def set_logfiles(self, fname = None, fdir = None, use_temp = False):
        if fdir is None:
            fdir = "./log"
        if fname is None:
            fname = "happyscript"
        fname,_ = os.path.splitext(fname)
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        self.info.set_filename( os.path.join(fdir, fname+".yml") )
        self.textlogoutput.set_filename( os.path.join(fdir, fname+".log"), use_temp = use_temp )
        self.logger.info("Writing log to %s" % os.path.join(fdir, fname+".log"))
        self.logfiles_defined = True
    def close_logfiles(self):
        self.set_logfiles()
        self.logfiles_defined = False
    def stop_scripts(self):
        self.ctrl.stop()
    def add_object(self, objName, theObject):
        self._script_params.add_object( objName, theObject)
    def add_objects(self, *args, **kwargs):
        self._script_params.add_objects(*args, **kwargs)
    def _on_add_object(self, obj_name, obj_value):
        if obj_value is None:
            self.logger.warning( f"Object with name {obj_name} is None." )
        else:
            self.logger.info("Added object %s" %obj_name)
            self.dialog.PushShellCommand("%s = _mngr_._script_params.get_param('%s')" % (obj_name, obj_name))
    def add_scripts(self, script_dir, group_name = None):
        full_path = os.path.normpath(os.path.abspath(script_dir))
        self.logger.info( "Adding scripts in %s" % full_path )
        if group_name is None:
            group_name = os.path.basename(full_path)
        reader = ScriptReader(script_dir, group_name)
        self._script_readers[group_name] = reader
        reader.reload()
        newPanel = PanelScripts2(self.dialog._nbk_scripts, reader, self.ctrl )
        self.dialog._nbk_scripts.AddPage( newPanel, group_name, False)
    def add_test(self, description, scriptname, **args):
        self.dialog.pnlTests.add_test( description, scriptname, **args )
    def add_tests(self, testlist):
        for x in testlist:
            if len(x)==3:
                self.add_test( x[0], x[1], **x[2] )
            elif len(x)==2:
                self.add_test( x[0], x[1] )
            else:
                self.logger.critical("Expected at least description and test name in test list.")
    @property
    def on_cmd_line(self):
        return self.dialog.logPane.callback
    @on_cmd_line.setter
    def on_cmd_line(self, value):
        self.dialog.logPane.callback = value
    def handle_batch_start(self):
        result = True
        self.info.clear()
        if self.logfiles_defined:
            self.close_logfiles()
        if not self.on_batch_start is None and callable(self.on_batch_start):
            result = self.on_batch_start()
        if not self.logfiles_defined:
            fname = "test_" + time.strftime("%y%m%d-%H%M%S")
            self.set_logfiles(fname, use_temp=True)
        return result
    def handle_batch_end(self):
        if not self.on_batch_end is None and callable(self.on_batch_end):
            self.on_batch_end()
        self.info.update_file(True)
        self.close_logfiles()
    def ask_serials(self, count, labels = None, filters=None, add_to_info=True):
        serials = FormSerials.show(count, labels, filters)
        if add_to_info:
            self.info.set_serials(serials)
        return serials
    def add_custom_panel(self, title, panelType, **args):
        return self.dialog.AddCustomPanel(title, panelType, **args)
    def run(self):
        self.dialog.BeforeShow()
        PrintRedirect.start_redirection(self.loghandler)
        print("Happyscript started")
        self.app.MainLoop()
        PrintRedirect.stop_redirection()
        self.info.update_file(True)
        self.textlogoutput.close()
