# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "numpy",
#     "bokeh",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import marimo as mo
    from bokeh.io import output_file, save
    from bokeh.plotting import figure

    return mo, np, output_file, save, figure


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction to Bokeh

    ## Objectives

    - Draw a line, then set the figure size and move the toolbar.
    - Add circles on the same figure, draw a step line, and draw three lines with color and dash.
    - Leave a gap in a line where an x value is missing.
    - Draw scatters with size, transparency, and marker shape, and style the legend and the title.
    - Save one figure as an HTML file.

    ## Background

    Bokeh draws glyphs on a figure. The figure is the chart this cell displays. A line joins the points in order. A step line moves horizontally, then vertically, between points. A scatter draws one marker at each point.

    The toolbar holds pan, zoom, and reset. `toolbar_location` can be `"left"`, `"right"`, `"above"`, `"below"`, or `None`.

    ## Datasets Used

    Three short arrays built in this lesson: `y`, `y2`, and `y3`, each paired with `x` from 1 to 10.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The points

    `x` is the horizontal position. `y` is the height of the first series.
    """)
    return


@app.cell
def _(np):
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    y = np.array([8, 4, 6, 3, 4, 3, 5, 4, 6, 5])
    print("x:", x)
    print("y:", y)
    return x, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A line

    `figure` creates the chart. `line` joins `x` and `y`. `line_width=2` sets the thickness.
    """)
    return


@app.cell
def _(figure, x, y):
    _fig = figure(title="Simple Line Graph", x_axis_label="x", y_axis_label="y")
    _fig.line(x, y, line_width=2)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Size and toolbar

    `width` and `height` set the figure size in pixels. This figure puts the toolbar on the left.
    """)
    return


@app.cell
def _(figure, x, y):
    _fig = figure(
        title="Simple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="left",
        height=400,
        width=600,
    )
    _fig.line(x, y, line_width=2)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This figure puts the toolbar above the chart. Each chart in this lesson is a new figure.
    """)
    return


@app.cell
def _(figure, x, y):
    _fig = figure(
        title="Simple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="above",
        height=400,
        width=600,
    )
    _fig.line(x, y, line_width=2)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Circles on the line

    `scatter` draws a circle at each point. `legend_label` names that glyph in the legend. `legend.location` places the legend.

    Legend locations include `top_left`, `top_center`, `top_right`, `bottom_left`, `bottom_center`, `bottom_right`, `center_left`, `center`, and `center_right`.
    """)
    return


@app.cell
def _(figure, x, y):
    _fig = figure(
        title="Simple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="above",
        height=400,
        width=600,
    )
    _fig.line(x, y, legend_label="line", line_width=2)
    _fig.scatter(
        x,
        y,
        legend_label="circle",
        fill_color="darkorange",
        line_color="white",
        size=10,
    )
    _fig.legend.location = "top_center"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_location` is `"bottom_left"`. Where does the legend sit?
    """)
    return


@app.cell
def _(figure, x, y):
    student_location = "bottom_left"
    _fig = figure(
        title="Simple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="above",
        height=400,
        width=600,
    )
    _fig.line(x, y, legend_label="line", line_width=2)
    _fig.scatter(
        x,
        y,
        legend_label="circle",
        fill_color="darkorange",
        line_color="white",
        size=10,
    )
    _fig.legend.location = student_location
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Bottom left.** `legend.location` uses the string you assign. `"bottom_left"` sits in the lower left of the plot.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A step line

    `step` draws a staircase between the same points. The circles mark the data values.
    """)
    return


@app.cell
def _(figure, x, y):
    _fig = figure(
        title="Step Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="above",
        height=400,
        width=600,
    )
    _fig.step(x, y, legend_label="line", line_width=2)
    _fig.scatter(
        x,
        y,
        legend_label="circle",
        fill_color="darkorange",
        line_color="white",
        size=12,
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Three lines

    `y2` and `y3` are two more series on the same `x`. `line_dash` can be `"dashed"` or `"dotted"`. `line_color` sets the color. `legend.title` names the legend box.
    """)
    return


