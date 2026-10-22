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
    # Linking Charts with a Brush

    ## Objectives

    - Brush horsepower against highway mpg, and limit that brush to x or to y.
    - Filter a make bar chart from the scatter brush, side by side and one above the other.
    - Link two, then three, price scatters with one brush.
    - Cross-filter histograms of length, width, and height.
    - Brush the sunspot months after 1980, and use an overview chart to set the date range.

    ## Background

    A brush is an interval selection. Points inside keep their body-style color. Points outside turn grey. The same brush can filter another chart with `transform_filter`.

    Charts that share a brush are built in the same cell, on one selection. A chart in another cell has its own selection, so the two do not move together.

    Sunspots are darker regions on the Sun's photosphere. They occur in pairs of opposite magnetic polarity. The published series follows an approximately 11-year cycle. The charts show the monthly number after 1980. They do not estimate the cycle length.

    ## Datasets Used

    - **Automobile Dataset** from the UCI Machine Learning Repository.
    - **Monthly mean total sunspot number**, from SIDC at the Royal Observatory of Belgium. The file is `Sunspots.csv`.
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
    ## A brush on one scatter

    Drag a rectangle. Points inside keep the body-style color. The second chart's brush uses only x, so the selected band is vertical. The third uses only y, so the band is horizontal.
    """)
    return


@app.cell
def _(alt, cars):
    _brush = alt.selection_interval()
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
            color=alt.condition(_brush, "body_style:N", alt.value("grey")),
        )
        .add_params(_brush)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    brush_x = alt.selection_interval(encodings=["x"])
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
            color=alt.condition(brush_x, "body_style:N", alt.value("grey")),
        )
        .add_params(brush_x)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    brush_y = alt.selection_interval(encodings=["y"])
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x="horsepower:Q",
            y="highway_mpg:Q",
            color=alt.condition(brush_y, "body_style:N", alt.value("grey")),
        )
        .add_params(brush_y)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The brush filters a bar chart

    The bars count makes inside the brush, colored by body style. `|` places the scatter and the bars side by side. The next cell builds the same pair one above the other, with its own brush.
    """)
    return


@app.cell
def _(alt, cars):
    _brush = alt.selection_interval()
    _points = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            color=alt.condition(_brush, "body_style:N", alt.value("grey")),
        )
        .properties(
            width=350,
            height=300,
            title={"text": "Horsepower vs. Highway (mpg)", "fontSize": 16},
        )
        .add_params(_brush)
    )
    _bars = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", axis=alt.Axis(title="Make")),
            alt.Y("count()", axis=alt.Axis(title="Count")),
            alt.Color("body_style"),
        )
        .properties(
            width=350,
            height=300,
            title={"text": "Count of body style by Make", "fontSize": 16},
        )
        .transform_filter(_brush)
    )
    _chart = _points | _bars
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _brush = alt.selection_interval()
    _points = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            alt.X("horsepower", scale=alt.Scale(zero=False)),
            alt.Y("highway_mpg", scale=alt.Scale(zero=False)),
            color=alt.condition(_brush, "body_style:N", alt.value("grey")),
        )
        .properties(
            width=350,
            height=300,
            title={"text": "Horsepower vs. Highway (mpg)", "fontSize": 16},
        )
        .add_params(_brush)
    )
    _bars = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", axis=alt.Axis(title="Make")),
            alt.Y("count()", axis=alt.Axis(title="Count")),
            alt.Color("body_style"),
        )
        .properties(
            width=350,
            height=300,
            title={"text": "Count of body style by Make", "fontSize": 16},
        )
        .transform_filter(_brush)
    )
    _chart = _points & _bars
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Linked price scatters

    The shared encoding is price on y and body style as the color. Highway mpg and city mpg use the domain 10 to 55. The three-chart row adds horsepower. A brush on any of them highlights the same cars on the others. Four cars have no price, so they are not drawn.
    """)
    return


@app.cell
def _(alt, cars):
    _brush = alt.selection_interval()
    _base = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            alt.Y("price"),
            color=alt.condition(_brush, "body_style:N", alt.value("gray")),
        )
        .properties(width=230, height=250)
        .add_params(_brush)
    )
    _highway = _base.encode(
        alt.X("highway_mpg", scale=alt.Scale(domain=[10, 55]))
    ).properties(title={"text": "Car Price vs. Highway (mpg)", "fontSize": 16})
    _city = _base.encode(
        alt.X("city_mpg", scale=alt.Scale(domain=[10, 55]))
    ).properties(title={"text": "Car Price vs. City (mpg)", "fontSize": 16})
    _chart = _highway | _city
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _brush = alt.selection_interval()
    _base = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            alt.Y("price"),
            color=alt.condition(_brush, "body_style:N", alt.value("gray")),
        )
        .properties(width=230, height=250)
        .add_params(_brush)
    )
    _highway = _base.encode(
        alt.X("highway_mpg", scale=alt.Scale(domain=[10, 55]))
    ).properties(title={"text": "Car Price vs. Highway (mpg)", "fontSize": 16})
    _city = _base.encode(
        alt.X("city_mpg", scale=alt.Scale(domain=[10, 55]))
    ).properties(title={"text": "Car Price vs. City (mpg)", "fontSize": 16})
    _horsepower = _base.encode(alt.X("horsepower")).properties(
        title={"text": "Car Price vs. Horsepower", "fontSize": 16}
    )
    _chart = _highway | _city | _horsepower
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Cross-filter histograms

    Each panel is a histogram of one dimension, with at most 20 bins. The grey bars are all cars. The blue bars are the cars inside the brush. The brush is on x, and it is shared across the three panels. This brush belongs to these histograms only.
    """)
    return


