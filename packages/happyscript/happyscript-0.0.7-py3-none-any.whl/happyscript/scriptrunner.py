import datetime, logging, threading
from .scriptexceptions import ScriptUserAbortException
from .scriptexceptions import ScriptRecursiveAbortException
class ScriptThreadRunner:
    logger = logging.getLogger("happyscript.runner")
    MARKER_LEVEL = 25
    def __init__(self, ctrl):
        self._ctrl = ctrl
        self._recurse_count = 0
        self.top_script_name = ''
        self.last_result = False
        self.busy = False
    def execute_script(self, script_name, script_func, argvalues):
        self.last_result = False
        self.busy = True
        if threading.currentThread().getName()=="ScriptThread":
            self.execute_threadfunc(script_name, script_func, argvalues)
        elif self._recurse_count>0:
            self.logger.error( "Script '%s' already running.  Wait until it completed." % self.top_script_name )
        else:
            self.top_script_name = script_name
            thread = threading.Thread(name = "ScriptThread", target=self.execute_threadfunc, args=(script_name, script_func, argvalues) )
            thread.start()
    def execute_threadfunc(self, script_name, script_func, argvalues):
        if self._recurse_count<0:
            self._recurse_count = 0
        tstamp = datetime.datetime.now().strftime("%m/%d_%H:%M")
        self.logger.log(self.MARKER_LEVEL, "__________%s__________%s__" % (script_name, tstamp) )
        test_passed = False
        all_tests_done = False
        try:
            self._recurse_count += 1
            self._ctrl.set_busy(True)
            script_func( *argvalues )
            test_passed = True
        except ScriptUserAbortException as _:
            self.logger.error("Script stopped by user")
        except Exception as e:
            if self._ctrl.m_stop_script:
                self.logger.error("Script stopped by user")
            else:
                logging.error(str(e), exc_info = e)
        finally:
            self._recurse_count -= 1
            if self._recurse_count<=0:
                all_tests_done = True
            if test_passed:
                self.logger.log(self.MARKER_LEVEL, "\\_________%s__________ PASS ______/" % script_name )
            else:
                self.logger.log(self.MARKER_LEVEL, "\\_________%s__________ FAIL ______/" % script_name )
        if self._recurse_count>0 and test_passed==False:
            raise ScriptRecursiveAbortException("Stopping parent script...")
        if all_tests_done:
            self._recurse_count = 0
            self.top_script_name=''
            self.last_result = test_passed
            self._ctrl.set_busy(False)
            self.busy = False
class ScriptRunner:
    logger = logging.getLogger("happyscript.runner")
    def __init__(self, script_params, script_readers, script_control):
        self.script_params = script_params
        self._readers = script_readers
        self._recurse_count = 0
        self.start_ok = False
        self.thread_runner = ScriptThreadRunner(script_control)
    @property
    def test_passed(self):
        return self.start_ok and self.thread_runner.last_result
    @property
    def busy(self):
        return self.thread_runner.busy
    def run_script(self, script_name, **argv):
        parts = script_name.split(".")
        if len(parts) != 3:
            self.logger.error("Must provide script name as dirname.filename.scriptname")
            return
        self.start_script(parts[0], parts[1], parts[2], **argv)
    def start_script(self, group_name, filename, funcname, **extra_params):
        self.start_ok = False
        scriptname = "%s.%s.%s" % (group_name, filename, funcname)
        if not group_name in self._readers:
            self.logger.error("Cannot start %s : group %s not found" % (scriptname, group_name))
            return
        func = self._readers[group_name].get_func(filename, funcname)
        if func is None:
            self.logger.error("Cannot start %s : function not found" % scriptname)
            return
        if (extra_params is None) or (not isinstance(extra_params,dict)):
            extra_params = dict()
        (argvalues, missing) = self.script_params.get_parameters(func, extra_params)
        if len(missing)>0:
            self.logger.error( "Error : missing value for parameter(s) %s" % ("".join(missing) ) )
            self.logger.error( "        Make sure to use valid names as parameters for your function.")
            self.logger.log(self.MARKER_LEVEL, "\\_________%s_________ ERROR ______/" % scriptname )
            return
        self.thread_runner.execute_script(scriptname, func, argvalues)
        self.start_ok = True
