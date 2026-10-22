# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "pandas",
#     "altair",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import altair as alt
    import marimo as mo
    import pandas as pd

    return alt, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction to Altair

    ## Objectives

    - Draw horsepower against highway mpg with the short-hand encoding and with `alt.X` and `alt.Y`.
    - Mark the points as points, circles, or squares, and stop the axes from starting at zero.
    - Size the points by cylinder count, after mapping the words to numbers.
    - Add color, shape, opacity, a tooltip, zoom, a title, and axis text.

    ## Background

    Altair builds a chart from a table and a set of encodings. A short-hand string such as `horsepower:Q` names the column and the type. `Q` means quantitative. The long-hand form is `alt.X("horsepower", type="quantitative")`.

    `mark_point` draws an open marker. `mark_circle` and `mark_square` draw filled shapes. `scale=alt.Scale(zero=False)` lets an axis start near the data instead of at zero.

    `Size` on a text column treats the words as an unordered set. Mapping `four` to 4, `six` to 6, and the other cylinder words to their numbers makes size a quantity.

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
    Short-hand and long-hand encodings name the same channels.

    | Short-hand | Long-hand |
    | --- | --- |
    | `x="varname"` | `alt.X("varname")` |
    | `x="varname:Q"` | `alt.X("varname", type="quantitative")` |
    | `x="sum(varname)"` | `alt.X("varname", aggregate="sum")` |
    | `x="sum(varname):Q"` | `alt.X("varname", aggregate="sum", type="quantitative")` |
    | `x="count():Q"` | `alt.X(aggregate="count", type="quantitative")` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scatter plots

    The short-hand chart leaves the type unset. Altair treats horsepower and highway mpg as quantities. Cars with a missing horsepower are not drawn.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            x="horsepower",
            y="highway_mpg",
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The long-hand chart uses `alt.X` and `alt.Y` with the same column names.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            alt.X("horsepower"),
            alt.Y("highway_mpg"),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `:Q` states the quantitative type in the short-hand string.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
        )
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_circle()
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
        )
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_square()
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The smallest horsepower in the file is 48, and the smallest highway mpg is 16. An axis that starts at zero leaves an empty region at the lower left. `zero=False` starts each axis near the data.
    """)
    return


@app.cell
def _(cars):
    print("Min horsepower:", cars.horsepower.min())
    print("Min highway_mpg:", cars.highway_mpg.min())
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Size and the cylinder words

    `num_cylinders` is stored as words. `Size` then has no numeric order. The next chart shows that legend.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
        )
    )
    _chart
    return _chart


@app.cell
def _(cars):
    print(cars.num_cylinders.unique())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The map builds a new table, `cars_sized`. The original `cars` table keeps the words.
    """)
    return


@app.cell
def _():
    num_cyl = {
        "four": 4,
        "six": 6,
        "five": 5,
        "eight": 8,
        "two": 2,
        "three": 3,
        "twelve": 12,
    }
    print(num_cyl)
    return (num_cyl,)