@app.cell
def _(np):
    y2 = np.array([2, 3, 4, 3, 2, 1, 3, 4, 2, 3])
    y3 = np.array([4, 5, 5, 4, 3, 4, 2, 2, 4, 2])
    print("y2:", y2)
    print("y3:", y3)
    return y2, y3


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.line(x, y, line_width=2, legend_label="Line 1")
    _fig.line(
        x,
        y2,
        line_width=2,
        legend_label="Line 2",
        line_dash="dashed",
        line_color="red",
    )
    _fig.line(
        x,
        y3,
        line_width=2,
        legend_label="Line 3",
        line_dash="dotted",
        line_color="green",
    )
    _fig.legend.title = "Lines"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A gap where x is missing

    The third and seventh positions of `x` (indexes 2 and 6) are set to `NaN`. A line stops at a missing x and starts again at the next number.
    """)
    return


@app.cell
def _(np, x):
    x1 = np.array(x, dtype=float)
    x1[[2, 6]] = np.nan
    print(x1)
    return (x1,)


@app.cell
def _(figure, x1, y, y2, y3):
    _fig = figure(
        title="Multiple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.line(x1, y, line_width=2, legend_label="Line 1")
    _fig.line(
        x1,
        y2,
        line_width=2,
        legend_label="Line 2",
        line_dash="dashed",
        line_color="red",
    )
    _fig.line(
        x1,
        y3,
        line_width=2,
        legend_label="Line 3",
        line_dash="dotted",
        line_color="green",
    )
    _fig.legend.title = "Lines"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scatters

    Three scatters share one figure. `size` is the marker width in pixels. The legend title is `Circles`.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Circle Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(x, y, legend_label="Circle 1", size=10)
    _fig.scatter(x, y2, legend_label="Circle 2", fill_color="red", size=20)
    _fig.scatter(x, y3, legend_label="Circle 3", fill_color="grey", size=30)
    _fig.legend.title = "Circles"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `fill_alpha` is the fill transparency, from 0 (invisible) to 1 (solid). `line_color` is the marker outline.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Circle Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Circle 1",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Circle 2",
        fill_color="red",
        fill_alpha=0.2,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Circle 3",
        fill_color="grey",
        fill_alpha=0.3,
        line_color="white",
        size=30,
    )
    _fig.legend.title = "Circles"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The default legend sits at the top right. This figure moves it to the top left.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Circle Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Circle 1",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Circle 2",
        fill_color="red",
        fill_alpha=0.2,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Circle 3",
        fill_color="grey",
        fill_alpha=0.3,
        line_color="white",
        size=30,
    )
    _fig.legend.title = "Circles"
    _fig.legend.location = "top_left"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The legend text can change font, style, and color. This legend is bold Arial, in black, at the top center.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Circle Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Circle 1",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Circle 2",
        fill_color="red",
        fill_alpha=0.2,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Circle 3",
        fill_color="grey",
        fill_alpha=0.3,
        line_color="white",
        size=30,
    )
    _fig.legend.title = "Circles"
    _fig.legend.location = "top_center"
    _fig.legend.label_text_font = "arial"
    _fig.legend.label_text_font_style = "bold"
    _fig.legend.label_text_color = "black"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `border_line_width`, `border_line_color`, and `border_line_alpha` style the legend box. `background_fill_color` and `background_fill_alpha` style the fill behind the labels.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Circle Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Circle 1",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Circle 2",
        fill_color="red",
        fill_alpha=0.2,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Circle 3",
        fill_color="grey",
        fill_alpha=0.3,
        line_color="white",
        size=30,
    )
    _fig.legend.title = "Circles"
    _fig.legend.location = "top_center"
    _fig.legend.label_text_font = "arial"
    _fig.legend.label_text_font_style = "bold"
    _fig.legend.label_text_color = "black"
    _fig.legend.border_line_width = 2
    _fig.legend.border_line_color = "black"
    _fig.legend.border_line_alpha = 0.3
    _fig.legend.background_fill_color = "silver"
    _fig.legend.background_fill_alpha = 0.3
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `title.text` is the title string. `text_font_size`, `align`, `background_fill_color`, and `text_color` style it.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="New Multiple Circles Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Circle 1",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Circle 2",
        fill_color="red",
        fill_alpha=0.2,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Circle 3",
        fill_color="grey",
        fill_alpha=0.3,
        line_color="white",
        size=30,
    )
    _fig.legend.title = "Circles"
    _fig.legend.location = "top_center"
    _fig.legend.label_text_font = "arial"
    _fig.legend.label_text_font_style = "bold"
    _fig.legend.label_text_color = "black"
    _fig.legend.border_line_width = 2
    _fig.legend.border_line_color = "black"
    _fig.legend.border_line_alpha = 0.3
    _fig.legend.background_fill_color = "silver"
    _fig.legend.background_fill_alpha = 0.3
    _fig.title.text_font_size = "20px"
    _fig.title.align = "center"
    _fig.title.background_fill_color = "lightgrey"
    _fig.title.text_color = "black"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Squares

    `marker="square"` changes the shape. The sizes and the alpha values stay with each series.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Multiple Square Graph",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        legend_label="Square 1",
        marker="square",
        fill_alpha=0.3,
        size=10,
    )
    _fig.scatter(
        x,
        y2,
        legend_label="Square 2",
        marker="square",
        fill_color="red",
        fill_alpha=0.2,
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        legend_label="Square 3",
        marker="square",
        fill_color="grey",
        fill_alpha=0.5,
        size=30,
    )
    _fig.legend.title = "Squares"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other markers

    `marker` chooses the shape. Names include `asterisk`, `circle`, `cross`, `diamond`, `diamond_cross`, `hex_dot`, `plus`, `square`, `square_x`, `star_dot`, and `triangle_pin`. The list is on the Bokeh scatter page: https://docs.bokeh.org/en/latest/docs/user_guide/basic/scatters.html

    The first chart uses `diamond_cross`, `hex_dot`, and `square_x`. The legend names match those markers.
    """)
    return


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Scatterplot",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        marker="diamond_cross",
        legend_label="Diamond cross",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=30,
    )
    _fig.scatter(
        x,
        y2,
        marker="hex_dot",
        legend_label="Hex dot",
        fill_color="red",
        fill_alpha=0.4,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y3,
        marker="square_x",
        legend_label="Square",
        fill_color="grey",
        fill_alpha=0.7,
        line_color="white",
        size=20,
    )
    _fig.legend.title = "Markers"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell
