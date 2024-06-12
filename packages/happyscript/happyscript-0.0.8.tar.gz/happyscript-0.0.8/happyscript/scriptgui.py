import wx
import threading
from .scriptexceptions import ScriptUserAbortException
from .forms.form_askimage import FormAskImage
from .forms.form_askchoice import FormAskChoice
from .forms.form_stop import FormStop
class ScriptGui:
    def __init__(self, mngr):
        self._mngr = mngr
        self.__func = None
        self.__params = None
        self.__reply = None
        self.__have_reply = threading.Semaphore(0)
        self.m_stop_dialog = None
    def on_gui_timer(self):
        if self.__func is not None:
            func = self.__func
            self.__func = None
            try:
                self.__reply = func(*self.__params)
            except Exception as e:
                self.__reply = e
            self.__have_reply.release()
    def __run_with_timer(self, func, *params):
        self.__params = params
        self.__func = func
        self.__have_reply.acquire()
        if isinstance(self.__reply, Exception):
            raise self.__reply
        return self.__reply
    def do_func(self, func, *params):
        if func is None or not callable(func):
            raise Exception("Given function to execute is not something callable.")
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(func, *params )
        else:
            return func(*params)
    def ask(self, message, default_value="" ):
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(self.ask, message, default_value )
        result = None
        dlg = wx.TextEntryDialog( None, message, 'HappyScript', default_value )
        if dlg.ShowModal() == wx.ID_OK:
            result = dlg.GetValue()
        dlg.Destroy()
        if result is None:
            raise ScriptUserAbortException( "User did not provide value in dialog" )
        return result
    def ask_number(self, message, default_value=None ):
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(self.ask_number, message, default_value )
        result = None
        if default_value is None:
            default_value = ""
        else:
            default_value = "%d" % default_value
        dlg = wx.TextEntryDialog( None, message, 'HappyScript', default_value )
        while result is None:
            if dlg.ShowModal() == wx.ID_OK:
                txt_result = dlg.GetValue().encode("latin1")
            else:
                break
            try:
                result = int(txt_result)
            except:
                result = None
        dlg.Destroy()
        if result is None:
            raise ScriptUserAbortException( "User did not provide value in dialog" )
        return result
    def ask_yesno(self, message, cancel = False):
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(self.ask_yesno, message, cancel )
        style = wx.YES_NO|wx.CANCEL if cancel else wx.YES_NO
        dlg = wx.MessageDialog(None, message, 'HappyScript', style=style)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_YES:
            return True
        elif result == wx.ID_NO:
            return False
        raise ScriptUserAbortException( "User did not answer yes/no dialog" )
    def ask_image(self, message, filename, arrow_pos=None, yesno=False, cancel=False, numeric=False):
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(self.ask_image, message, filename, arrow_pos, yesno, cancel, numeric )
        form = FormAskImage(message, filename, arrow_pos, yesno, cancel, numeric )
        if form.ShowModal() == wx.ID_CANCEL:
            form.Destroy()
            raise ScriptUserAbortException( "User pressed cancel in dialog" )
        result = form.result
        form.Destroy()
        return result
    def ask_choice(self, message, choices, do_assert = True):
        if threading.currentThread().getName()=="ScriptThread":
            return self.__run_with_timer(self.ask_choice, message, choices )
        form = FormAskChoice(message, choices )
        if form.ShowModal() == wx.ID_CANCEL:
            if do_assert:
                form.Destroy()
                raise ScriptUserAbortException( "User pressed cancel in dialog" )
        result = form.result
        form.Destroy()
        return result
    def ask_open_file(self, message, wildcard):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.ask_open_file, message, wildcard)
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        dlg = wx.FileDialog(
            None, message, wildcard=wildcard, style=style)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return None
        return dlg.GetPath()
    def show_stop_dialog(self, message=None ):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.show_stop_dialog, message)
        if message is None:
            message = "Press the 'Stop' button to stop the test."
        if self.m_stop_dialog is None:
            self.m_stop_dialog = FormStop(message, self._mngr)
        else:
            self.m_stop_dialog.update_message(message)
        self.m_stop_dialog.Show()
    def close_stop_dialog(self):
        if self.m_stop_dialog is None:
            return
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.close_stop_dialog)
        self.m_stop_dialog.Destroy()
        self.m_stop_dialog = None
    def add_scatter_chart(self, name):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.add_scatter_chart, name)
        return self._mngr.charts.add_scatter_chart(name)
    def add_time_chart(self, name):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.add_time_chart, name)
        return self._mngr.charts.add_time_chart(name)
    def add_histogram(self, name, binsize):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.add_histogram, name, binsize)
        return self._mngr.charts.add_histogram(name, binsize)
    def add_matplotlib(self, name):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.add_matplotlib, name)
        return self._mngr.charts.add_matplotlib(name)
    def get_chart(self, name):
        return self._mngr.charts.get_chart(name)
    def delete_chart(self, name):
        if threading.currentThread().getName() == "ScriptThread":
            return self.__run_with_timer(self.delete_chart, name)
        self._mngr.charts.delete_chart(name)
