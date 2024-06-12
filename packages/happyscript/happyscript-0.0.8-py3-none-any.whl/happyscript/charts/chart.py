import wx
from wx.lib import plot as wxplot
class Chart(wxplot.PlotCanvas):
    COLORS = ( wx.Colour(68,114,196), wx.Colour(237,125,49), wx.Colour(165,165,165), wx.Colour(255,193,4),
               wx.Colour(91,155,213), wx.Colour(112,173,71), wx.Colour(38,68,120), wx.Colour(158,72,14),
               wx.Colour(99,99,99),  wx.Colour(153,115,0), wx.Colour(37,94,145), wx.Colour(67,104,43),
               wx.Colour(105,142,208),  wx.Colour(241,151,90), wx.Colour(183,183,183), wx.Colour(255,205,51),
               wx.Colour(124,175,221),
               )
    def __init__(self, parent_control, name):
        super().__init__(parent_control, -1)
        self.__name = name
        self.enableLegend = True
        self.enableGrid = True
        self.antiAlias = False
        self._series = dict()
        self.__dirty = False
        self.__on_update_func = None
        self.__num_series_added = 0
        self._xrange = None
        self._yrange = None
        self.configure(title=name, x_label="", y_label="", x_log=False, y_log=False)
    def get_series_color(self):
        idx = self.__num_series_added % len(self.COLORS)
        self.__num_series_added += 1
        return self.COLORS[idx]
    @property
    def name(self):
        return self.__name
    def configure(self, /, x_label=None, y_label=None, title=None,
                  y_log=None, x_log=None, x_range=None, y_range=None):
        if title is not None:
            self._title = title if isinstance(title, str) else str(title)
            self.enablePlotTitle = True if len(self._title)>0 else False
        if x_label is not None:
            self._xlabel = x_label if isinstance(x_label, str) else str(x_label)
            self.enableXAxisLabel = True if len(self._xlabel)>0 else False
        if y_label is not None:
            self._ylabel = y_label if isinstance(y_label, str) else str(y_label)
            self.enableYAxisLabel = True if len(self._ylabel)>0 else False
        if x_log is not None:
            self._xlog = True if x_log else False
        if y_log is not None:
            self._ylog = True if y_log else False
        if x_range is not None:
            ok = False
            if type(x_range) is tuple and len(x_range)==2:
                try:
                    if x_range[0]+1 < x_range[1]+1:
                        self._xrange = x_range
                    ok = True
                except:
                    pass
            if not ok:
                print(f"x_range {x_range} is invalid")
        if y_range is not None:
            ok = False
            if type(y_range) is tuple and len(y_range)==2:
                try:
                    if y_range[0]+1 < y_range[1]+1:
                        self._yrange = y_range
                    ok = True
                except:
                    pass
            if not ok:
                print(f"y_range {y_range} is invalid")
        self.logScale = (self._xlog, self._ylog)
        if len(self._series)>0:
            self.update()
    @property
    def on_update(self):
        return self.__on_update_func
    @on_update.setter
    def on_update(self, value):
        if value is None or callable(value):
            self.__on_update_func = value
    @property
    def dirty(self):
        return self.__dirty
    def update(self, / , antialiasing=False):
        self.antiAlias = antialiasing
        self.__dirty = True
        if self.__on_update_func is not None:
            self.__on_update_func()
    def redraw(self):
        self.enableAntiAliasing = self.antiAlias
        self.antiAlias = False
        self.do_redraw()
        self.__dirty = False
    def do_redraw(self):
        plot_objects = list()
        try:
            for series in self._series.values():
                if len(series.get_points())>0:
                    plot_objects.append( series.get_plot_object() )
        except RuntimeError:
            return
        if len(plot_objects)>0:
            pg = wxplot.PlotGraphics(plot_objects, self._title, self._xlabel, self._ylabel)
            try:
                self.Draw(pg, xAxis=self._xrange, yAxis=self._yrange)
            except:
                pass
    def delete_series(self, name):
        if name in self._series:
            del self._series[name]
            if hasattr(self, name):
                delattr(self, name)
    def add_series(self, name):
        if ( not name.isidentifier() or
             name in ['update', 'redraw', 'add_series', 'delete_series'] or
             ( hasattr(self, name) and name not in self._series) ):
            raise ValueError("Series name '%s' is invalid" % name)
        self.delete_series(name)
        series = self.do_add_series(name)
        if series is not None:
            self._series[name] = series
            setattr(self, name, series)
        self.update()
        return series
    def do_add_series(self, name):
        return None
    def get_series(self, name):
        if name in self._series:
            return self._series[name]
        else:
            return None
    def get_data_as_text(self):
        return ""
