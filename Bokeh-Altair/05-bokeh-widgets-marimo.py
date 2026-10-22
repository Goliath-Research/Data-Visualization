# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "numpy",
#     "pandas",
#     "bokeh",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    from bokeh.layouts import column, row
    from bokeh.models import ColorPicker, ColumnDataSource, CustomJS, Select, Slider
    from bokeh.palettes import Bokeh5
    from bokeh.plotting import figure

    return (
        Bokeh5,
        ColorPicker,
        ColumnDataSource,
        CustomJS,
        Select,
        Slider,
        column,
        figure,
        mo,
        np,
        pd,
        row,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bokeh Widgets

    ## Objectives

    - Link a slider to the marker size, and place that slider above, below, or beside the figure.
    - Link a color picker to the fill color, and a select menu to the marker name.
    - Put the slider, the color picker, and the select menu on one figure.
    - Draw `y = x**2`, then use three sliders to change `a`, `h`, and `k` in `y = a(x - h)**2 + k`.
    - Hide or mute automobile points from the legend, by body style.

    ## Background

    These widgets are Bokeh models. `js_link` connects a widget property to a glyph property in the browser. The size slider writes `value` into the glyph's `size`. The color picker writes `color` into `fill_color`. The select menu writes `value` into `marker`.

    The quadratic chart uses `CustomJS`. When `a`, `h`, or `k` changes, the callback recomputes `y` in that chart's own data source. The static `y = x**2` chart is a separate figure, so the sliders do not change it.

    `legend.click_policy` is `"hide"` or `"mute"`. Hide removes the glyph. Mute fades it.

    ## Datasets Used

    - Five points built in this lesson, and a quadratic sampled at 1,000 x values from -5 to 5.
    - **Automobile Dataset** from the UCI Machine Learning Repository. The legend charts use highway mpg, price, and body style.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the file is read from

    Pandas can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website.
    - **Inside a web browser.** This lesson can run inside a web page. The browser only lets a page download files from websites that allow it. This security rule is called **CORS**. The UCI website does not allow it, so the browser blocks that download.

    This lesson reads a copy of the Automobile file stored on GitHub. GitHub allows a browser page to read its files, so the copy works in both places. The original UCI address is kept in a comment.
    """)
    return


@app.cell
def _():
    auto_file = (
        "https://raw.githubusercontent.com/Goliath-Research/"
        "Introduction-to-Data-Science/main/"
        "04-Introduction%20to%20Pandas/public/imports-85.data"
    )
    # UCI address, blocked in the browser:
    # https://archive.ics.uci.edu/ml/machine-learning-databases/autos/imports-85.data
    headers = [
        "symboling",
        "normalized_losses",
        "make",
        "fuel_type",
        "aspiration",
        "num_doors",
        "body_style",
        "drive_wheels",
        "engine_location",
        "wheel_base",
        "length",
        "width",
        "height",
        "curb_weight",
        "engine_type",
        "num_cylinders",
        "engine_size",
        "fuel_system",
        "bore",
        "stroke",
        "compression_ratio",
        "horsepower",
        "peak_rpm",
        "city_mpg",
        "highway_mpg",
        "price",
    ]
    marker_names = ["star", "square", "plus", "diamond", "triangle", "circle"]
    return auto_file, headers, marker_names


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A size slider

    The slider runs from 1 to 100 and starts at 30. It is linked to the circle size. This layout puts the slider above the figure. Each layout below is a new figure and a new slider.
    """)
    return


@app.cell
def _(ColumnDataSource, Slider, column, figure):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=350,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        marker="circle_dot",
        source=_source,
        color="orchid",
        size=30,
    )
    _slider = Slider(start=1, end=100, step=1, value=30, title="Size")
    _slider.js_link("value", _glyph.glyph, "size")
    _layout = column(_slider, _fig)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slider sits below the figure.
    """)
    return


@app.cell
def _(ColumnDataSource, Slider, column, figure):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=350,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        marker="circle_dot",
        source=_source,
        color="orchid",
        size=30,
    )
    _slider = Slider(start=1, end=100, step=1, value=30, title="Size")
    _slider.js_link("value", _glyph.glyph, "size")
    _layout = column(_fig, _slider)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slider sits to the right of the figure.
    """)
    return


@app.cell
def _(ColumnDataSource, Slider, figure, row):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=350,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        marker="circle_dot",
        source=_source,
        color="orchid",
        size=30,
    )
    _slider = Slider(start=1, end=100, step=1, value=30, title="Size")
    _slider.js_link("value", _glyph.glyph, "size")
    _layout = row(_fig, _slider)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A color picker

    The picker starts at forest green. `js_link` writes the chosen color into `fill_color`. The markers are squares.
    """)
    return


@app.cell
def _(ColorPicker, ColumnDataSource, column, figure):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=350,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        marker="square",
        source=_source,
        color="forestgreen",
        size=30,
    )
    _picker = ColorPicker(title="Circles Color", color="forestgreen")
    _picker.js_link("color", _glyph.glyph, "fill_color")
    _layout = column(_picker, _fig)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A marker menu

    The menu lists `star`, `square`, `plus`, `diamond`, `triangle`, and `circle`. The starting marker is `circle`. The chosen name is written into the glyph's `marker`.
    """)
    return


