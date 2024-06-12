import wx
from .formsbase import FormOnTestFailure_Base
class FormOnTestFailure( FormOnTestFailure_Base):
    static_item = None
    @classmethod
    def show(cls, testname):
        if cls.static_item is None:
            cls.static_item = FormOnTestFailure()
        cls.static_item.m_txtMessage.Label = "Test '%s' is gefaald.\nWat wil je doen ?" % testname
        cls.static_item.ShowModal()
        return cls.static_item.result
    @classmethod
    def cleanup(cls):
        if cls.static_item is not None:
            cls.static_item.Destroy()
            cls.static_item = None
    def __init__( self ):
        super().__init__(None)
        self.result = wx.ID_STOP
    def OnBtnRetry( self, event ):
        self.result = wx.ID_RETRY
        self.Close()
    def OnBtnSkip( self, event ):
        self.result = wx.ID_FORWARD
        self.Close()
    def OnBtnStop( self, event ):
        self.result = wx.ID_STOP
        self.Close()
