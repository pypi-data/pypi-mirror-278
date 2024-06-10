from .histogram_series import HistogramSeries
from .chart import Chart
class HistogramChart(Chart):
    def __init__(self, parent_control, name, binsize):
        super().__init__(parent_control, name)
        self.__binsize = binsize
        self._xlabel = "Value"
        self._ylabel = "Count"
    def do_add_series(self, name):
        return HistogramSeries(self, name, self.__binsize, color=self.get_series_color() )
    def get_data_as_text(self):
        lines = ""
        data = list()
        min_x = None
        max_x = None
        line = "Value"
        for ser in self._series:
            line += "\t" + ser
        lines += line.strip() + "\r\n"
        for ser in self._series.values():
            points = ser.get_points()
            if min_x is None:
                min_x = min(points.keys())
            else:
                min_x = min( min_x, min(points.keys()))
            if max_x is None:
                max_x = max(points.keys())
            else:
                max_x = max( max_x, max(points.keys()))
            data.append( points )
        for x in range(min_x,max_x+1):
            line = str( x * self.__binsize )
            for pts in data:
                if x in pts:
                    line += "\t%d" % pts[x]
                else:
                    line += "\t0"
            lines += line.strip() + "\r\n"
        return lines
