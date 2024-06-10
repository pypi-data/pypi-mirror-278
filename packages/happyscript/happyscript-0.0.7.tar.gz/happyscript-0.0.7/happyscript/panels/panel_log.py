import wx
import logging
from .panelsbase import PanelLog_Base
class PanelLog( PanelLog_Base ):
    def __init__( self, parent ):
        super().__init__(parent)
        self.lstCommandHistory = list()
        self.posInCommandHistory = 0
        self.callback = None
        self.first_time_in_commandline = True
        self.loglevel = logging.INFO
        self._stop_log = False
    def OnBtnClearLog( self, event ):
        self.wx_txtLog.Clear()
    def HandleLog(self, logdata):
        if logdata.levelno < self.loglevel:
            return
        if self._stop_log:
            return
        if logdata.levelno >= logging.WARN:
            self.wx_txtLog.AppendText(f"{logdata.levelname}: {logdata.msg}\r\n")
        else:
            self.wx_txtLog.AppendText(logdata.msg+"\r\n")
        if logdata.exc_info is not None:
            self.wx_txtLog.AppendText(logdata.exc_info)
    def OnSelectLogLevel( self, event ):
        sel = self.m_cboLogLevel.GetStringSelection().lower()
        if sel=="warning":
            self.loglevel = logging.WARN
        elif sel=="info":
            self.loglevel = logging.INFO
        else:
            self.loglevel = logging.DEBUG
            logger = logging.getLogger('')
            if logger.getEffectiveLevel() > logging.DEBUG:
                logger.setLevel(logging.DEBUG)
    def OnBtnStop( self, event ):
        self._stop_log = True
        self.m_btnStop.Enable(False)
        self.m_btnResume.Enable(True)
        self.m_btnResume.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
    def OnBtnResume( self, event ):
        self._stop_log = False
        self.m_btnStop.Enable(True)
        self.m_btnResume.Enable(False)
        self.m_btnResume.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
    def OnSetFocus( self, event ):
        if self.first_time_in_commandline:
            self.first_time_in_commandline = False
            self.wx_txtCommand.Clear()
        event.Skip()
    def OnCmdKeyUp( self, event ):
        if len(self.lstCommandHistory)==0:
            return;
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.posInCommandHistory -= 1
        elif key== wx.WXK_DOWN:
            self.posInCommandHistory += 1
        else:
            return
        if self.posInCommandHistory<0:
            self.posInCommandHistory = 0
        elif self.posInCommandHistory>=len(self.lstCommandHistory):
            self.posInCommandHistory = len(self.lstCommandHistory)-1
        self.wx_txtCommand.Value = self.lstCommandHistory[self.posInCommandHistory]
    def OnCmdEnter( self, event ):
        if self.callback is None:
            print("[ERROR] no callback defined for when you type a command")
            return
        cmd = self.wx_txtCommand.GetValue().strip()
        if cmd not in self.lstCommandHistory:
            self.lstCommandHistory.append(cmd)
            self.posInCommandHistory = len(self.lstCommandHistory)
        self.wx_txtCommand.Clear()
        self.callback(cmd)
