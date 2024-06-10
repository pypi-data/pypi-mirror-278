from .formsbase import FormStop_base
class FormStop( FormStop_base):
    def __init__( self, message, mngr ):
        super().__init__(mngr.dialog)
        self._mngr = mngr
        self.m_lblMessage.Label = message
    def OnBtnStop( self, event ):
        self._mngr.stop_scripts()
        self.Close()
    def update_message(self, msg):
        self.m_lblMessage.Label = msg
