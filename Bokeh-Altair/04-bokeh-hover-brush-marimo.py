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
    from bokeh.layouts import column, gridplot, row
    from bokeh.models import BoxAnnotation, ColumnDataSource, HoverTool
    from bokeh.plotting import figure
    from bokeh.transform import cumsum

    return (
        BoxAnnotation,
        ColumnDataSource,
        HoverTool,
        column,
        cumsum,
        figure,
        gridplot,
        mo,
        np,
        pd,
        pi,
        row,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Hover and Linked Brushing

    ## Objectives

    - Show x and y in a hover on a six-point line.
    - Show the fruit name and the count in a hover on a pie.
    - Draw the monthly sunspot number, then add a hover for the month, day, year, and the value.
    - Shade sunspot counts below 100 and above 300.
    - Link three automobile scatters with one data source, and arrange that trio as a row, a column, and several grids.

    ## Background

    A hover is a tooltip. The text uses column names from the data, such as `@x` and `@y`.

    Linked brushing needs one `ColumnDataSource` shared by every scatter in the layout, and one layout around those scatters. A box select or a lasso select on any scatter highlights the same rows in the others. Each layout below builds its own source and its own three figures.

    Sunspots are darker regions on the Sun's photosphere. They occur in pairs of opposite magnetic polarity. The published series follows an approximately 11-year cycle. The charts below show the monthly number. They do not estimate the cycle length.

    ## Datasets Used

    - A six-point line, and a four-fruit pie, both built in this lesson.
    - **Monthly mean total sunspot number**, from SIDC at the Royal Observatory of Belgium. The file is `Sunspots.csv`.
    - **Automobile Dataset** from the UCI Machine Learning Repository. The scatters use price, highway mpg, city mpg, and horsepower.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the files are read from

    Pandas can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website, and it can read `Sunspots.csv` from this folder.
    - **Inside a web browser.** This lesson can run inside a web page. The browser only lets a page download files from websites that allow it. This security rule is called **CORS**. The UCI website does not allow it, so the browser blocks that download.

    This lesson reads GitHub copies of both files. GitHub allows a browser page to read its files, so the copies work in both places. The UCI address and the local sunspot file name are kept in comments.
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
    sun_file = (
        "https://raw.githubusercontent.com/Goliath-Research/"
        "Data-Visualization/main/Bokeh-Altair/Sunspots.csv"
    )
    # Local file in this folder: Sunspots.csv
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
    return auto_file, headers, sun_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hover on a line

    The tooltip `(@x,@y)` reads the coordinates of the point under the pointer. The line joins the points. The circles are the hover targets.
    """)
    return


@app.cell
def _(HoverTool, figure):
    x1 = [1, 2, 3, 4, 5, 6]
    y1 = [3, 4, 2, 3, 6, 5]
    _fig = figure(
        title="Hover over Points",
        x_axis_label="x",
        y_axis_label="y",
        y_range=(0, 7),
        tools=[HoverTool()],
        tooltips="(@x,@y)",
        width=600,
        height=400,
    )
    _fig.line(x1, y1, line_width=2)
    _fig.scatter(x1, y1, marker="circle", size=15, line_color="white")
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hover on a pie

    The counts are Guava 2, Mango 4, Orange 5, and Lime 3. The angle is each count's share of the total, times `2 * pi`. The tooltip shows the fruit and the count.
    """)
    return


@app.cell
def _(ColumnDataSource, HoverTool, cumsum, figure, np, pi):
    fruits = ["Guava", "Mango", "Orange", "Lime"]
    fruit_counts = [2, 4, 5, 3]
    _source = ColumnDataSource(
        data=dict(
            fruits=fruits,
            counts=fruit_counts,
            angles=[count / np.sum(fruit_counts) * 2 * pi for count in fruit_counts],
            colors=["lightcoral", "gold", "darkorange", "limegreen"],
        )
    )
    _fig = figure(
        tools=[HoverTool()],
        tooltips="(@fruits,@counts)",
        width=500,
        height=500,
    )
    _fig.axis.visible = False
    _fig.grid.grid_line_color = None
    _fig.wedge(
        x=2,
        y=0,
        radius=0.8,
        start_angle=cumsum("angles", include_zero=True),
        end_angle=cumsum("angles"),
        line_color="white",
        fill_color="colors",
        legend_field="fruits",
        source=_source,
    )
    _fig.legend.orientation = "horizontal"
    _fig.legend.location = "top"
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sunspots

    The file's first column is a row number, so `index_col=0` skips it. The value column is renamed `Sunspots`. `Date` becomes a datetime, and Year, Month, and Day are taken from it. The series runs from January 1749 through January 2021.
    """)
    return


@app.cell
def _(pd, sun_file):
    sunspots = pd.read_csv(sun_file, index_col=0)
    sunspots = sunspots.rename(
        columns={"Monthly Mean Total Sunspot Number": "Sunspots"}
    )
    sunspots = sunspots.assign(Date=pd.to_datetime(sunspots.Date))
    sunspots = sunspots.assign(
        Year=sunspots.Date.dt.year,
        Month=sunspots.Date.dt.month,
        Day=sunspots.Date.dt.day,
    )
    print(sunspots.shape)
    return (sunspots,)


@app.cell
def _(mo, sunspots):
    mo.Html(sunspots.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first line uses the date on the x axis, so the months stay in time order.
    """)
    return


