import logging
import wx
try:
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False
class MatPlotLibChart(wx.Panel):
    def __init__(self, parent_control, name):
        super().__init__(parent_control, -1)
        self.__name = name
        self.__dirty = False
        self.__on_update_func = None
        if not HAVE_MATPLOTLIB:
            logging.error("Matplotlib is not installed.")
            self.__figure = None
            return
        self.__figure = Figure(dpi=None, figsize=(2, 2))
        self.__figure.set_tight_layout(True)
        self.canvas = FigureCanvas(self, -1, self.__figure)
        self.__toolbar = NavigationToolbar(self.canvas)
        self.__toolbar.Realize()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.__toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
    @property
    def name(self):
        return self.__name
    @property
    def figure(self):
        return self.__figure
    def configure(self, /, x_label=None, y_label=None, title=None,
                  y_log=None, x_log=None, x_range=None, y_range=None):
        if not HAVE_MATPLOTLIB: return
        if title is not None and isinstance(title, str):
            if len(self.figure.axes)>0:
                self.figure.axes[0].set_title(title)
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
        if antialiasing:
            logging.warn("Antialiasing not supported for matplotlib chart")
        self.__dirty = True
        if self.__on_update_func is not None:
            self.__on_update_func()
    def redraw(self):
        self.antiAlias = False
        self.do_redraw()
        self.__dirty = False
    def do_redraw(self):
        if not HAVE_MATPLOTLIB: return
        self.canvas.draw()
    def clear(self):
        if not HAVE_MATPLOTLIB: return
        try:
            self.figure.clf()
        except:
            pass
        pass
    def delete_series(self, name):
        logging.error("Deleting series not supported for matplotlib charts")
    def add_series(self, name):
        logging.error("Use matplotlib API for adding series")
    def get_series(self, name):
        logging.error("Getting series not supported for matplotlib charts")
        return None
    def get_data_as_text(self):
        logging.error("Getting series not supported for matplotlib charts")
        return "Data not available for matplotlib charts"
