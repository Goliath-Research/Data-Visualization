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
    # Hierarchical Graphs

    ## Objectives

    - Draw the same Automobile hierarchy as a sunburst, a treemap, and an icicle chart.
    - See how the order of `path` changes which category is on the inside.
    - Size the sectors by a sum, using `values`, and color them by a number or by a category.
    - Check a tooltip against the table: a count, a sum of price, and a weighted average of tip.

    ## Background

    A hierarchy is a set of nested groups. Body style contains fuel type, and fuel type contains the make of the car. Sunburst, treemap, and icicle charts draw that nesting.

    - A sunburst uses rings. The first name in `path` is the center.
    - A treemap uses nested rectangles.
    - An icicle chart uses rectangles in a row, from the root out to the leaves.

    With no `values`, the size of a sector is the number of rows. With `values="price"`, the size is the sum of price. Click a sector to zoom in. The path bar at the corner zooms back out.

    ## Datasets Used

    - **Automobile Dataset** from the UCI Machine Learning Repository. The charts use the 159 complete rows.
    - **Tips**, a table built into Plotly Express. Each row is one restaurant bill. It is used for the color examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the Automobile file is read from

    Pandas can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website.
    - **Inside a web browser.** This lesson can run inside a web page. The browser only lets a page download files from websites that allow it. This security rule is called **CORS**. The UCI website does not allow it, so the browser blocks that download.

    This lesson reads a copy of the Automobile file stored on GitHub. GitHub allows a browser page to read its files, so the copy works in both places. The original UCI address is kept in a comment. The tips table is part of Plotly Express, so it does not need a download.
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
    cars_raw = pd.read_csv(auto_file, header=None, names=headers, na_values="?")
    print(cars_raw.shape)
    return (cars_raw,)


@app.cell
def _(cars_raw):
    print(cars_raw.isnull().sum())
    return