@app.cell
def _(figure, sunspots):
    _fig = figure(
        title="Sunspots",
        x_axis_label="Date",
        y_axis_label="Sunspots",
        height=400,
        width=900,
    )
    _fig.line(x=sunspots.Date, y=sunspots.Sunspots, line_width=2)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hover on the sunspot line

    The hover source stores the year as `x`, the sunspot number as `y`, and the month and day as `m` and `d`. The tooltip prints `month-day-year` and the sunspot number with one decimal. The line uses `x` and `y` from that source. Months of the same year share one x position.
    """)
    return


@app.cell
def _(ColumnDataSource, figure, sunspots):
    sun_source = ColumnDataSource(
        data=dict(
            x=sunspots.Year,
            y=sunspots.Sunspots,
            m=sunspots.Month,
            d=sunspots.Day,
        )
    )
    _tooltips = [
        ("    Date = ", "@m-@d-@x"),
        ("Sunspots = ", "@y{0.0}"),
    ]
    _fig = figure(
        title="Sunspots",
        x_axis_label="Date",
        y_axis_label="Sunspots",
        tooltips=_tooltips,
        height=400,
        width=900,
    )
    _fig.line(x="x", y="y", line_width=2, source=sun_source)
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bands at 100 and 300

    The green band covers sunspot numbers below 100. The coral band covers numbers above 300. The hover line is drawn again on this figure, with the same tooltip.
    """)
    return


@app.cell
def _(BoxAnnotation, ColumnDataSource, figure, sunspots):
    _source = ColumnDataSource(
        data=dict(
            x=sunspots.Year,
            y=sunspots.Sunspots,
            m=sunspots.Month,
            d=sunspots.Day,
        )
    )
    _fig = figure(
        title="Sunspots",
        x_axis_label="Date",
        y_axis_label="Sunspots",
        tooltips=[
            ("    Date = ", "@m-@d-@x"),
            ("Sunspots = ", "@y{0.0}"),
        ],
        height=400,
        width=900,
    )
    _fig.line(x="x", y="y", line_width=2, source=_source)
    _fig.add_layout(BoxAnnotation(top=100, fill_alpha=0.2, fill_color="palegreen"))
    _fig.add_layout(BoxAnnotation(bottom=300, fill_alpha=0.2, fill_color="lightcoral"))
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linked automobile scatters

    Four cars have no price, so those rows are not drawn. The y axis runs from 0 to 50,000. The tools are box select, lasso select, reset, and help.

    Select points on any scatter. The same rows highlight on the other two, because the three scatters read one source.
    """)
    return


@app.cell
def _(auto_file, headers, mo, pd):
    cars = pd.read_csv(auto_file, header=None, names=headers, na_values="?")
    print(cars.shape)
    print("missing price:", int(cars.price.isna().sum()))
    mo.Html(cars.head().to_html())
    return (cars,)


@app.cell
def _(ColumnDataSource, cars, figure):
    def price_trio():
        source = ColumnDataSource(
            data=dict(
                Price=cars.price,
                Hmpg=cars.highway_mpg,
                Cmpg=cars.city_mpg,
                Hpower=cars.horsepower,
            )
        )
        tools = "box_select, lasso_select, reset, help"
        highway = figure(
            tools=tools,
            y_range=[0, 50000],
            title="Car Price vs. Highway (mpg)",
        )
        highway.scatter("Hmpg", "Price", source=source, color="orangered", size=8)
        city = figure(
            tools=tools,
            y_range=[0, 50000],
            title="Car Price vs. City (mpg)",
        )
        city.scatter("Cmpg", "Price", source=source, color="orange", size=8)
        power = figure(
            tools=tools,
            y_range=[0, 50000],
            title="Car Price vs. Horsepower",
        )
        power.scatter("Hpower", "Price", source=source, color="steelblue", size=8)
        return highway, city, power

    return (price_trio,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### One row of three

    `gridplot` places the three figures in a single row. Drag a box on one chart and the matching cars highlight on the other two.
    """)
    return


