import wx
import wx.py as py
import configparser
try:
    from agw import aui
except ImportError:
    import wx.lib.agw.aui as aui
from ..scriptartwork import ScriptArtwork
from .form_ontestfailure import FormOnTestFailure
from .form_serials import FormSerials
from ..panels.panel_messages import PanelMessages
from ..panels.panel_tests import PanelTests
from ..panels.panel_log import PanelLog
from ..charts.panel_charts import PanelCharts
from .formsbase import FormMain_Base
class FormMain(FormMain_Base):
    VALID_OPERATORS = ("OPERATOR", "TECHNICIAN", "ENGINEER", "EXPERT")
    def __init__(self, script_manager ):
        ScriptArtwork.register()
        super().__init__(None)
        self.logFile = None
        self._script_manager = script_manager
        self.on_gui_timer = None
        self.on_log_timer = None
        self.current_user = None
        scriptLocals = { "_mngr_": self._script_manager }
        self._shell_window = py.shell.Shell( self, -1, introText = None, locals=scriptLocals )
        info = wx.aui.AuiPaneInfo().Caption("Python shell").Name("PY_Shell")
        info.Bottom().Layer(1).Dock().CloseButton(False)
        self.m_mgr.AddPane(self._shell_window, info)
        info = wx.aui.AuiPaneInfo().Caption("Control Panels").Name("ControlPanels")
        info.Left().Layer(1).Position(0).CloseButton(False).MinSize( (100,200) )
        self._nbk_control_panels = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_mgr.AddPane(self._nbk_control_panels, info)
        info = wx.aui.AuiPaneInfo().Caption("Messages").Name("Messages")
        info.Center().Layer(1).Dock().CloseButton(False).MinSize( (100,200) )
        self.msgArea = PanelMessages(self)
        self.m_mgr.AddPane(self.msgArea, info)
        info = wx.aui.AuiPaneInfo().Caption("Tests").Name("Tests")
        info.Left().Layer(1).Dock().CloseButton(False).MinSize( (100,200) )
        self.pnlTests = PanelTests(self, self._script_manager)
        self.m_mgr.AddPane(self.pnlTests, info)
        info = wx.aui.AuiPaneInfo().Caption("Log").Name("Log")
        info.Bottom().Layer(1).Dock().CloseButton(False).MinSize( (100,200) )
        self.logPane = PanelLog(self)
        self.m_mgr.AddPane(self.logPane, info)
        info = wx.aui.AuiPaneInfo().Caption("Charts").Name("Charts")
        info.Bottom().Layer(1).Dock().CloseButton(False).MinSize( (100,200) )
        self.chartsPane = PanelCharts(self)
        self.m_mgr.AddPane(self.chartsPane, info)
        info = wx.aui.AuiPaneInfo().Caption("Scripts").Name("Scripts")
        info.Right().Layer(1).CloseButton(False).MinSize( (150,150) )
        self._nbk_scripts = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_mgr.AddPane(self._nbk_scripts, info)
        self.ALL_BUTTONS = [self.m_btnTestList, self.m_btnMessages, self.m_btnLogging, self.m_btnPython, self.m_btnScripts, self.m_btnControls, self.m_btnCharts ]
        self.ALL_PANELS  = [self._nbk_scripts, self._nbk_control_panels, self.logPane, self.pnlTests, self.msgArea, self._shell_window, self.chartsPane ]
    def BeforeShow(self):
        self.SwitchUser(None)
        self.m_guiTimer.Start(20)
    def OnMnuLayoutClicked( self, event ):
        tb = event.GetEventObject()
        tb.SetToolSticky(event.GetId(), True)
        rect = tb.GetToolRect(event.GetId())
        pt = tb.ClientToScreen(rect.GetBottomLeft())
        pt = self.ScreenToClient(pt)
        self.PopupMenu(self.m_mnuLayout, pt)
        tb.SetToolSticky(event.GetId(), False)
    def AddCustomPanel(self, title, panelType, **args):
        args["parent"] = self._nbk_control_panels
        newPanel = panelType(**args)
        self._nbk_control_panels.AddPage( newPanel, title, False)
        return newPanel
    def HideCustomPanels(self):
        if self._nbk_control_panels.GetPageCount()==0:
            info = self.m_mgr.GetPaneByName("ControlPanels")
            info.Hide()
            self.m_mgr.Update()
    def SwitchUser(self, user):
        if user is None:
            ini = configparser.ConfigParser()
            ini.read( ["happyscript.ini"] )
            user = ini.get("varia", "CurrentUser", fallback="ENGINEER" )
            if user not in self.VALID_OPERATORS:
                user = "OPERATOR"
        if self.current_user == user:
            return
        if self.current_user is not None:
            self.SavePosition()
        self.current_user = user
        self.RestorePosition()
        if self.current_user=="OPERATOR":
            hide_panels = [self.logPane, self._nbk_scripts, self._nbk_control_panels, self._shell_window, self.chartsPane]
            bitmap = ScriptArtwork.GetBitmap("user_operator")
            center = self.msgArea
            enable_buttons = list()
        elif self.current_user=="TECHNICIAN":
            hide_panels = [self.logPane, self._nbk_scripts, self._shell_window, self.chartsPane]
            bitmap = ScriptArtwork.GetBitmap("user_technician")
            center = self.msgArea
            enable_buttons = [ self.m_btnControls ]
        elif self.current_user=="ENGINEER":
            hide_panels = list()
            bitmap = ScriptArtwork.GetBitmap("user_engineer")
            center = self.logPane
            enable_buttons = self.ALL_BUTTONS
        else:
            hide_panels = list()
            bitmap = ScriptArtwork.GetBitmap("user_expert")
            center = self._shell_window
            enable_buttons = self.ALL_BUTTONS
        self.m_btnLayout.SetBitmap(bitmap)
        for btn in self.ALL_BUTTONS:
            enable = True if btn in enable_buttons else False
            self.m_mnuToolbar.EnableTool(btn.GetId(), enable )
        if center==self.logPane:
            self.m_mnuToolbar.EnableTool(self.m_btnLogging.GetId(), False)
        elif center==self._shell_window:
            self.m_mnuToolbar.EnableTool(self.m_btnPython.GetId(), False)
        pane = self.m_mgr.GetPane(center)
        pane.Dock().Center()
        if not pane.IsShown():
            pane.Show(True)
        for panel in [self.msgArea, self.logPane, self._shell_window]:
            if panel == center:
                continue
            pane = self.m_mgr.GetPane(panel)
            if pane.dock_direction == aui.AUI_DOCK_CENTER:
                pane.Dock().Bottom()
        if self._nbk_control_panels.PageCount==0:
            self.m_mnuToolbar.EnableTool(self.m_btnControls.GetId(), False)
            hide_panels.append(self._nbk_control_panels)
        for panel in hide_panels:
            pane = self.m_mgr.GetPane(panel)
            if pane.IsShown():
                if pane.IsDocked():
                    pane.Float()
                pane.Show(False)
        self.m_mnuToolbar.Show()
        self.m_mgr.Update()
    def RestorePosition( self ):
        if self.current_user not in self.VALID_OPERATORS:
            return
        section = "LAYOUT_" + self.current_user
        ini = configparser.ConfigParser()
        ini.read( ["happyscript.ini"] )
        if ini.has_section(section):
            x = ini.getint(section, "WindowX")
            y = ini.getint(section, "WindowY")
            width = ini.getint(section, "WindowWidht" )
            height = ini.getint(section, "WindowHeight" )
            self.SetPosition((x,y))
            self.SetSize((width, height))
            if ini.has_option(section, "pane_layout"):
                panes = ini.get(section, "pane_layout")
                try:
                    self.m_mgr.LoadPerspective(panes, False)
                except:
                    pass
    def SavePosition( self, also_save_user = False ):
        if self.current_user not in self.VALID_OPERATORS:
            return
        section = "LAYOUT_" + self.current_user
        x, y = self.GetPosition()
        width, height = self.GetSize()
        ini = configparser.ConfigParser()
        ini.read( ["happyscript.ini"] )
        if not ini.has_section(section):
            ini.add_section(section)
        ini.set(section, "WindowX", str(x) )
        ini.set(section, "WindowY", str(y) )
        ini.set(section, "WindowWidht", str(width) )
        ini.set(section, "WindowHeight", str(height) )
        ini.set(section, "pane_layout", self.m_mgr.SavePerspective() )
        if also_save_user:
            if not ini.has_section("varia"):
                ini.add_section("varia")
            ini.set("varia", "CurrentUser", self.current_user )
        with open("happyscript.ini", "w") as inifile:
            ini.write(inifile)
    def OnFormClose(self, event):
        self.m_guiTimer.Stop()
        FormOnTestFailure.cleanup()
        FormSerials.cleanup()
        self.SavePosition(True)
        self.m_mgr.UnInit()
        self.Destroy()
        wx.GetApp().ExitMainLoop()
    def TogglePanel(self, panel):
        pane = self.m_mgr.GetPane(panel)
        if pane.IsShown():
            if pane.IsDocked():
                pane.Float()
            pane.Show(False)
        else:
            pane.Dock()
            pane.Show(True)
        self.m_mgr.Update()
    def OnBtnScripts( self, event ):
        self.TogglePanel(self._nbk_scripts)
    def OnBtnPython( self, event ):
        self.TogglePanel(self._shell_window)
    def OnBtnLogging( self, event ):
        self.TogglePanel(self.logPane)
    def OnBtnMessages( self, event ):
        self.TogglePanel(self.msgArea)
    def OnBtnTestList( self, event ):
        self.TogglePanel(self.pnlTests)
    def OnBtnCharts( self, event ):
        self.TogglePanel(self.chartsPane)
    def OnBtnControls( self, event ):
        self.TogglePanel(self._nbk_control_panels)
    def OnLayoutOperator( self, event ):
        self.SwitchUser("OPERATOR")
    def OnLayoutTechnician( self, event ):
        self.SwitchUser("TECHNICIAN")
    def OnLayoutEngineer( self, event ):
        self.SwitchUser("ENGINEER")
    def OnLayoutExpert( self, event ):
        self.SwitchUser("EXPERT")
    def OnResetLayout( self, event ):
        event.Skip()
    def OnBtnExit( self, event ):
        self.Close()
    def PushShellCommand(self, cmd):
        self._shell_window.push(cmd, True)
    def OnGuiTimer( self, event ):
        if self.on_gui_timer is not None:
            self.on_gui_timer()
        if self.on_log_timer is not None:
            self.on_log_timer()