@app.cell
def _(cars_raw):
    cars = cars_raw.dropna()
    print(cars.shape)
    return (cars,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sunburst

    `path=["body_style", "fuel_type"]` puts body style in the center and fuel type in the outer ring. The tooltip of a sector shows the label, the count of rows, the parent, and an id such as `sedan/gas`.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.sunburst(
        cars,
        path=["body_style", "fuel_type"],
        width=600,
        height=600,
        title="Body style, then fuel type",
    )
    _fig
    return _fig


@app.cell
def _(cars):
    sedan_gas = cars[(cars.body_style == "sedan") & (cars.fuel_type == "gas")]
    print(sedan_gas.shape[0])
    return (sedan_gas,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That count is 67, the same count as the `sedan/gas` sector.

    Reversing `path` moves fuel type to the center.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.sunburst(
        cars,
        path=["fuel_type", "body_style"],
        width=600,
        height=600,
        title="Fuel type, then body style",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The first name in `path` is the center ring. What is the center of this chart?
    """)
    return


@app.cell
def _(cars, px):
    inner_ring = "make"
    _fig = px.sunburst(
        cars,
        path=[inner_ring, "body_style"],
        width=600,
        height=600,
        title="Make, then body style",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Make.** `path` starts with `make`, so each make is a wedge of the center ring. Body style is the outer ring.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Size by price

    `values="price"` sizes each sector by the sum of price, not by the number of cars. The `sedan/gas` tooltip shows that sum.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.sunburst(
        cars,
        path=["body_style", "fuel_type"],
        values="price",
        width=600,
        height=600,
        title="Sized by the sum of price",
    )
    _fig
    return _fig


@app.cell
def _(sedan_gas):
    print(sedan_gas.price.sum())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sum is 813499. That is the price shown on the `sedan/gas` sector.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Color

    The tips table has 244 bills. `values="total_bill"` sizes the sector by the sum of the bills. `color="tip"` colors it. The color of a sector is not the plain average of tip. It is the average of tip weighted by `total_bill`.
    """)
    return


@app.cell
def _(px):
    tips = px.data.tips()
    print(tips.shape)
    return (tips,)


@app.cell
def _(mo, tips):
    mo.Html(tips.head(3).to_html())
    return


@app.cell
def _(px, tips):
    _fig = px.sunburst(
        tips,
        path=["day", "time"],
        values="total_bill",
        width=600,
        height=600,
        title="Day, then time",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.sunburst(
        tips,
        path=["day", "time"],
        values="total_bill",
        color="tip",
        color_continuous_scale="RdBu",
        width=600,
        height=600,
        title="Colored by tip",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.sunburst(
        tips,
        path=["day", "time"],
        values="total_bill",
        color="tip",
        color_continuous_scale="RdBu",
        hover_data={"tip": ":.2f"},
        width=600,
        height=600,
        title="Tip formatted to two decimals",
    )
    _fig
    return _fig


@app.cell
def _(tips):
    sat_dinner = tips[(tips.day == "Sat") & (tips.time == "Dinner")].copy()
    print(sat_dinner.shape[0])
    print(round(sat_dinner.total_bill.sum(), 1))
    return (sat_dinner,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Saturday dinner has 87 bills, and the bills sum to 1778.4. That sum is the `total_bill` on the `Sat/Dinner` sector.

    The tooltip's tip is the weighted average. Multiply each tip by its bill, add those products, and divide by the sum of the bills.
    """)
    return


@app.cell
def _(sat_dinner):
    sat_weighted = sat_dinner.assign(
        bill_times_tip=sat_dinner.total_bill * sat_dinner.tip
    )
    weighted_tip = sat_weighted.bill_times_tip.sum() / sat_weighted.total_bill.sum()
    print(f"{weighted_tip:.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The weighted tip is 3.52, the value on the `Sat/Dinner` tooltip.

    A text column can be the color too. `color_discrete_map` assigns a color to each sex.
    """)
    return


@app.cell
def _(px, tips):
    _fig = px.sunburst(
        tips,
        path=["sex", "time", "day"],
        values="total_bill",
        color="sex",
        width=600,
        height=600,
        title="Colored by sex",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.sunburst(
        tips,
        path=["sex", "time", "day"],
        values="total_bill",
        color="sex",
        color_discrete_map={"Male": "dimgrey", "Female": "coral"},
        width=600,
        height=600,
        title="Named colors for sex",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Treemap

    The same `path` and `values` work for a treemap. Rectangles replace the rings. The first name in `path` is the outer rectangle.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.treemap(
        cars,
        path=["body_style", "fuel_type"],
        width=800,
        height=500,
        title="Body style, then fuel type",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.treemap(
        cars,
        path=["fuel_type", "body_style"],
        width=800,
        height=500,
        title="Fuel type, then body style",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.treemap(
        cars,
        path=["body_style", "fuel_type"],
        values="price",
        width=800,
        height=500,
        title="Sized by the sum of price",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.treemap(
        cars,
        path=["body_style", "fuel_type", "make"],
        values="price",
        width=800,
        height=500,
        title="Body style, fuel type, and make",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.treemap(
        tips,
        path=["day", "time"],
        values="total_bill",
        color="tip",
        color_continuous_scale="RdBu",
        hover_data={"tip": ":.2f"},
        width=800,
        height=500,
        title="Colored by the weighted tip",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.treemap(
        tips,
        path=["sex", "time", "day"],
        values="total_bill",
        color="time",
        width=800,
        height=500,
        title="Colored by time of day",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Icicle

    An icicle chart uses the same columns. The sectors cascade from the root toward the leaves. `px.Constant("Cars")` adds one root block named Cars, so every body style sits under that single label.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.icicle(
        cars,
        path=["body_style", "fuel_type"],
        width=800,
        height=500,
        title="Body style, then fuel type",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.icicle(
        cars,
        path=["fuel_type", "body_style"],
        width=800,
        height=500,
        title="Fuel type, then body style",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.icicle(
        cars,
        path=["body_style", "fuel_type"],
        values="price",
        width=800,
        height=500,
        title="Sized by the sum of price",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.icicle(
        cars,
        path=[px.Constant("Cars"), "body_style", "fuel_type", "make"],
        values="price",
        width=600,
        height=700,
        title="One root named Cars",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.icicle(
        tips,
        path=["day", "time"],
        values="total_bill",
        color="tip",
        color_continuous_scale="RdBu",
        hover_data={"tip": ":.2f"},
        width=800,
        height=600,
        title="Colored by the weighted tip",
    )
    _fig
    return _fig


@app.cell
def _(px, tips):
    _fig = px.icicle(
        tips,
        path=["sex", "time", "day"],
        values="total_bill",
        color="time",
        width=800,
        height=600,
        title="Colored by time of day",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    Saturday dinner's tooltip reports a tip of 3.52. Is that the ordinary mean of the tip column, or the mean weighted by the bill?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**The weighted mean.** Each tip is weighted by `total_bill`. The sum of tip times bill, divided by the sum of the bills, is 3.52.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - Sunburst, treemap, and icicle charts take the same `path`, `values`, and `color`. The first name in `path` is the center of a sunburst and the outer level of a treemap or an icicle chart.
    - With no `values`, sector size is the number of rows. `values="price"` uses the sum of price. The `sedan/gas` group is 67 cars and the prices sum to 813499.
    - `color` on a numeric column is the average of that column weighted by `values`. For Saturday dinner, the weighted tip is 3.52 and the bills sum to 1778.4.
    - `color_discrete_map` names a color for each category. `px.Constant("Cars")` adds a single root to an icicle chart.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. Which chart uses rings, and which name in `path` is the center?
    2. How many sedan cars with gas fuel are in the cleaned table?
    3. What does `values="price"` change about a sector?
    4. Why is the Saturday-dinner tip 3.52 rather than the plain mean of `tip`?
    5. What does `hover_data={"tip": ":.2f"}` change?
    6. What is the same about the data passed to sunburst, treemap, and icicle?
    7. What does `px.Constant("Cars")` add to the icicle chart?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **The sunburst:** The first name in `path` is the center ring.
2. **67:** That is the count on the `sedan/gas` sector when `values` is omitted.
3. **The size becomes a sum:** The sector area follows the sum of `price` in that group. For sedan and gas, the sum is 813499.
4. **It is weighted by the bill:** Plotly averages `tip` using `total_bill` as the weight. Larger bills count more.
5. **The tooltip format:** Tip is shown with two decimal places. The sector color is unchanged.
6. **`path`, `values`, and `color`:** The three charts read the same columns. They differ in the shape used to draw each level.
7. **A single root:** Every other level is drawn under one block named Cars.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Sunburst charts in Python.* https://plotly.com/python/sunburst-charts/
    - Plotly. *Treemaps in Python.* https://plotly.com/python/treemaps/
    - Plotly. *Icicle charts in Python.* https://plotly.com/python/icicle-charts/
    """)
    return


if __name__ == "__main__":
    app.run()
