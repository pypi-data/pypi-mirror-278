import re
import wx
from .formsbase import FormSerials_Base
class FormSerials( FormSerials_Base):
    static_item = None
    @classmethod
    def show(cls, count, labels = None, filters=None):
        if count<1 or count>5:
            return None
        if cls.static_item is None:
            cls.static_item = FormSerials()
        return cls.static_item.ask_serials(count, labels, filters)
    @classmethod
    def cleanup(cls):
        if cls.static_item is not None:
            cls.static_item.Destroy()
            cls.static_item = None
    def __init__( self ):
        super().__init__(None)
        self.labels = [ self.m_lblSerial1, self.m_lblSerial2, self.m_lblSerial3, self.m_lblSerial4, self.m_lblSerial5 ]
        self.texts = [ self.m_txtSerial1, self.m_txtSerial2, self.m_txtSerial3, self.m_txtSerial4, self.m_txtSerial5 ]
        self.result = False
    def ask_serials(self, count, labels, filters ):
        if count<1 or count>5:
            return None
        self.initializing = True
        if labels is None:
            labels = [ "Board 1", "Board 2", "Board 3", "Board 4", "Board 5" ]
        if filters is None:
            self.filters = [ None, None, None, None, None ]
        else:
            self.filters = filters
        self.valid = list()
        for i in range(count):
            self.texts[i].Value = ''
            self.labels[i].Label = labels[i]
            self.texts[i].Show()
            self.labels[i].Show()
            self.texts[i].SetBackgroundColour(wx.Colour(255,204,204))
            if self.filters[i] is not None:
                self.filters[i] = re.compile(self.filters[i])
            self.valid.append(False)
        for i in range(count,5):
            self.texts[i].Hide()
            self.labels[i].Hide()
        self.m_btnOK.Disable()
        self.initializing = False
        if self.ShowModal() != wx.ID_OK:
            return None
        if False in self.valid:
            return None
        serials = list()
        for i in range(count):
            serials.append( self.texts[i].Value.strip() )
        return serials
    def handle_ontext(self, num):
        if self.initializing or num<0 or num>4:
            return
        txt = self.texts[num].Value.strip()
        valid = False
        if len(txt)==0:
            valid = False
        elif self.filters[num] is not None:
            valid = True if self.filters[num].search(txt) else False
        else:
            valid = True
        self.texts[num].SetBackgroundColour( wx.Colour(204,255,204) if valid else wx.Colour(255,204,204) )
        self.valid[num] = valid
        if not self.m_btnOK.IsEnabled() and not (False in self.valid):
            self.m_btnOK.Enable()
        elif self.m_btnOK.IsEnabled() and (False in self.valid):
            self.m_btnOK.Disable()
        self.Update()
        self.Refresh()
    def OnText1( self, event ):
        self.handle_ontext(0)
    def OnText2( self, event ):
        self.handle_ontext(1)
    def OnText3( self, event ):
        self.handle_ontext(2)
    def OnText4( self, event ):
        self.handle_ontext(3)
    def OnText5( self, event ):
        self.handle_ontext(4)
    def handle_enter(self, num):
        if self.initializing or num<0 or num>4:
            return
        if num==4 or not self.texts[num+1].IsShown():
            self.m_btnOK.SetFocus()
        else:
            self.texts[num+1].SetFocus()
    def OnEnter1( self, event ):
        self.handle_enter(0)
    def OnEnter2( self, event ):
        self.handle_enter(1)
    def OnEnter3( self, event ):
        self.handle_enter(2)
    def OnEnter4( self, event ):
        self.handle_enter(3)
    def OnEnter5( self, event ):
        self.handle_enter(4)
    def OnBtnCancel( self, event ):
        self.EndModal(wx.ID_CANCEL)
    def OnBtnOK( self, event ):
        self.EndModal(wx.ID_OK)
