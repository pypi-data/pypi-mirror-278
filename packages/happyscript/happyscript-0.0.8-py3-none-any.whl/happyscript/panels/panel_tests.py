import logging
from enum import Enum, IntEnum
import wx
from .panelsbase import PanelTests_Base
from ..scriptartwork import ScriptArtwork
from ..forms.form_ontestfailure import FormOnTestFailure
class RunState(Enum):
    IDLE = 1
    RUN_SINGLE = 2
    RUNNING = 3
    PAUSED = 4
    FINISHED = 5
    DO_SETUP_FUNC = 6
    DO_CLEANUP_FUNC = 7
    WAIT_TEST_END = 8
    ERROR = 9
    START_FIRST = 10
class RunAction(Enum):
    NONE = 1
    STOP_ALL = 2
    PAUSE = 6
class TestIcon(IntEnum):
    FAIL = 0
    PASS = 1
    TODO = 2
    WARN = 3
    IDLE = 4
    RUNNING = 5
    PAUSED = 6
    @classmethod
    def GetImageList(cls):
        il = wx.ImageList(16, 16)
        il.Add( wx.ArtProvider.GetBitmap("test_fail") )
        il.Add( wx.ArtProvider.GetBitmap("test_pass") )
        il.Add( wx.ArtProvider.GetBitmap("test_todo") )
        il.Add( wx.ArtProvider.GetBitmap("test_warning" ))
        il.Add( wx.ArtProvider.GetBitmap("test_idle" ))
        il.Add( wx.ArtProvider.GetBitmap("test_running"))
        il.Add( wx.ArtProvider.GetBitmap("test_pause"))
        return il
class TestInfo:
    def __init__(self, description, scriptname, **args):
        self.description = description
        self.scriptname = scriptname
        self.extra_args = args
        self.passed = False
