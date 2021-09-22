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


# Expects data like [{"title": "...", "array": [[1, 17], [2, 20]]}]
def plot_data(data):
    plots = []
    for series in data:
        plot = figure(title=series["title"], tooltips="@x, @y")
        # pylint: disable-next=W0632
        x, y = unzip(sorted(series["array"], key=lambda a: a[0]))
        plot.line(x, y)
        plot.circle(x, y)

        plots.append(plot)

    show(row(*plots))
