import itertools

from bokeh.layouts import row
from bokeh.plotting import figure, show


def unzip(arr):
    result = []
    for inner in arr:
        for index, value in enumerate(inner):
            while index >= len(result):
                result.append([])

            result[index].append(value)

    return result


# Expects data like:
# [{"title": "...", "data": {"seriesName": [[1, 17], [2, 20]]}]
def plot_data(data):
    plots = []
    for chart in data:
        plot = figure(title=chart["title"], tooltips="@x, @y")

        palette = itertools.cycle(["#FF0000", "#000000", "#0000FF"])
        for color, (seriesName, series) in zip(palette, chart["data"].items()):
            # pylint: disable-next=W0632
            x, y = unzip(sorted(series, key=lambda a: a[0]))
            plot.line(x, y, color=color, legend_label=seriesName)
            plot.circle(x, y, color=color, legend_label=seriesName)

        plot.legend.click_policy = "hide"

        plots.append(plot)

    show(row(*plots))
