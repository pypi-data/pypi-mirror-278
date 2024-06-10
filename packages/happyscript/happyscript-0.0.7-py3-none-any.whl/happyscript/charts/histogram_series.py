import wx
from wx.lib import plot as wxplot
class HistogramSeries(object):
    def __init__(self, chart, name, binsize, color):
        self.__chart = chart
        self.__name = name
        self.__points = dict()
        self.__binsize = binsize
        self.__color = color
    @property
    def name(self):
        return self.__name
    def get_plot_object(self):
        bs = self.__binsize
        data = list()
        prev = None
        prev_val = None
        for k in sorted(self.__points.keys()):
            if prev is None:
                data.append( (k*bs,0) )
                data.append( (k*bs, self.__points[k]) )
            elif k != prev+1:
                data.append( ((prev+1)*bs,0) )
                data.append( (k*bs,0) )
                data.append( (k*bs, self.__points[k]) )
            else:
                if prev_val != self.__points[k]:
                    data.append( (k*bs, self.__points[k]) )
            data.append( ((k+1) * bs, self.__points[k]) )
            prev_val = self.__points[k]
            prev = k
        data.append( ((prev+1)*bs,0) )
        line = wxplot.PolyLine(data, colour=self.__color, width=2, style=wx.PENSTYLE_SOLID, legend=self.name)
        return line
    def add_value(self, x):
        binnum = int( x / self.__binsize )
        if binnum in self.__points:
            self.__points[binnum] = self.__points[binnum] + 1
        else:
            self.__points[binnum] = 1
        self.__chart.update()
    def add_values(self, data):
        for x in data:
            binnum = int( x / self.__binsize )
            if binnum in self.__points:
                self.__points[binnum] = self.__points[binnum] + 1
            else:
                self.__points[binnum] = 1
        self.__chart.update()
    def clear(self):
        self.__points = [0 for _ in range(100)]
        self.__chart.update()
    def get_points(self):
        return self.__points
