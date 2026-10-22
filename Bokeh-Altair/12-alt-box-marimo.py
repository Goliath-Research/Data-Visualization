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
    # Box Plots, Violins, Strips, and a Heatmap

    ## Objectives

    - Draw a box plot of price by body style, and set the box size, the title, the label angle, and the color.
    - Change `extent` so the whiskers reach 1.5, 1, or 0.5 times the interquartile range.
    - Draw a violin of price, then split it by fuel type into columns and into rows.
    - Draw strip plots of price by fuel type and by body style.
    - Draw a heatmap of make by body style, with a count in each cell.

    ## Background

    A box plot marks the median, the first and third quartiles, and the whiskers. `extent` is how many IQRs the whiskers reach past the quartiles. Points beyond `Q1 - extent * IQR` and `Q3 + extent * IQR` are drawn as circles. The default extent is 1.5. The argument name is `extent`.

    A violin is a density. `transform_density` estimates it. `stack="center"` places the density on both sides of a center line. Four cars have no price. The density charts use the 201 cars that have a price.

    A strip plot uses `mark_tick`, one tick per car. A heatmap uses `mark_rect`. The cell color is the count of that make and body style. Counts below 6 are labeled in black. Counts of 6 or more are labeled in white.

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
    priced = cars.dropna(subset=["price"]).copy()
    print(cars.shape)
    print("with price:", priced.shape[0])
    return cars, priced


