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
    from math import pi

    import marimo as mo
    import numpy as np
    import pandas as pd
    from bokeh.models import BoxAnnotation, ColumnDataSource
    from bokeh.palettes import Bokeh
    from bokeh.plotting import figure
    from bokeh.transform import cumsum

    return (
        Bokeh,
        BoxAnnotation,
        ColumnDataSource,
        cumsum,
        figure,
        mo,
        np,
        pd,
        pi,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Histograms and Pie Charts with Bokeh

    ## Objectives

    - Read the Automobile file and count length, width, and height with `numpy.histogram`.
    - Draw each histogram with the `quad` glyph, and wrap that drawing in a function that returns the figure.
    - Overlay the three histograms, then mark each mean at the height of that histogram's tallest bin.
    - Shade count bands at 20 and at 40.
    - Draw a pie of body style with `wedge`, using the angle of each slice.

    ## Background

    Bokeh has no histogram glyph. `numpy.histogram` returns the counts and the bin edges. A `quad` is one rectangle: `bottom`, `top`, `left`, and `right`. For a histogram, the bottom is 0, the top is the count, and the left and right are neighboring edges.

    A pie uses `wedge`. Each slice needs a start angle and an end angle. The angles are the cumulative share of the circle. `cumsum` on the angle column builds those running totals.

    These charts use every car. Length, width, height, and body style have no missing values.

    ## Datasets Used

    - **Automobile Dataset** from the UCI Machine Learning Repository. The file has no header row. Missing entries are written as `?`.
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
    return auto_file, headers


@app.cell
def _(auto_file, headers, pd):
    cars = pd.read_csv(auto_file, header=None, names=headers, na_values="?")
    print(cars.shape)
    return (cars,)


@app.cell
def _(cars, mo):
    mo.Html(cars.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A histogram of length

    Ten bins cover the range from the shortest car to the longest. There is one more edge than there are counts, because each count sits between two edges.
    """)
    return


@app.cell
def _(cars, np):
    length_counts, length_edges = np.histogram(
        cars.length,
        bins=10,
        range=[cars.length.min(), cars.length.max()],
    )
    print("counts:", len(length_counts), length_counts)
    print("edges:", len(length_edges))
    return length_counts, length_edges


@app.cell
def _(figure, length_counts, length_edges):
    _fig = figure(height=400, width=600, title="Histogram of Car length")
    _fig.quad(
        bottom=0,
        top=length_counts,
        left=length_edges[:-1],
        right=length_edges[1:],
        fill_color="salmon",
        line_color="white",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A function that returns the figure

    `create_hist` counts the values, builds a figure, draws the quads, and returns the figure. `bins` is the number of bars.
    """)
    return


@app.cell
def _(figure, np):
    def create_hist(values, bins=10):
        counts, edges = np.histogram(
            values,
            bins=bins,
            range=[np.min(values), np.max(values)],
        )
        hist = figure(height=400, width=600, title="Histogram")
        hist.quad(
            bottom=0,
            top=counts,
            left=edges[:-1],
            right=edges[1:],
            fill_color="salmon",
            line_color="white",
        )
        return hist

    return (create_hist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Length, 10 bins and 5 bins
    """)
    return


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.length, 10)
    return _fig


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.length, 5)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    This chart asks for 5 bins of length. Do the bars get wider or narrower than in the 10-bin chart?
    """)
    return


@app.cell
def _(cars, create_hist):
    student_bins = 5
    _fig = create_hist(cars.length, student_bins)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Wider.** Fewer bins cover the same length range, so each bar is wider.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Width, 10 bins and 5 bins
    """)
    return


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.width, 10)
    return _fig


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.width, 5)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Height, 10 bins and 5 bins
    """)
    return


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.height, 10)
    return _fig


