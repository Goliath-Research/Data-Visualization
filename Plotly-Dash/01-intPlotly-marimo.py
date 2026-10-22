# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "pandas",
#     "plotly",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import plotly.express as px

    return mo, pd, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction to Plotly

    ## Objectives

    - Build a line and a bar from two short lists, and see that a figure has data, a layout, and frames.
    - Read the Automobile file, drop rows that still have a missing value, and count cars by risk symbol.
    - Draw symboling by make as a bar chart, and use color and `barmode` to separate fuel type.
    - Use a histogram for a count, an average, a maximum, or a minimum, and add bins, a pattern, and a marginal plot.

    ## Background

    Plotly Express builds a figure from a table or from two lists. The figure is what this cell displays. It has three parts: the data (the traces), the layout (title, size, and axes), and the frames (used later for animation). This lesson has no animation, so the frames are empty.

    A bar chart of several rows adds the y values that share the same x value. A histogram can count rows, or it can summarize another column with `histfunc`.

    ## Datasets Used

    - Two short lists, `x` and `y`, built in this lesson.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A line from two lists

    `x` holds the horizontal positions. `y` holds the heights. `px.line` joins those points in order.
    """)
    return


@app.cell
def _():
    x = [1, 2, 3, 4, 5]
    y = [4, 5, 3, 2, 6]
    print("x:", x)
    print("y:", y)
    return x, y


@app.cell
def _(px, x, y):
    line_fig = px.line(x=x, y=y, width=800)
    line_fig
    return line_fig


@app.cell
def _(line_fig):
    _title = line_fig.layout.title.text
    print(f"traces: {len(line_fig.data)}")
    print("title:", _title if _title else "(none)")
    print(f"frames: {len(line_fig.frames)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cell above prints three facts about that figure. There is one trace, the line. The title is empty because the call did not set one. There are no frames.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    Change `student_y`, then run the cell. Does the line end higher than it starts?
    """)
    return


@app.cell
def _(px):
    student_y = [1, 3, 2, 5, 4]
    _fig = px.line(x=[1, 2, 3, 4, 5], y=student_y, width=800, title="Your line")
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**It ends higher.** The first height is 1 and the last height is 4.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A bar from the same lists

    `px.bar` draws one bar for each pair. `color=x` paints each bar from its horizontal value. `width` sets the figure width in pixels.
    """)
    return


@app.cell
def _(px, x, y):
    _fig = px.bar(x=x, y=y, color=x, width=800, title="Five bars")
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Automobile file

    The file has 205 cars and 26 columns. `na_values="?"` turns each `?` into a missing value. The table is wide, so it is shown as HTML.
    """)
    return


@app.cell
def _(auto_file, headers, pd):
    cars_raw = pd.read_csv(auto_file, header=None, names=headers, na_values="?")
    print(cars_raw.shape)
    return (cars_raw,)


@app.cell
def _(cars_raw, mo):
    mo.Html(cars_raw.head(3).to_html())
    return


@app.cell
def _(cars_raw):
    print(cars_raw.isnull().sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Several columns have missing values. `normalized_losses` has the most, 41. A row can have more than one missing value, so the counts above are not a count of rows.

    `dropna` drops every row that still has a missing value. The charts below use `cars`, the 159 complete rows.
    """)
    return


@app.cell
def _(cars_raw):
    cars = cars_raw.dropna()
    print(cars.shape)
    print("missing values left:", int(cars.isnull().sum().sum()))
    return (cars,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bars of the risk symbol

    `symboling` is the insurance risk symbol. A higher number is a riskier car. `value_counts(sort=False)` counts the cars at each symbol and keeps the symbols in their original order.
    """)
    return


@app.cell
def _(cars):
    symbol_counts = cars.symboling.value_counts(sort=False)
    print(symbol_counts)
    return (symbol_counts,)


@app.cell
def _(px, symbol_counts):
    _fig = px.bar(
        x=symbol_counts.index,
        y=symbol_counts.values,
        width=800,
        title="Cars at each risk symbol",
    )
    _fig
    return _fig


@app.cell
def _(px, symbol_counts):
    _fig = px.bar(
        x=symbol_counts.index,
        y=symbol_counts.values,
        color=symbol_counts.values,
        width=800,
        title="Risk symbol (from safe to risky)",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next chart uses the car table directly. Several cars share a make, so `px.bar` **adds** the symboling values of that make. The bar is a sum, not a count and not an average.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="symboling",
        width=800,
        title="Sum of risk symbol by make",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="symboling",
        color="symboling",
        width=800,
        title="Sum of risk symbol by make",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="symboling",
        color="fuel_type",
        width=800,
        title="Sum of risk symbol by make and fuel type",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `color="fuel_type"`, each make is split into gas and diesel. The default places those pieces in one stack. `barmode="group"` places them side by side.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="symboling",
        color="fuel_type",
        barmode="group",
        width=800,
        title="Sum of risk symbol by make and fuel type",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The chart colors the bars by body style. What does one color stand for?
    """)
    return


@app.cell
def _(cars, px):
    color_column = "body_style"
    _fig = px.bar(
        cars,
        x="make",
        y="symboling",
        color=color_column,
        barmode="group",
        width=800,
        title="Sum of risk symbol by make and body style",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**A body style.** Each color is one value of `body_style`, such as sedan or hatchback. The height is still the sum of `symboling`.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Histograms

    `px.histogram` groups the x values. With no `y` and no `histfunc`, the height of a bar is the number of rows in that group.

    To get the **average** symboling of each make, pass `y="symboling"` and `histfunc="avg"`.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="make",
        y="symboling",
        color="fuel_type",
        barmode="group",
        histfunc="avg",
        width=800,
        title="Average risk symbol by make and fuel type",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Without `barmode="group"`, the fuel types are stacked. The stack is the sum of the two averages, which is not itself an average. The grouped chart is the one that compares the two averages.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="make",
        y="symboling",
        color="fuel_type",
        histfunc="avg",
        width=800,
        title="Stacked averages of risk symbol",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="make",
        y="price",
        histfunc="avg",
        width=800,
        title="Average price by make",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        barmode="group",
        histfunc="avg",
        width=800,
        title="Average price by make and fuel type",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A histogram of one numeric column counts cars in ranges of that column. `nbins` sets how many bars to aim for. More bars means a narrower range in each bar.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(cars, x="length", width=800, title="Car length")
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(cars, x="length", nbins=10, width=800, title="Car length, 10 bins")
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="length",
        nbins=10,
        color="body_style",
        width=800,
        title="Car length and body style",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="length",
        nbins=10,
        color="body_style",
        pattern_shape="fuel_type",
        width=800,
        title="Car length, body style, and fuel type",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    This length histogram asks for 5 bins. Do the bars get wider or narrower than in the 10-bin chart?
    """)
    return