@app.cell
def _(gridplot, price_trio):
    _highway, _city, _power = price_trio()
    _layout = gridplot([[_highway, _city, _power]], width=300, height=300)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The `row` layout

    `row` places the same three charts side by side. This cell builds a new trio, so the selection is local to this layout.
    """)
    return


@app.cell
def _(price_trio, row):
    _highway, _city, _power = price_trio()
    _layout = row(_highway, _city, _power)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Two on the first row

    Highway and city sit on the first row. Horsepower sits alone on the second row.
    """)
    return


@app.cell
def _(gridplot, price_trio):
    _highway, _city, _power = price_trio()
    _layout = gridplot([[_highway, _city], [_power]], width=350, height=300)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### An empty slot

    `None` leaves the bottom-left cell empty, so horsepower sits under the city chart.
    """)
    return


@app.cell
def _(gridplot, price_trio):
    _highway, _city, _power = price_trio()
    _layout = gridplot([[_highway, _city], [None, _power]], width=350, height=300)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A column of three

    `gridplot` can stack the three charts. `column` does the same stacking with the layout object.
    """)
    return


@app.cell
def _(gridplot, price_trio):
    _highway, _city, _power = price_trio()
    _layout = gridplot([[_highway], [_city], [_power]], width=350, height=200)
    _layout
    return _layout


@app.cell
def _(column, price_trio):
    _highway, _city, _power = price_trio()
    _layout = column(_highway, _city, _power)
    _layout
    return _layout


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The fruit counts are Guava 2, Mango 4, Orange 5, and Lime 3. Which fruit is the largest slice?
    """)
    return


@app.cell
def _():
    student_counts = {"Guava": 2, "Mango": 4, "Orange": 5, "Lime": 3}
    print(max(student_counts, key=student_counts.get))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Orange.** Its count is 5, the largest of 2, 4, 5, and 3.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The six-point hover prints `(@x,@y)`. The fruit hover prints the name and the count. Orange is the largest slice, with 5 of the 14 pieces.
    - The sunspot file has 3,265 months, from January 1749 through January 2021. The first line uses the date. The hover line uses the year as x and shows month-day-year plus the sunspot number.
    - The green band is sunspot numbers below 100. The coral band is numbers above 300.
    - The three price scatters share one source inside each layout. A box select or a lasso select highlights the same cars on the other charts. Four cars have no price, so they are not drawn. `row`, `column`, and `gridplot` only change where the three charts sit. `None` leaves a grid cell empty.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does the line tooltip `(@x,@y)` show?
    2. Which fruit has the largest count?
    3. What does the sunspot tooltip show?
    4. Why do months of one year share an x position on the hover chart?
    5. Which sunspot numbers fall in the green band?
    6. Why do the three price scatters highlight together?
    7. What does `None` do in a `gridplot`?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **The point's coordinates.** `@x` and `@y` are the data columns under the pointer.
2. **Orange.** The counts are Guava 2, Mango 4, Orange 5, and Lime 3.
3. **Month, day, year, and the sunspot number.** The format is `@m-@d-@x`, and `@y{0.0}` prints one decimal.
4. **The x column is the year.** All twelve months of a year have the same year number.
5. **Numbers below 100.** The coral band starts at 300.
6. **They share one ColumnDataSource.** A selection is a set of rows in that source, so every glyph that reads it highlights those rows.
7. **It leaves that cell empty.** The horsepower chart sits under the city chart.
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
    - Bokeh. *Layouts.* https://docs.bokeh.org/en/latest/docs/reference/layouts.html
    - Wikipedia. *Sunspot.* https://en.wikipedia.org/wiki/Sunspot
    - SIDC, Royal Observatory of Belgium. *Sunspot Number.* https://www.sidc.be/SILSO/home
    """)
    return


if __name__ == "__main__":
    app.run()
