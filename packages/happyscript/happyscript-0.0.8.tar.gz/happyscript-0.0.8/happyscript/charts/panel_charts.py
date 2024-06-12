import wx
import os
import logging
from ..panels.panelsbase import PanelCharts_Base
from ..charts.scatter_chart import ScatterChart
from ..charts.time_chart import TimeChart
from ..charts.histogram_chart import HistogramChart
from ..charts.matplotlib_chart import MatPlotLibChart
class PanelCharts( PanelCharts_Base):
    def __init__( self, parent):
        super().__init__(parent)
        self.__dirty = False
        self.charts = dict()
        self.default_savedir = os.getcwd()
    def update(self):
        self.__dirty = True
    def OnRedrawTimer( self, event ):
        if self.__dirty:
            self.__dirty = False
            for x in self.charts.values():
                x.redraw()
    def OnRadioBoxMouseMode( self, event ):
        for chart in self.charts.values():
            if self.m_rbxMouseMode.Selection==0:
                chart.enableZoom = False
                chart.enableDrag = False
            elif self.m_rbxMouseMode.Selection==1:
                chart.enableZoom = True
                chart.enableDrag = False
            else:
                chart.enableDrag = True
                chart.enableZoom = False
    def BtnCopyDataClick( self, event ):
        index = self.m_nbkPlots.GetSelection()
        if index == wx.NOT_FOUND or self.m_nbkPlots.GetPageText(index) not in self.charts:
            wx.MessageBox( "Cannot find chart on current page", "HappyScript", wx.OK | wx.ICON_ERROR )
        chart = self.charts[self.m_nbkPlots.GetPageText(index)]
        try:
            clipdata = wx.TextDataObject()
            lines = chart.get_data_as_text()
            clipdata.SetText(lines)
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()
            wx.MessageBox( "Data written to clipboard", "HappyScript", wx.OK | wx.ICON_INFORMATION )
        except:
            wx.MessageBox( "Could not write text to clipboard", "HappyScript", wx.OK | wx.ICON_ERROR )
    def OnMakePretty( self, event ):
        index = self.m_nbkPlots.GetSelection()
        if index == wx.NOT_FOUND or self.m_nbkPlots.GetPageText(index) not in self.charts:
            wx.MessageBox( "Cannot find chart on current page", "HappyScript", wx.OK | wx.ICON_ERROR )
        chart = self.charts[self.m_nbkPlots.GetPageText(index)]
        chart.update(antialiasing = True)
    def OnBtnSaveBitmap( self, event ):
        index = self.m_nbkPlots.GetSelection()
        if index == wx.NOT_FOUND or self.m_nbkPlots.GetPageText(index) not in self.charts:
            wx.MessageBox( "Cannot find chart on current page", "HappyScript", wx.OK | wx.ICON_ERROR )
        chart = self.charts[self.m_nbkPlots.GetPageText(index)]
        try:
            with wx.FileDialog(self, "Output file name", wildcard="PNG files(*.png)|*.png",
                    defaultDir = self.default_savedir,
                    style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fdlg:
                if fdlg.ShowModal() == wx.ID_OK:
                    filename = fdlg.GetPath()
                    chart.SaveFile(filename)
                    self.default_savedir = os.path.dirname(filename)
        except:
            wx.MessageBox( "Could not write bitmap", "HappyScript", wx.OK | wx.ICON_ERROR )
    def get_chart(self, name):
        if name in self.charts:
            return self.charts[name]
        else:
            return None
    def delete_chart(self, name):
        if not name in self.charts:
            return
        ch = self.charts[name]
        page_num = self.m_nbkPlots.FindPage(ch)
        if page_num != wx.NOT_FOUND:
            self.m_nbkPlots.DeletePage(page_num)
        del self.charts[name]
    def add_scatter_chart(self, name ):
        self.delete_chart(name)
        chart = ScatterChart(self.m_nbkPlots, name)
        chart.on_update = self.update
        self.charts[name] = chart
        self.m_nbkPlots.AddPage( chart, name, True)
        return chart
    def add_time_chart(self, name ):
        self.delete_chart(name)
        chart = TimeChart(self.m_nbkPlots, name)
        chart.on_update = self.update
        self.charts[name] = chart
        self.m_nbkPlots.AddPage( chart, name, True)
        return chart
    def add_histogram(self, name, binsize ):
        self.delete_chart(name)
        chart = HistogramChart(self.m_nbkPlots, name, binsize)
        chart.on_update = self.update
        self.charts[name] = chart
        self.m_nbkPlots.AddPage( chart, name, True)
        return chart
    def add_matplotlib(self, name ):
        self.delete_chart(name)
        chart = MatPlotLibChart(self.m_nbkPlots, name)
        assert chart.figure is not None, "Could not add matplotlib chart."
        chart.on_update = self.update
        self.charts[name] = chart
        self.m_nbkPlots.AddPage( chart, name, True)
        return chart