@app.cell
def _(cars, px):
    length_bins = 5
    _fig = px.histogram(
        cars,
        x="length",
        nbins=length_bins,
        width=800,
        title=f"Car length, {length_bins} bins",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Wider.** Fewer bins means each bar covers a longer span of `length`.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Price and horsepower

    With only `x="price"`, the vertical axis is the number of cars. `text_auto=True` writes that count on the bar.

    `histnorm="probability density"` rescales the heights so that the area of the bars is 1. The shape of the distribution is the same.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(cars, x="price", width=800, title="Price, counts")
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="price",
        text_auto=True,
        width=800,
        title="Price, counts labeled",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="price",
        histnorm="probability density",
        width=800,
        title="Price, probability density",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="price",
        histnorm="probability density",
        color_discrete_sequence=["salmon"],
        width=800,
        title="Price, probability density",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="horsepower",
        color_discrete_sequence=["seagreen"],
        width=800,
        title="Horsepower",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="horsepower",
        color_discrete_sequence=["seagreen"],
        opacity=0.7,
        width=800,
        title="Horsepower, opacity 0.7",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `opacity` below 1 makes the bars partly transparent.

    The next three charts put `price` on the vertical axis and change `histfunc`. The horizontal axis is still horsepower, in bins. The height is the average price in that bin, then the maximum price, then the minimum price.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="horsepower",
        y="price",
        histfunc="avg",
        color_discrete_sequence=["olivedrab"],
        opacity=0.7,
        width=800,
        title="Average price by horsepower bin",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="horsepower",
        y="price",
        histfunc="max",
        color_discrete_sequence=["olivedrab"],
        width=800,
        title="Maximum price by horsepower bin",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="horsepower",
        y="price",
        histfunc="min",
        color_discrete_sequence=["olivedrab"],
        opacity=0.3,
        width=800,
        title="Minimum price by horsepower bin",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A marginal plot

    `color="drive_wheels"` splits city fuel economy by drive wheels. `marginal` adds a small plot of the same rows above the histogram: a rug, a box, or a violin.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="city_mpg",
        nbins=30,
        color="drive_wheels",
        width=800,
        title="City MPG by drive wheels",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="city_mpg",
        nbins=30,
        color="drive_wheels",
        marginal="rug",
        width=800,
        title="City MPG by drive wheels, with a rug",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="city_mpg",
        nbins=30,
        color="drive_wheels",
        marginal="box",
        width=800,
        title="City MPG by drive wheels, with a box",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="city_mpg",
        nbins=30,
        color="drive_wheels",
        marginal="violin",
        width=800,
        title="City MPG by drive wheels, with a violin",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - A Plotly figure has data, a layout, and frames. This lesson's figures have traces and a layout, and no frames.
    - The Automobile file has 205 rows. Dropping rows with a missing value leaves 159 complete rows. The charts use those 159.
    - `px.bar` on a table adds the y values that share an x value. `color` splits or paints the bars. `barmode="group"` places the colored pieces side by side. The default stacks them.
    - `px.histogram` counts rows when no summary column is given. `histfunc` can be `"avg"`, `"max"`, or `"min"`. `nbins` changes the bar width. `histnorm="probability density"` rescales the heights so the area is 1. `marginal` adds a rug, a box, or a violin of the same rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What are the three parts of a Plotly figure?
    2. How many Automobile rows remain after `dropna`?
    3. On the bar chart of symboling by make, what does the height of a bar mean?
    4. What does `barmode="group"` change when the bars are colored by fuel type?
    5. What does `histfunc="avg"` put on the vertical axis?
    6. What happens to the length bars when `nbins` goes from 10 to 5?
    7. What does `marginal="box"` add to the city-MPG histogram?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **Data, layout, and frames:** The data holds the traces. The layout holds the title, the size, and the axes. The frames hold animation steps. These charts have no frames.
2. **159 rows:** The file starts with 205 rows. 46 rows have a missing value and are dropped.
3. **A sum:** Every car of that make adds its `symboling` into the bar. The height is not a count of cars.
4. **Side by side:** Gas and diesel each get their own bar. Without `barmode="group"`, those pieces are stacked.
5. **The average of y:** The bar height is the mean of the y column inside that x group.
6. **The bars get wider:** Five bins cover the same length range with fewer, wider bars.
7. **A box plot of the same rows:** It sits above the histogram and uses the same `drive_wheels` colors.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Plotly Express in Python.* https://plotly.com/python/plotly-express/
    - Plotly. *Bar charts in Python.* https://plotly.com/python/bar-charts/
    - Plotly. *Histograms in Python.* https://plotly.com/python/histograms/
    """)
    return


if __name__ == "__main__":
    app.run()