@app.cell
def _(ColumnDataSource, Select, column, figure, marker_names):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=350,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        source=_source,
        color="orangered",
        size=30,
        marker="circle",
    )
    _select = Select(title="Select marker", value="circle", options=marker_names)
    _select.js_link("value", _glyph.glyph, "marker")
    _layout = column(_select, _fig)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slider, color, and marker together

    One figure has all three links. The widgets sit in a column to the right of the chart.
    """)
    return


@app.cell
def _(ColorPicker, ColumnDataSource, Select, Slider, column, figure, marker_names, row):
    _source = ColumnDataSource(data={"x": [1, 2, 3, 4, 5], "y": [3, 1, 5, 2, 4]})
    _fig = figure(
        x_range=(0, 6),
        y_range=(0, 6),
        toolbar_location=None,
        width=400,
        height=300,
    )
    _glyph = _fig.scatter(
        x="x",
        y="y",
        source=_source,
        color="deepskyblue",
        line_color="white",
        size=30,
        marker="circle",
    )
    _slider = Slider(start=1, end=100, step=1, value=30, title="Size")
    _slider.js_link("value", _glyph.glyph, "size")
    _picker = ColorPicker(title="Circles Color", color="deepskyblue")
    _picker.js_link("color", _glyph.glyph, "fill_color")
    _select = Select(title="Select marker", value="circle", options=marker_names)
    _select.js_link("value", _glyph.glyph, "marker")
    _layout = row(_fig, column(_select, _picker, _slider))
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A static quadratic

    `x` is 1,000 evenly spaced values from -5 to 5. `y` is `x` squared. The axis limits are -5 to 5 on both axes, so the arms of the parabola leave the frame.
    """)
    return


@app.cell
def _(ColumnDataSource, figure, np):
    quad_x = np.linspace(-5, 5, 1000)
    _source = ColumnDataSource(data=dict(x=quad_x, y=quad_x**2))
    _fig = figure(
        y_range=(-5, 5),
        x_range=(-5, 5),
        width=600,
        height=400,
        title="Quadratic Function",
    )
    _fig.line("x", "y", source=_source, line_width=2, color="green", line_alpha=0.7)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sliders for `a`, `h`, and `k`

    The callback reads the three slider values and writes `y[i] = a * (x[i] - h)**2 + k`. `a` starts at 1. `h` and `k` start at 0, so the curve starts as `y = x**2`. This source belongs to the interactive figure only.

    The first layout puts the sliders to the right. The second layout stacks the sliders above a new copy of the chart.
    """)
    return


@app.cell
def _(ColumnDataSource, CustomJS, Slider, column, figure, np, row):
    _x = np.linspace(-5, 5, 1000)
    _source = ColumnDataSource(data=dict(x=_x, y=_x**2))
    _fig = figure(
        y_range=(-5, 5),
        x_range=(-5, 5),
        width=600,
        height=400,
        title="Quadratic Function",
    )
    _fig.line("x", "y", source=_source, line_width=2, color="green", line_alpha=0.7)
    _slider_a = Slider(start=-5, end=5, value=1, step=0.1, title="Quadratic Coefficient")
    _slider_h = Slider(start=-5, end=5, value=0, step=0.1, title="Vertex x-coordinate")
    _slider_k = Slider(start=-5, end=5, value=0, step=0.1, title="Vertex y-coordinate")
    _callback = CustomJS(
        args=dict(source=_source, sa=_slider_a, sh=_slider_h, sk=_slider_k),
        code="""
        var data = source.data;
        var a = sa.value;
        var h = sh.value;
        var k = sk.value;
        var x = data['x'];
        var y = data['y'];
        for (var i = 0; i < x.length; i++) {
            y[i] = a * (x[i] - h)**2 + k;
        }
        source.change.emit();
        """,
    )
    _slider_a.js_on_change("value", _callback)
    _slider_h.js_on_change("value", _callback)
    _slider_k.js_on_change("value", _callback)
    _layout = row(_fig, column(_slider_a, _slider_h, _slider_k))
    _layout
    return _layout


@app.cell
def _(ColumnDataSource, CustomJS, Slider, column, figure, np):
    _x = np.linspace(-5, 5, 1000)
    _source = ColumnDataSource(data=dict(x=_x, y=_x**2))
    _fig = figure(
        y_range=(-5, 5),
        x_range=(-5, 5),
        width=600,
        height=400,
        title="Quadratic Function",
    )
    _fig.line("x", "y", source=_source, line_width=2, color="green", line_alpha=0.7)
    _slider_a = Slider(start=-5, end=5, value=1, step=0.1, title="Quadratic Coefficient")
    _slider_h = Slider(start=-5, end=5, value=0, step=0.1, title="Vertex x-coordinate")
    _slider_k = Slider(start=-5, end=5, value=0, step=0.1, title="Vertex y-coordinate")
    _callback = CustomJS(
        args=dict(source=_source, sa=_slider_a, sh=_slider_h, sk=_slider_k),
        code="""
        var data = source.data;
        var a = sa.value;
        var h = sh.value;
        var k = sk.value;
        var x = data['x'];
        var y = data['y'];
        for (var i = 0; i < x.length; i++) {
            y[i] = a * (x[i] - h)**2 + k;
        }
        source.change.emit();
        """,
    )
    _slider_a.js_on_change("value", _callback)
    _slider_h.js_on_change("value", _callback)
    _slider_k.js_on_change("value", _callback)
    _layout = column(_slider_a, _slider_h, _slider_k, _fig)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_a` is 2, and `student_h` and `student_k` are 0. At `x = 0`, what is `a(x - h)**2 + k`?
    """)
    return