@app.cell
def _(cars, create_hist):
    _fig = create_hist(cars.height, 5)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Three histograms on one figure

    Each variable keeps its own edges, because length, width, and height live on different scales. The quads overlap. Length is indian red, width is dark orange, and height is dodger blue. Alpha lets the bars show through each other.
    """)
    return


@app.cell
def _(cars, np):
    bins = 10
    length_top, length_bin_edges = np.histogram(
        cars.length,
        bins=bins,
        range=[cars.length.min(), cars.length.max()],
    )
    width_top, width_bin_edges = np.histogram(
        cars.width,
        bins=bins,
        range=[cars.width.min(), cars.width.max()],
    )
    height_top, height_bin_edges = np.histogram(
        cars.height,
        bins=bins,
        range=[cars.height.min(), cars.height.max()],
    )
    print("length max count:", length_top.max())
    print("width max count:", width_top.max())
    print("height max count:", height_top.max())
    return (
        height_bin_edges,
        height_top,
        length_bin_edges,
        length_top,
        width_bin_edges,
        width_top,
    )


@app.cell
def _(
    figure,
    height_bin_edges,
    height_top,
    length_bin_edges,
    length_top,
    width_bin_edges,
    width_top,
):
    _fig = figure(
        height=400,
        width=600,
        toolbar_location="above",
        title="Histograms",
    )
    _fig.quad(
        bottom=0,
        top=length_top,
        left=length_bin_edges[:-1],
        right=length_bin_edges[1:],
        legend_label="length",
        fill_color="indianred",
        fill_alpha=0.8,
        line_color="salmon",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=width_top,
        left=width_bin_edges[:-1],
        right=width_bin_edges[1:],
        legend_label="width",
        fill_color="darkorange",
        fill_alpha=0.8,
        line_color="darkorange",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=height_top,
        left=height_bin_edges[:-1],
        right=height_bin_edges[1:],
        legend_label="height",
        fill_color="dodgerblue",
        fill_alpha=0.8,
        line_color="lightblue",
        line_alpha=0.8,
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Means and the tallest bins

    The x positions are the means, in the column order height, width, length. The y positions are the tallest bin of each histogram, in that same order. The line visits those three points. It is a marker on this chart, not a histogram by itself.
    """)
    return


@app.cell
def _(cars, height_top, length_top, width_top):
    dimension_means = cars[["height", "width", "length"]].mean()
    tallest = [height_top.max(), width_top.max(), length_top.max()]
    print(dimension_means)
    print("tallest bins:", tallest)
    return dimension_means, tallest


@app.cell
def _(
    dimension_means,
    figure,
    height_bin_edges,
    height_top,
    length_bin_edges,
    length_top,
    tallest,
    width_bin_edges,
    width_top,
):
    _fig = figure(
        height=400,
        width=600,
        toolbar_location="above",
        title="Histograms",
    )
    _fig.quad(
        bottom=0,
        top=length_top,
        left=length_bin_edges[:-1],
        right=length_bin_edges[1:],
        legend_label="length",
        fill_color="indianred",
        fill_alpha=0.8,
        line_color="salmon",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=width_top,
        left=width_bin_edges[:-1],
        right=width_bin_edges[1:],
        legend_label="width",
        fill_color="darkorange",
        fill_alpha=0.8,
        line_color="darkorange",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=height_top,
        left=height_bin_edges[:-1],
        right=height_bin_edges[1:],
        legend_label="height",
        fill_color="dodgerblue",
        fill_alpha=0.8,
        line_color="lightblue",
        line_alpha=0.8,
    )
    _fig.line(x=dimension_means, y=tallest, color="grey", line_width=2)
    _fig.scatter(x=dimension_means, y=tallest, marker="circle", fill_color="grey", size=10)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Count bands

    A `BoxAnnotation` paints a horizontal band. With no left or right, the band crosses the whole x axis. The bands split the count axis: below 20, from 20 to 40, and above 40.
    """)
    return


@app.cell
def _(
    BoxAnnotation,
    dimension_means,
    figure,
    height_bin_edges,
    height_top,
    length_bin_edges,
    length_top,
    tallest,
    width_bin_edges,
    width_top,
):
    _fig = figure(
        height=400,
        width=600,
        toolbar_location="above",
        title="Histograms",
    )
    _fig.quad(
        bottom=0,
        top=length_top,
        left=length_bin_edges[:-1],
        right=length_bin_edges[1:],
        legend_label="length",
        fill_color="indianred",
        fill_alpha=0.8,
        line_color="salmon",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=width_top,
        left=width_bin_edges[:-1],
        right=width_bin_edges[1:],
        legend_label="width",
        fill_color="darkorange",
        fill_alpha=0.8,
        line_color="darkorange",
        line_alpha=0.8,
    )
    _fig.quad(
        bottom=0,
        top=height_top,
        left=height_bin_edges[:-1],
        right=height_bin_edges[1:],
        legend_label="height",
        fill_color="dodgerblue",
        fill_alpha=0.8,
        line_color="lightblue",
        line_alpha=0.8,
    )
    _fig.line(x=dimension_means, y=tallest, color="grey", line_width=2)
    _fig.scatter(x=dimension_means, y=tallest, marker="circle", fill_color="grey", size=10)
    _fig.add_layout(BoxAnnotation(top=20, fill_alpha=0.2, fill_color="powderblue"))
    _fig.add_layout(BoxAnnotation(bottom=20, top=40, fill_alpha=0.2, fill_color="beige"))
    _fig.add_layout(BoxAnnotation(bottom=40, fill_alpha=0.2, fill_color="powderblue"))
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A pie of body style

    `value_counts` gives the number of cars in each body style. The angle of a slice is that count divided by the total, times a full circle (`2 * pi`). `Bokeh[5]` supplies one color per slice, because there are five body styles.

    `cumsum('angles', include_zero=True)` is the start of each slice. `cumsum('angles')` is the end. The legend lists the body styles.
    """)
    return


