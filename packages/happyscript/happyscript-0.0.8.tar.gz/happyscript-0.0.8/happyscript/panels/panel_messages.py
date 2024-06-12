import wx
import datetime, logging
from .panelsbase import PanelMessages_Base
class PanelMessages( PanelMessages_Base ):
    def __init__( self, parent ):
        PanelMessages_Base.__init__(self, parent)
        self.lstMessages.InsertColumn(0, "Time", wx.LIST_FORMAT_RIGHT)
        self.lstMessages.InsertColumn(1, "Status")
        self.lstMessages.InsertColumn(2, "Message")
        self.lstMessages.SetColumnWidth(0, 75)
        self.lstMessages.SetColumnWidth(1, 70)
        self.lstMessages.SetColumnWidth(2, 100)
        self.loglevel = logging.WARN+1
    def OnListSize( self, event ):
        width = self.GetClientSize().width
        if width<160:
            width = 160;
        self.lstMessages.SetColumnWidth(2, width-150)
        event.Skip()
    def HandleLogData(self, logdata):
        if logdata.levelno < self.loglevel:
            return
        if logdata.levelno>=logging.ERROR:
            color = wx.RED
        elif logdata.levelno==logging.WARN+1:
            color = wx.BLUE
        elif logdata.levelno>=logging.WARN:
            color = wx.Colour(255, 128, 0)
        else:
            color = None
        self.AddListEntry(logdata.levelname, logdata.msg, color)
    def AddListEntry(self, result, msg, color=None):
        tstamp = datetime.datetime.now().strftime("%m/%d %H:%M")
        self.lstMessages.Append( (tstamp, result, msg) )
        cnt = self.lstMessages.GetItemCount()
        if color is not None:
            item = self.lstMessages.GetItem(cnt-1)
            item.SetTextColour(color)
            self.lstMessages.SetItem(item)
        self.lstMessages.EnsureVisible(cnt - 1)
        self.lstMessages.Update()
    def OnBtnClearList( self, event ):
        self.lstMessages.DeleteAllItems()
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
