import time
import wx
from wx.lib import plot as wxplot
class TimeSeries(object):
    def __init__(self, chart, name, color, start_time=None):
        self.__chart = chart
        self.__name = name
        self.__points = list()
        self.__color = color
        self.__start_time = time.time() if start_time is None else start_time
    @property
    def name(self):
        return self.__name
    def get_plot_object(self):
        line = wxplot.PolyLine(self.__points, colour=self.__color, width=2, style=wx.PENSTYLE_SOLID, legend=self.name)
        return line
    def add_value(self, value, t=None):
        if t is None:
            t = time.time()
        self.__points.append( (t-self.__start_time, value) )
        self.__chart.update()
    def clear(self):
        self.__points = list()
        self.__chart.update()
    def get_points(self):
        return self.__points