@app.cell
def _(alt, cars):
    hist_brush = alt.selection_interval(encodings=["x"])
    base_hist = (
        alt.Chart()
        .mark_bar()
        .encode(
            x=alt.X(alt.repeat("column"), type="quantitative", bin=alt.Bin(maxbins=20)),
            y="count()",
        )
        .properties(width=250, height=250)
    )
    background = base_hist.encode(color=alt.value("lightgrey")).add_params(hist_brush)
    highlight = base_hist.transform_filter(hist_brush)
    _chart = alt.layer(background, highlight, data=cars).repeat(
        column=["length", "width", "height"]
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sunspots after 1980

    The file's first column is a row number. The value column is renamed `Sunspots`. Year, month, and day come from the date. The charts keep months with `Year > 1980`.
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
    recent = sunspots[sunspots.Year > 1980]
    print(sunspots.shape)
    print("after 1980:", recent.shape[0])
    return recent, sunspots


@app.cell
def _(mo, sunspots):
    mo.Html(sunspots.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The gold bars are the mean sunspot number by date. A brush on the date axis fades the bars outside it. The brown rule is the mean of the brushed months. The black rules are the minimum and the maximum of those same months. This brush is separate from the automobile brushes.
    """)
    return


@app.cell
def _(alt, recent):
    sun_brush = alt.selection_interval(encodings=["x"])
    sun_bars = (
        alt.Chart()
        .mark_bar(color="gold")
        .encode(
            alt.X("Date:T"),
            alt.Y("mean(Sunspots):Q"),
            opacity=alt.condition(
                sun_brush,
                alt.OpacityValue(1),
                alt.OpacityValue(0.3),
            ),
        )
        .properties(
            width=900,
            height=400,
            title={"text": "Sunspots by Year"},
        )
        .add_params(sun_brush)
    )
    line_mean = (
        alt.Chart()
        .mark_rule(color="brown")
        .encode(y="mean(Sunspots):Q", size=alt.SizeValue(3))
        .transform_filter(sun_brush)
    )
    line_min = (
        alt.Chart()
        .mark_rule(color="black")
        .encode(y="min(Sunspots):Q", size=alt.SizeValue(1))
        .transform_filter(sun_brush)
    )
    line_max = (
        alt.Chart()
        .mark_rule(color="black")
        .encode(y="max(Sunspots):Q", size=alt.SizeValue(1))
        .transform_filter(sun_brush)
    )
    _chart = alt.layer(sun_bars, line_min, line_mean, line_max, data=recent)
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Overview

    The lower area is 60 pixels tall and holds the brush. The upper area's x domain is that brush, so dragging the overview sets the dates in the detail chart.
    """)
    return


@app.cell
def _(alt, recent):
    overview_brush = alt.selection_interval(encodings=["x"])
    _base = (
        alt.Chart(recent)
        .mark_area(color="gold")
        .encode(alt.X("Date:T"), alt.Y("Sunspots:Q"))
        .properties(width=900, height=350)
    )
    upper = _base.encode(alt.X("Date:T", scale=alt.Scale(domain=overview_brush))).properties(
        title={"text": "Sunspots"}
    )
    lower = _base.properties(height=60).add_params(overview_brush)
    _chart = upper & lower
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The cross-filter uses `encodings=["x"]`. If you brush the length histogram, which axis is shared with width and height?
    """)
    return


@app.cell
def _():
    student_encodings = ["x"]
    print(student_encodings)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**The horizontal axis.** Each panel brushes its own x values. Length, width, and height do not share a numeric scale. The selection is the set of cars inside the length brush, and those cars are highlighted in the other panels.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - A brush on horsepower against highway mpg keeps the body-style color inside the rectangle. `encodings=["x"]` selects a vertical band. `encodings=["y"]` selects a horizontal band.
    - That brush filters the make bars. `|` places the scatter beside the bars. `&` places the bars underneath. Each pair has its own brush.
    - The price scatters share one brush. Highway and city mpg use the domain 10 to 55. The third chart adds horsepower. Four cars have no price, so they are not drawn.
    - The cross-filter draws length, width, and height. Grey is every car. The highlight is the cars inside the x brush.
    - After 1980, the sunspot brush sets the gold bars' opacity and the brown mean rule, plus the black minimum and maximum. The overview brush sets the date domain of the upper area. That brush is not the automobile brush.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What color are the points outside a brush?
    2. What does `encodings=["y"]` select?
    3. What do the make bars count?
    4. Which x domains are fixed on the price scatters?
    5. In the cross-filter, what do the grey bars show?
    6. Which months enter the sunspot charts?
    7. What does the lower sunspot area control?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **Grey.** Points inside keep the body-style color.
2. **A horizontal band.** The full width is included. Only the y range is tested.
3. **Cars inside the scatter brush.** The bars are makes, colored by body style.
4. **Highway and city mpg, from 10 to 55.** Horsepower keeps Altair's own domain.
5. **Every car.** The colored bars on top are the cars inside the brush.
6. **Months with year greater than 1980.** The full file starts in 1749.
7. **The dates shown in the upper area.** Its brush is the upper chart's x domain.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Altair. *Interactive charts.* https://altair-viz.github.io/user_guide/interactions.html
    - Vega-Lite. *Aggregate operations.* https://vega.github.io/vega-lite/docs/aggregate.html
    - Wikipedia. *Sunspot.* https://en.wikipedia.org/wiki/Sunspot
    - SIDC, Royal Observatory of Belgium. *Sunspot Number.* https://www.sidc.be/SILSO/home
    """)
    return


if __name__ == "__main__":
    app.run()