@app.cell
def _(cars, num_cyl):
    cars_sized = cars.assign(num_cylinders=cars.num_cylinders.map(num_cyl))
    print(cars_sized.num_cylinders.unique())
    return (cars_sized,)


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point()
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `filled=True` fills the markers. A larger marker is a larger cylinder count.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Color can use the same column as size, or a different column. The first chart colors by cylinder count. The second colors by fuel type.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
            alt.Color("num_cylinders"),
        )
    )
    _chart
    return _chart


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
            alt.Color("fuel_type"),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `Shape` uses engine location. `OpacityValue(0.5)` makes every marker half transparent.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
            alt.Color("fuel_type"),
            alt.Shape("engine_location"),
        )
    )
    _chart
    return _chart


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
            alt.Color("fuel_type"),
            alt.Shape("engine_location"),
            alt.OpacityValue(0.5),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The tooltip lists price and make. `.interactive()` turns on wheel zoom and drag. The axis limits follow the zoom.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            alt.Size("num_cylinders"),
            alt.Color("fuel_type"),
            alt.Shape("engine_location"),
            alt.OpacityValue(0.5),
            tooltip=[
                alt.Tooltip("price"),
                alt.Tooltip("make"),
            ],
        )
        .interactive()
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `properties` sets the width, the height, and the title. The title dictionary sets the text, the size, the weight, and the color.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False), title="Horsepower"),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False), title="Highway (mpg)"),
            alt.Size("num_cylinders", title="Number of cylinders"),
            alt.Color("fuel_type", title="Fuel type"),
            alt.Shape("engine_location", title="Engine location"),
            alt.OpacityValue(0.5),
            tooltip=[
                alt.Tooltip("price", title="Price"),
                alt.Tooltip("make", title="Make"),
            ],
        )
        .properties(
            width=500,
            height=350,
            title={
                "text": "Horsepower vs Highway MPG",
                "fontSize": 20,
                "fontWeight": "bold",
                "color": "grey",
            },
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `configure_axis` sets the axis title size, the title color, and the tick-label size. `grid=False` removes the grid lines.
    """)
    return


@app.cell
def _(alt, cars_sized):
    _chart = (
        alt.Chart(cars_sized)
        .mark_point(filled=True)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False), title="Horsepower"),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False), title="Highway (mpg)"),
            alt.Size("num_cylinders", title="Number of cylinders"),
            alt.Color("fuel_type", title="Fuel type"),
            alt.Shape("engine_location", title="Engine location"),
            alt.OpacityValue(0.5),
            tooltip=[
                alt.Tooltip("price", title="Price"),
                alt.Tooltip("make", title="Make"),
            ],
        )
        .properties(
            width=500,
            height=350,
            title={
                "text": "Horsepower vs Highway MPG",
                "fontSize": 20,
                "fontWeight": "bold",
                "color": "grey",
            },
        )
        .configure_axis(
            titleFontSize=16,
            titleColor="grey",
            labelFontSize=12,
            grid=False,
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_zero` is `False`, so the horsepower axis does not start at 0. The smallest horsepower in the file is 48. Does the axis need to include 0?
    """)
    return


@app.cell
def _(alt, cars):
    student_zero = False
    _chart = (
        alt.Chart(cars)
        .mark_point()
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=student_zero)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=student_zero)),
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**No.** The smallest horsepower is 48 and the smallest highway mpg is 16, so a zero baseline only adds empty space.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The short-hand string and `alt.X` / `alt.Y` encode the same columns. `:Q` marks a column as quantitative.
    - `mark_point`, `mark_circle`, and `mark_square` change the marker. The smallest horsepower is 48 and the smallest highway mpg is 16, so `zero=False` removes the empty corner.
    - Sizing by the cylinder words has no numeric order. `cars_sized` maps those words to 2, 3, 4, 5, 6, 8, and 12, and the original table is unchanged.
    - Color shows fuel type or cylinder count. Shape shows engine location. Opacity 0.5 fades every point. The tooltip shows price and make, and `.interactive()` zooms the axes.
    - The last chart sets the title, the axis titles, the legend titles, the axis font sizes, and turns the grid off.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does `:Q` mean in `horsepower:Q`?
    2. What is the smallest horsepower in the file?
    3. What does `alt.Scale(zero=False)` change?
    4. Why is the cylinder legend unordered before the map?
    5. What does `cars_sized` hold in `num_cylinders`?
    6. Which column does `Shape` use in the later charts?
    7. What does `.interactive()` add?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **Quantitative.** Altair treats the column as a number.
2. **48.** The smallest highway mpg is 16.
3. **The axis starts near the data.** It does not force a zero baseline.
4. **The values are words.** Size has no order for `four`, `six`, and the other labels until they become numbers.
5. **The numbers 2, 3, 4, 5, 6, 8, and 12.** The original `cars` table still has the words.
6. **`engine_location`.** Color in that chart is fuel type, and size is the cylinder count.
7. **Zoom and pan.** The axis limits follow the region you drag or scroll.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Altair. *Documentation.* https://altair-viz.github.io/
    - Altair. *Encodings.* https://altair-viz.github.io/user_guide/encodings/index.html
    """)
    return


if __name__ == "__main__":
    app.run()
