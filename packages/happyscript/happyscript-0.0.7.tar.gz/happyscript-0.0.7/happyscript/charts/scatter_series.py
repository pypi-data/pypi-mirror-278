import wx
from wx.lib import plot as wxplot
class ScatterSeries(object):
    def __init__(self, chart, name, color):
        self.__chart = chart
        self.__name = name
        self.__points = list()
        self.__color = color
    @property
    def name(self):
        return self.__name
    def get_plot_object(self):
        line = wxplot.PolyLine(self.__points, colour=self.__color, width=2, style=wx.PENSTYLE_SOLID, legend=self.name)
        return line
    def add_point(self, x, y):
        self.__points.append( (x, y) )
        self.__chart.update()
    def clear(self):
        self.__points = list()
        self.__chart.update()
    def get_points(self):
        return self.__points
