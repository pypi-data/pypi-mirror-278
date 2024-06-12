import time
from .time_series import TimeSeries
from .chart import Chart
class TimeChart(Chart):
    start_time = None
    def do_add_series(self, name):
        if self.start_time is None:
            self.start_time = time.time()
        return TimeSeries(self, name, self.get_series_color(), self.start_time)
    def get_data_as_text(self):
        lines = ""
        all_data = list()
        data_lengths = list()
        next_t = list()
        data_pos = list()
        line = "time\t"
        for (k,v) in self._series.items():
            line += k + "\t"
            data = v.get_points()
            all_data.append(data)
            data_lengths.append(len(data))
            data_pos.append(0)
            next_t.append(None)
        lines += line.strip() + "\r\n"
        num_series = len(data_lengths)
        max_lines = sum(data_lengths)
        for j in range(num_series):
            if data_lengths[j]>0:
                next_t[j] = all_data[j][0][0]
        for _ in range(max_lines):
            try:
                t = min(x for x in next_t if x is not None)
            except:
                break
            line = "%f" % t
            for j in range(num_series):
                if next_t[j] is None:
                    line += "\t"
                    continue
                if next_t[j] <= t+0.0001:
                    pos = data_pos[j]
                    line += "\t" + str(all_data[j][pos][1])
                    pos += 1
                    if pos<data_lengths[j]:
                        data_pos[j] = pos
                        next_t[j] = all_data[j][pos][0]
                    else:
                        next_t[j] = None
                else:
                    line += "\t"
            lines += line.strip() + "\r\n"
        return lines
    def add_values(self, t=None, **values):
        if t is None:
            t = time.time()
        for name, value in values.items():
            series = self.get_series(name)
            if series is not None:
                series.add_value(value, t)