@app.cell
def _(cars, mo):
    mo.Html(cars.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Box plots

    The first box plot is price by body style. `width` and `size` enlarge the chart and the boxes. The title, the axis titles, and `labelAngle=0` set the text. `configure_axis` sets the title size and the label size, and `grid=False` removes the grid. Color uses body style.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_boxplot(size=60)
        .encode(
            alt.X("body_style", title="Body style", axis=alt.Axis(labelAngle=0)),
            alt.Y("price", title="Car Price"),
            color=alt.Color("body_style", title="Body style"),
        )
        .properties(
            width=500,
            title={
                "text": "Box Plot: Car Price by Body style",
                "fontSize": 20,
                "color": "steelblue",
            },
        )
        .configure_axis(titleFontSize=16, labelFontSize=13, grid=False)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `extent=1.5` draws a circle for a price below Q1 - 1.5 IQR or above Q3 + 1.5 IQR. `extent=1` uses one IQR. `extent=0.5` uses half an IQR, so more prices fall outside the whiskers.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_boxplot(size=60, extent=1.5)
        .encode(
            alt.X("body_style", title="Body style", axis=alt.Axis(labelAngle=0)),
            alt.Y("price", title="Car Price"),
            color=alt.Color("body_style", title="Body style"),
        )
        .properties(
            width=500,
            title={
                "text": [
                    "Box Plot: Car Price by Body style",
                    "(circles represent outliers)",
                ],
                "fontSize": 20,
                "color": "steelblue",
            },
        )
        .configure_axis(titleFontSize=16, labelFontSize=13, grid=False)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_boxplot(size=60, extent=1)
        .encode(
            alt.X("body_style", title="Body style", axis=alt.Axis(labelAngle=0)),
            alt.Y("price", title="Price"),
            color=alt.Color("body_style", title="Body style"),
        )
        .properties(
            width=500,
            title={
                "text": ["Box Plot: Price by Body style", "(circles represent outliers)"],
                "fontSize": 20,
                "color": "steelblue",
            },
        )
        .configure_axis(titleFontSize=16, labelFontSize=13, grid=False)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_boxplot(size=60, extent=0.5)
        .encode(
            alt.X("body_style", title="Body style", axis=alt.Axis(labelAngle=0)),
            alt.Y("price", title="Price"),
            color=alt.Color("body_style", title="Body style"),
        )
        .properties(
            width=500,
            title={
                "text": ["Box Plot: Price by Body style", "(circles represent outliers)"],
                "fontSize": 20,
                "color": "steelblue",
            },
        )
        .configure_axis(titleFontSize=16, labelFontSize=13, grid=False)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_extent` is 0.5. Compared with 1.5, do more prices or fewer prices fall outside the whiskers?
    """)
    return


@app.cell
def _(alt, cars):
    student_extent = 0.5
    _chart = (
        alt.Chart(cars)
        .mark_boxplot(size=60, extent=student_extent)
        .encode(x="body_style", y="price")
        .properties(width=500, title=f"extent = {student_extent}")
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**More prices.** A smaller extent stops the whiskers closer to the quartiles, so more points are drawn as circles.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Violin plots

    These charts use the 201 cars with a price. `orient="horizontal"` lays the violin on its side. `groupby` makes one density per fuel type. `column` and `row` separate those violins. `impute=None` leaves gaps in the density axis instead of filling them.
    """)
    return


@app.cell
def _(alt, priced):
    _chart = (
        alt.Chart(priced)
        .transform_density("price", as_=["price", "density"])
        .mark_area(orient="horizontal")
        .encode(
            alt.Y("price:Q", title="Car Price"),
            alt.X("density:Q", stack="center"),
        )
        .configure_axis(titleFontSize=16, labelFontSize=13)
    )
    _chart
    return _chart


@app.cell
def _(alt, priced):
    _chart = (
        alt.Chart(priced)
        .transform_density("price", as_=["price", "density"], groupby=["fuel_type"])
        .mark_area(orient="horizontal")
        .encode(
            alt.Y("price:Q", title="Car Price"),
            alt.X("density:Q", stack="center"),
            alt.Color("fuel_type:N", title="Fuel type"),
            alt.Column("fuel_type"),
        )
        .configure_axis(titleFontSize=16, labelFontSize=13)
    )
    _chart
    return _chart


@app.cell
def _(alt, priced):
    _chart = (
        alt.Chart(priced)
        .transform_density("price", as_=["price", "density"], groupby=["fuel_type"])
        .mark_area(orient="horizontal")
        .encode(
            alt.Y("price:Q", title="Car Price"),
            alt.X("density:Q", stack="center", impute=None),
            alt.Color("fuel_type:N", title="Fuel type"),
            alt.Row("fuel_type"),
        )
        .configure_axis(titleFontSize=16, labelFontSize=13)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Strip plots

    Each tick is one car. The first strip groups by fuel type. The second groups by body style.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_tick()
        .encode(x="price:Q", y="fuel_type:N")
        .properties(title="Strip Plot of Price by Fuel type")
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_tick()
        .encode(x="price:Q", y="body_style:N")
        .properties(width=600, height=200, title="Strip Plot of Price by Body style")
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Heatmap

    Each rectangle is one make and one body style. The color is how many cars fall in that pair. The text is that count. A count below 6 is black. A count of 6 or more is white, so it stays readable on the darker reds. The second heatmap uses the `reds` scheme.
    """)
    return


@app.cell
def _(alt, cars):
    heat_base = (
        alt.Chart(cars)
        .transform_aggregate(num_records="count()", groupby=["make", "body_style"])
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("body_style:N", title="Body style"),
        )
        .properties(
            width=600,
            height=150,
            title={"text": "Make vs. Body Style", "fontSize": 20},
        )
    )
    heat_rect = heat_base.mark_rect().encode(
        color=alt.Color("num_records:Q", scale=alt.Scale(scheme="reds"))
    )
    heat_text = heat_base.mark_text(baseline="middle").encode(
        text="num_records:Q",
        color=alt.condition(
            alt.datum.num_records < 6,
            alt.value("black"),
            alt.value("white"),
        ),
    )
    _chart = heat_rect + heat_text
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The box plots show price by body style. `extent` sets the whisker reach: 1.5 IQR, 1 IQR, or 0.5 IQR. Prices beyond the whiskers are circles. Four cars have no price, so they do not enter the boxes.
    - The violins use the 201 cars with a price. One violin is the price density. Grouping by fuel type, then `column` or `row`, separates gas and diesel. `impute=None` leaves the density axis unfilled.
    - The strip plots put one tick per car, by fuel type and by body style.
    - The heatmap counts cars in each make and body style. Labels below 6 are black. Labels of 6 or more are white. The rectangle colors use the `reds` scheme.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does a box plot's whisker depend on?
    2. What does a smaller `extent` do to the number of circles?
    3. How many cars enter the violin?
    4. What does `orient="horizontal"` change?
    5. What is one tick in the strip plot?
    6. What does one heatmap rectangle count?
    7. When is the heatmap label white?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **`extent` times the IQR.** The whiskers stop at Q1 - extent * IQR and Q3 + extent * IQR.
2. **More circles.** The whiskers stop closer to the box, so more prices count as outside.
3. **201 cars.** Four of the 205 rows have no price.
4. **The violin lies on its side.** Price is on the vertical axis and density is on the horizontal axis.
5. **One car.** The tick's position is that car's price.
6. **Cars of that make and body style.** The color and the printed number are `num_records`.
7. **When the count is 6 or more.** Counts below 6 are black.
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
    - Altair. *Box plot.* https://altair-viz.github.io/gallery/boxplot.html
    - Altair. *Violin plot.* https://altair-viz.github.io/gallery/violin_plot.html
    """)
    return


if __name__ == "__main__":
    app.run()