@app.cell
def _():
    student_a = 2
    student_h = 0
    student_k = 0
    student_x = 0
    print(student_a * (student_x - student_h) ** 2 + student_k)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**0.** With the vertex at the origin, the value at `x = 0` is `k`, which is 0.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Click the legend

    There are five body styles, and `Bokeh5` has five colors. Four cars have no price, so those points are not drawn. Click a legend entry to hide that body style. Click it again to show it.
    """)
    return


@app.cell
def _(auto_file, headers, pd):
    cars = pd.read_csv(auto_file, header=None, names=headers, na_values="?")
    print(cars.shape)
    print(cars.body_style.unique())
    print("missing price:", int(cars.price.isna().sum()))
    return (cars,)


@app.cell
def _(Bokeh5, cars, figure):
    _fig = figure(
        title="Click on legend entries to HIDE the corresponding points",
        x_axis_label="Highway (mpg)",
        y_axis_label="Price",
        height=400,
        width=700,
    )
    for _style, _color in zip(cars.body_style.unique(), Bokeh5):
        _rows = cars[cars.body_style == _style]
        _fig.scatter(
            _rows.highway_mpg,
            _rows.price,
            size=15,
            marker="circle_dot",
            color=_color,
            alpha=0.7,
            legend_label=_style,
        )
    _fig.legend.location = "top_right"
    _fig.legend.click_policy = "hide"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Mute keeps the points visible and draws them lighter. Hide removes them. This figure uses squares and `click_policy="mute"`.
    """)
    return


@app.cell
def _(Bokeh5, cars, figure):
    _fig = figure(
        title="Click on legend entries to MUTE the corresponding points",
        x_axis_label="Highway (mpg)",
        y_axis_label="Price",
        height=400,
        width=700,
    )
    for _style, _color in zip(cars.body_style.unique(), Bokeh5):
        _rows = cars[cars.body_style == _style]
        _fig.scatter(
            _rows.highway_mpg,
            _rows.price,
            size=10,
            marker="square_dot",
            color=_color,
            alpha=0.8,
            legend_label=_style,
        )
    _fig.legend.location = "top_right"
    _fig.legend.click_policy = "mute"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The size slider runs from 1 to 100 and starts at 30. `column` and `row` place that slider above, below, or to the right of its figure.
    - The color picker writes `fill_color`. The select menu writes `marker`, using star, square, plus, diamond, triangle, or circle.
    - The quadratic sample has 1,000 x values from -5 to 5. The static chart is `y = x**2`. The slider chart recomputes `y = a(x - h)**2 + k` in its own source. `a` starts at 1 and `h` and `k` start at 0.
    - The legend charts draw highway mpg against price for five body styles. `"hide"` removes a style. `"mute"` fades it. Four cars have no price, so they are absent from both charts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. Which glyph property does the size slider change?
    2. What does the color picker write into the glyph?
    3. Which marker names are in the select menu?
    4. What curve is drawn before you move `a`, `h`, or `k`?
    5. Why does the static quadratic stay put when the sliders move?
    6. What is the difference between `"hide"` and `"mute"`?
    7. Why are some cars missing from the body-style scatters?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **`size`.** `js_link` connects the slider's `value` to the glyph size.
2. **`fill_color`.** The picker's `color` is the new fill.
3. **Star, square, plus, diamond, triangle, and circle.** The menu starts on circle.
4. **`y = x**2`.** `a` is 1, and the vertex `(h, k)` is `(0, 0)`.
5. **It has its own data source.** The callback writes `y` only in the interactive chart.
6. **Hide removes the points. Mute fades them.** Both are `legend.click_policy` values.
7. **Four prices are missing.** A point with no price is not drawn.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Bokeh. *Documentation.* https://docs.bokeh.org/en/latest/
    - Bokeh. *Interaction.* https://docs.bokeh.org/en/latest/docs/user_guide/interaction.html
    - Bokeh. *Scatter glyph.* https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/scatter.html
    """)
    return


if __name__ == "__main__":
    app.run()
