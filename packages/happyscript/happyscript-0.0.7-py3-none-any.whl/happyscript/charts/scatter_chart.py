from .scatter_series import ScatterSeries
from .chart import Chart
class ScatterChart(Chart):
    def do_add_series(self, name):
        return ScatterSeries(self, name, color=self.get_series_color() )
    def get_data_as_text(self):
        lines = ""
        all_data = list()
        data_lengths = list()
        line = ""
        for (k,v) in self._series.items():
            line += k + "_x\t" + k + "_y\t"
            data = v.get_points()
            all_data.append(data)
            data_lengths.append(len(data))
        lines += line.strip() + "\r\n"
        num_series = len(data_lengths)
        num_lines = max(data_lengths)
        for i in range(num_lines):
            line = ""
            for j in range(num_series):
                if data_lengths[j]>i:
                    line += "\t".join(map(str,all_data[j][i]))+"\t"
                else:
                    line += "\t\t"
            lines += line.strip() + "\r\n"
        return lines