class PanelTests( PanelTests_Base):
    logger = logging.getLogger("happyscript")
    def __init__( self, parent, mngr ):
        PanelTests_Base.__init__(self, parent)
        self.on_sequence_start_callback = None
        self.on_sequence_end_callback = None
        self.mngr = mngr
        self.__run_state = RunState.IDLE
        self.__run_action = RunAction.NONE
        self.__testnum = -1
        self.tests = list()
        self.init_list()
    def init_list(self):
        ScriptArtwork.register()
        self.il = TestIcon.GetImageList()
        self.m_lstTests.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.m_lstTests.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL))
        info = wx.ListItem()
        info.Mask = wx.LIST_MASK_IMAGE
        info.Image = -1
        info.Align = wx.LIST_FORMAT_LEFT
        info.Text = ""
        self.m_lstTests.InsertColumn(0, info)
        info.Align = wx.LIST_FORMAT_LEFT
        info.Text = "Name"
        self.m_lstTests.InsertColumn(1, info)
        info.Mask = wx.LIST_MASK_IMAGE
        info.Image = -1
        info.Align = wx.LIST_FORMAT_LEFT
        info.Text = "?"
        self.m_lstTests.InsertColumn(2, info)
        self.m_lstTests.SetColumnWidth(0, 50)
        self.m_lstTests.SetColumnWidth(1, 100)
        self.m_lstTests.SetColumnWidth(2, 50)
    def OnListSize( self, event ):
        width = self.GetClientSize().width
        if width<160:
            width = 160;
        self.m_lstTests.SetColumnWidth(1, width-110)
        event.Skip()
    def OnListRightClick( self, event ):
        self.selected_row = event.Index
        print( self.selected_row )
        pos = wx.GetMousePosition()
        pos = self.ScreenToClient( pos )
        self.PopupMenu( self.m_mnuTestList, pos  )
    def add_test(self, description, scriptname, **args):
        test = TestInfo(description, scriptname, **args)
        self.tests.append(test)
        self.m_lstTests.Append( ('', description, '') )
        cnt = self.m_lstTests.GetItemCount()
        self.m_lstTests.SetItem(cnt-1, 0, "", imageId=TestIcon.IDLE )
        self.m_lstTests.SetItem(cnt-1, 2, "", imageId=TestIcon.TODO )
    def get_tests(self, is_passed, include = None, exclude = None):
        result = list()
        for i in range(len(self.tests)):
            if (i==self.__testnum) or (self.tests[i].passed!=is_passed):
                continue
            if (exclude is not None) and (self.tests[i].description in exclude):
                continue
            if (include is None) or (self.tests[i].description in include):
                result.append(self.tests[i].description)
        return result
    def OnBtnStartClick( self, event ):
        self.state = RunState.START_FIRST
    def OnBtnPauseClick( self, event ):
        if self.state==RunState.PAUSED:
            self.state = RunState.RUNNING
        else:
            self.__run_action = RunAction.PAUSE
    def OnBtnStopClick( self, event ):
        self.__run_action = RunAction.STOP_ALL
    def reset_icons(self):
        for index in range(len(self.tests)):
            self.m_lstTests.SetItem(index, 0, "", imageId=TestIcon.IDLE )
            self.m_lstTests.SetItem(index, 2, "", imageId=TestIcon.TODO )
            self.tests[index].passed = False
    @property
    def state(self):
        return self.__run_state
    @state.setter
    def state(self, value):
        if value==RunState.START_FIRST:
            self.__run_action = RunAction.NONE
            if self.state != RunState.IDLE:
                raise Exception("Test state is not idle, cannot start test sequence.")
        self.__run_state = value
        if value==RunState.IDLE:
            self.m_tmrStateMachine.Stop()
        else:
            self.m_tmrStateMachine.StartOnce(10)
    def OnTmrStateMachine( self, event ):
        if self.state == RunState.IDLE:
            self.m_tmrStateMachine.Stop()
        elif self.state == RunState.START_FIRST:
            self.__testnum = -1
            self.logger.debug("Starting new test sequence")
            self.m_txtStatus.Label = "Starting"
            self.m_txtStatus.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
            self.reset_icons()
            self.m_btnStart.Enabled = False
            self.m_btnStop.Enabled = True
            self.state = RunState.DO_SETUP_FUNC
        elif self.state == RunState.DO_SETUP_FUNC:
                if self.on_sequence_start_callback is None:
                    self.state = RunState.RUNNING
                else:
                    try:
                        result = self.on_sequence_start_callback()
                        if isinstance(result, str):
                            self.m_txtStatus.Label = result
                            self.state = RunState.ERROR
                        elif isinstance(result, bool) and result==False:
                            self.m_txtStatus.Label = "Test run aborted"
                            self.state = RunState.ERROR
                        else:
                            self.state = RunState.RUNNING
                    except Exception as e:
                        self.logger.critical("Error in callback at beginning of test", exc_info=e)
                        self.m_txtStatus.Label = "Internal error #1"
                        self.state = RunState.ERROR
                        return
        elif self.state == RunState.RUNNING:
            self.__testnum += 1
            if self.__testnum >= len(self.tests):
                self.logger.debug("No more test to execute")
                self.state = RunState.DO_CLEANUP_FUNC
            elif self.__run_action==RunAction.STOP_ALL:
                self.__run_action = RunAction.NONE
                self.logger.debug("Stopping all tests")
                self.state = RunState.DO_CLEANUP_FUNC
            else:
                self.m_lstTests.EnsureVisible(self.__testnum)
                self.m_lstTests.SetItem(self.__testnum, 0, "", imageId=TestIcon.RUNNING )
                self.m_lstTests.SetItem(self.__testnum, 2, "", imageId=TestIcon.TODO )
                self.m_lstTests.Update()
                self.m_txtStatus.Label = "Running test %d" % (self.__testnum+1)
                sname = self.tests[self.__testnum].scriptname
                sargs = self.tests[self.__testnum].extra_args
                if sargs is None:
                    self.mngr._script_runner.run_script(sname)
                else:
                    self.mngr._script_runner.run_script(sname, **sargs)
                self.state = RunState.WAIT_TEST_END
        elif self.state == RunState.WAIT_TEST_END:
            if self.mngr._script_runner.busy:
                self.state = RunState.WAIT_TEST_END
            else:
                test_pass = self.mngr._script_runner.test_passed
                index = self.__testnum
                if test_pass:
                    self.m_lstTests.SetItem(index, 0, "", imageId=TestIcon.IDLE )
                self.m_lstTests.SetItem(index, 2, "", imageId=TestIcon.PASS if test_pass else TestIcon.FAIL )
                self.m_lstTests.Update()
                self.tests[index].passed = test_pass
                if test_pass:
                    self.state = RunState.RUNNING
                else:
                    self.m_lstTests.SetItem(index, 0, "", imageId=TestIcon.WARN )
                    result = FormOnTestFailure.show(self.tests[index].description)
                    self.m_lstTests.SetItem(index, 0, "", imageId=TestIcon.IDLE )
                    if result==wx.ID_RETRY:
                        self.__testnum -= 1
                        self.logger.warn("Test failed, doing retry")
                        self.state = RunState.RUNNING
                    elif result==wx.ID_FORWARD:
                        self.logger.warn("Test skipped by user")
                        self.state = RunState.RUNNING
                    else:
                        self.logger.warn("Test sequence aborted by user")
                        self.state = RunState.DO_CLEANUP_FUNC
        elif self.state == RunState.RUN_SINGLE:
            self.logger.error("Run single not yet implemented")
            self.state = RunState.ERROR
        elif self.state == RunState.PAUSED:
            self.logger.error("Pause not yet implemented")
            self.state = RunState.ERROR
        elif self.state == RunState.DO_CLEANUP_FUNC:
            if self.on_sequence_end_callback is None:
                self.state = RunState.FINISHED
            else:
                try:
                    self.on_sequence_end_callback()
                    self.state = RunState.FINISHED
                except Exception as e:
                    self.logger.critical("Error in callback at end of test", exc_info=e)
                    self.m_txtStatus.Label = "Internal error #2"
                    self.state = RunState.ERROR
        elif self.state == RunState.FINISHED:
            self.logger.debug("Tests finished")
            num_fails = sum( 1 for x in self.tests if not x.passed)
            if num_fails==0:
                self.m_txtStatus.Label = "All test OK"
            elif num_fails==1:
                self.m_txtStatus.Label = "1 test failed !"
                self.m_txtStatus.SetForegroundColour(wx.RED)
            else:
                self.m_txtStatus.Label = "%d tests failed !" % num_fails
            self.m_txtStatus.SetForegroundColour(wx.RED)
            self.state = RunState.IDLE
            self.m_btnStart.Enabled = True
            self.m_btnStop.Enabled = False
        elif self.state == RunState.ERROR:
            self.state = RunState.IDLE
            self.m_btnStart.Enabled = True
            self.m_btnStop.Enabled = False
        else:
            self.logger.critical("run_state invalid in testlist state machine")
            self.m_txtStatus = "Internal error #3"
            self.state = RunState.IDLE
            self.m_btnStart.Enabled = True
            self.m_btnStop.Enabled = False