@app.cell
def _(cars):
    body_counts = cars.body_style.value_counts()
    print(body_counts)
    return (body_counts,)


@app.cell
def _(Bokeh, body_counts, pd, pi):
    body_slices = pd.DataFrame(
        {
            "body_style": body_counts.index,
            "number_cars": body_counts.values,
        }
    )
    body_slices = body_slices.assign(
        angles=body_slices.number_cars / body_slices.number_cars.sum() * 2 * pi,
        colors=Bokeh[body_slices.shape[0]],
    )
    print(body_slices)
    return (body_slices,)


@app.cell
def _(ColumnDataSource, body_slices, cumsum, figure):
    _source = ColumnDataSource(data=body_slices)
    _fig = figure(width=600, height=600, x_range=_source.data["body_style"])
    _fig.axis.visible = False
    _fig.grid.grid_line_color = None
    _fig.wedge(
        x=body_slices.shape[0] / 2,
        y=0,
        radius=2,
        start_angle=cumsum("angles", include_zero=True),
        end_angle=cumsum("angles"),
        line_color="white",
        fill_color="colors",
        legend_field="body_style",
        source=_source,
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This pie uses the same slices. The legend is horizontal and sits at the top.
    """)
    return


@app.cell
def _(ColumnDataSource, body_slices, cumsum, figure):
    _source = ColumnDataSource(data=body_slices)
    _fig = figure(width=600, height=600, x_range=_source.data["body_style"])
    _fig.axis.visible = False
    _fig.grid.grid_line_color = None
    _fig.wedge(
        x=body_slices.shape[0] / 2,
        y=0,
        radius=2,
        start_angle=cumsum("angles", include_zero=True),
        end_angle=cumsum("angles"),
        line_color="white",
        fill_color="colors",
        legend_field="body_style",
        source=_source,
    )
    _fig.legend.orientation = "horizontal"
    _fig.legend.location = "top"
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The Automobile file has 205 rows. Length, width, and height are complete, so these charts use all 205 cars.
    - `numpy.histogram` returns the counts and one extra edge. `quad` draws one bar between each pair of edges. `create_hist` returns that figure. Five bins make wider bars than ten bins.
    - The overlay keeps a separate set of edges for each dimension. The grey line passes through (mean of height, tallest height bin), then width, then length.
    - The bands mark counts below 20, from 20 to 40, and above 40.
    - The pie angles are each body style's share of 205 cars. Sedan is the largest slice (96), then hatchback (70), wagon (25), hardtop (8), and convertible (6).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. Why is the histogram built from `quad`?
    2. How many edges does a 10-bin histogram have?
    3. What does `create_hist` return?
    4. What changes when length uses 5 bins instead of 10?
    5. In the overlay, which order does the grey line visit?
    6. What counts do the powder-blue and beige bands cover?
    7. How is a pie slice's angle computed?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **Bokeh has no histogram glyph.** `quad` is a rectangle, so it can draw one bin.
2. **11 edges.** Ten counts need eleven boundaries.
3. **The figure.** The function counts the values, draws the quads, and returns the chart.
4. **The bars get wider.** Five bins cover the same length range.
5. **Height, then width, then length.** Those are the column order of the means, and the tallest bins follow that order.
6. **Below 20, and from 20 to 40.** The beige band is 20 to 40. Powder blue covers below 20 and above 40.
7. **Its share of the circle.** Count divided by the total, times `2 * pi`.
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
    - Bokeh. *Quad glyph.* https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/quad.html
    - Bokeh. *Wedge glyph.* https://docs.bokeh.org/en/latest/docs/reference/models/glyphs/wedge.html
    """)
    return


if __name__ == "__main__":
    app.run()