def _(figure, x, y, y2, y3):
    _fig = figure(
        title="Scatterplot",
        x_axis_label="x",
        y_axis_label="y",
        height=400,
        width=600,
    )
    _fig.scatter(
        x,
        y,
        marker="plus",
        legend_label="Plus",
        fill_color="navy",
        fill_alpha=0.5,
        line_color="white",
        size=20,
    )
    _fig.scatter(
        x,
        y2,
        marker="star_dot",
        legend_label="Star",
        fill_color="red",
        fill_alpha=0.6,
        line_color="white",
        size=30,
    )
    _fig.scatter(
        x,
        y3,
        marker="triangle_pin",
        legend_label="Triangle",
        fill_color="grey",
        fill_alpha=0.7,
        line_color="white",
        size=25,
    )
    _fig.legend.title = "Markers"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Save an HTML file

    `output_file` names the file. `save` writes the line-and-circles figure into `Simple Line.html` in this folder. When the lesson runs on your computer, open that file in a browser to see the chart by itself.
    """)
    return


@app.cell
def _(figure, output_file, save, x, y):
    _fig = figure(
        title="Simple Line Graph",
        x_axis_label="x",
        y_axis_label="y",
        toolbar_location="above",
        height=400,
        width=600,
    )
    _fig.line(x, y, legend_label="line", line_width=2)
    _fig.scatter(
        x,
        y,
        legend_label="circle",
        fill_color="darkorange",
        line_color="white",
        size=10,
    )
    _fig.legend.location = "top_center"
    output_file(filename="Simple Line.html", title="Simple Line HTML file")
    print(save(_fig))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - `figure` plus `line` draws the series `y` against `x`. `toolbar_location`, `width`, and `height` set the toolbar and the size.
    - `scatter` adds circles. `step` draws a staircase. Three `line` calls on one figure use color, dash, and a legend title to keep the series apart.
    - A `NaN` in `x` breaks the line. The line continues after the next numeric x.
    - Scatter size, `fill_alpha`, and `marker` change the points. The legend location, font, border, and background, and the title text and size, are properties of the figure.
    - `save` writes `Simple Line.html` for the line-and-circles figure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does `toolbar_location="above"` change?
    2. Which two glyphs are on the chart titled Simple Line Graph that has a legend?
    3. How does `step` move from one point to the next?
    4. What happens to the three lines when `x1` has missing values at indexes 2 and 6?
    5. On the circle chart, which series has the largest markers?
    6. What does `fill_alpha=0.2` do to a marker?
    7. What file does `save` write?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **The toolbar sits above the chart.** The line itself is unchanged.
2. **A line and circles.** `line` joins the points. `scatter` draws a dark-orange circle at each point.
3. **A staircase.** The line moves across, then up or down, instead of taking the straight diagonal.
4. **Each line breaks.** Bokeh skips the missing x and starts the segment again at the next number.
5. **Circle 3.** Its `size` is 30. Circle 1 is 10 and Circle 2 is 20.
6. **A faint fill.** 0.2 is close to invisible. 1 would be a solid fill.
7. **`Simple Line.html`.** It holds the line-and-circles figure.
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
    - Bokeh. *Scatter markers.* https://docs.bokeh.org/en/latest/docs/user_guide/basic/scatters.html
    - Bokeh. *Scatter glyph.* https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/scatter.html
    """)
    return


if __name__ == "__main__":
    app.run()
