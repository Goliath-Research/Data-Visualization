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
    # Bar Plots with Altair

    ## Objectives

    - Count cars by make and by fuel type, and set the chart width and the label angle.
    - Color the make bars by the count, by highway mpg, and by body style.
    - Split the make counts into columns or rows by fuel type.
    - Highlight Toyota with a condition, and aggregate the mean, maximum, and minimum price by make.
    - Draw horizontal count bars and write the count beside each bar.

    ## Background

    `mark_bar` draws one bar per category. `count()` is an aggregate: Altair counts the rows in each group. `transform_aggregate` computes another summary, such as `mean(price)`, inside the chart.

    `column` and `row` repeat the chart once per category. `alt.condition` picks one encoding when a test is true and another when it is false. Here the test is `make == "toyota"`.

    `|` places charts side by side. `&` places them one above the other. `mark_text` writes a label. `dx` shifts that label to the right of the bar end.

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
    | Short-hand | Long-hand |
    | --- | --- |
    | `x="varname"` | `alt.X("varname")` |
    | `x="varname:Q"` | `alt.X("varname", type="quantitative")` |
    | `x="sum(varname)"` | `alt.X("varname", aggregate="sum")` |
    | `x="count():Q"` | `alt.X(aggregate="count", type="quantitative")` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vertical bars

    The height is the number of cars of that make. `:N` marks the x column as nominal, a category with no numeric order.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
        )
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Fuel type has two values. `properties(width=300)` widens the chart. `labelAngle=0` draws the category labels upright.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("fuel_type:N", title="Fuel type"),
            alt.Y("count()", title="Count"),
        )
        .properties(width=300)
    )
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("fuel_type:N", axis=alt.Axis(title="Fuel type", labelAngle=0)),
            alt.Y("count()", title="Count"),
        )
        .properties(width=300)
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Color

    Color can be the count itself, a quantitative column such as highway mpg, or a nominal column such as body style. A quantitative color is a shade. A nominal color is one color per category, and the bars are stacked when that category is not the x axis.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("count()", legend=alt.Legend(title="Count")),
        )
    )
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("highway_mpg", title="Highway (MPG)"),
        )
    )
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("body_style", title="Body Style"),
        )
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Fuel type as color, column, or row

    Coloring by fuel type stacks gas and diesel inside each make. `column` repeats the chart once for gas and once for diesel. `row` stacks those two charts vertically.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("fuel_type", title="Fuel type"),
        )
        .properties(title={"text": "Make & Fuel Type", "fontSize": 20})
    )
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("fuel_type", title="Fuel type"),
            column="fuel_type",
        )
        .properties(title={"text": "Make & Fuel Type", "fontSize": 20})
    )
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            alt.Color("fuel_type", title="Fuel type"),
            row="fuel_type",
        )
        .properties(title={"text": "Make & Fuel Type", "fontSize": 20})
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A condition

    `alt.datum.make == "toyota"` is true for the Toyota bars. Those bars are steel blue. The other makes are silver.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y("count():Q", title="Count"),
            color=alt.condition(
                alt.datum.make == "toyota",
                alt.value("steelblue"),
                alt.value("silver"),
            ),
        )
        .properties(
            title={"text": "Make & Fuel Type", "fontSize": 20},
            width=600,
        )
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_make` is `"honda"`. Which bars turn steel blue?
    """)
    return


@app.cell
def _(alt, cars):
    student_make = "honda"
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y("count():Q", title="Count"),
            color=alt.condition(
                alt.datum.make == student_make,
                alt.value("steelblue"),
                alt.value("silver"),
            ),
        )
        .properties(width=600)
    )
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**The Honda bar.** The condition is true only when `make` equals `student_make`.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Aggregate inside the chart

    `transform_aggregate` computes the mean price by make. The y domain is 0 to 50,000 so the mean, the maximum, and the minimum share a scale. Four cars have no price, so they do not enter these three summaries.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y(
                "avg_price:Q",
                title="Average Price",
                scale=alt.Scale(domain=[0, 50000]),
            ),
            color=alt.value("limegreen"),
        )
        .transform_aggregate(avg_price="mean(price)", groupby=["make"])
        .properties(title={"text": "Average Price by Make", "fontSize": 20})
    )
    return _chart


@app.cell
def _(alt, cars):
    max_price = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y(
                "max_price:Q",
                title="Max Price",
                scale=alt.Scale(domain=[0, 50000]),
            ),
            color=alt.value("seagreen"),
        )
        .transform_aggregate(max_price="max(price)", groupby=["make"])
        .properties(title={"text": "Max Price by Make", "fontSize": 20})
    )
    min_price = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y(
                "min_price:Q",
                title="Min Price",
                scale=alt.Scale(domain=[0, 50000]),
            ),
            color=alt.value("palegreen"),
        )
        .transform_aggregate(min_price="min(price)", groupby=["make"])
        .properties(title={"text": "Min Price by Make", "fontSize": 20})
    )
    _side_by_side = min_price | max_price
    return _side_by_side


@app.cell
def _(alt, cars):
    _max_price = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y(
                "max_price:Q",
                title="Max Price",
                scale=alt.Scale(domain=[0, 50000]),
            ),
            color=alt.value("seagreen"),
        )
        .transform_aggregate(max_price="max(price)", groupby=["make"])
        .properties(title={"text": "Max Price by Make", "fontSize": 20})
    )
    _min_price = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            x=alt.X("make:N", title="Make"),
            y=alt.Y(
                "min_price:Q",
                title="Min Price",
                scale=alt.Scale(domain=[0, 50000]),
            ),
            color=alt.value("palegreen"),
        )
        .transform_aggregate(min_price="min(price)", groupby=["make"])
        .properties(title={"text": "Min Price by Make", "fontSize": 20})
    )
    _stacked = _min_price & _max_price
    return _stacked


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Horizontal bars with labels

    Swapping x and y makes the bars horizontal. `value_counts(sort=False)` keeps the make order from the table. The counts go into a new two-column table. `mark_text` with `dx=5` writes the count just to the right of each bar. The bars and the labels are layered with `+`.
    """)
    return


@app.cell
def _(cars, pd):
    make_counts = cars.make.value_counts(sort=False)
    make_table = pd.DataFrame(
        {"make": make_counts.index, "count": make_counts.values}
    )
    print(make_table.head())
    return (make_table,)


@app.cell
def _(alt, make_table):
    horizontal = (
        alt.Chart(make_table)
        .mark_bar()
        .encode(
            alt.Y("make:N", axis=alt.Axis(title="Make")),
            alt.X("count:Q", axis=alt.Axis(title="Count")),
        )
        .properties(height=500, title="Make")
    )
    labels = horizontal.mark_text(align="left", baseline="middle", dx=5).encode(
        text="count:Q"
    )
    _chart = horizontal + labels
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - `count()` is the number of cars in each make or fuel type. `width` and `labelAngle` change the chart size and the category labels.
    - Color by `count()` or by highway mpg is a quantitative shade. Color by body style or fuel type splits the bar into categories.
    - `column="fuel_type"` repeats the make chart side by side. `row="fuel_type"` repeats it one above the other.
    - `alt.condition` paints Toyota steel blue and the other makes silver. `transform_aggregate` computes the mean, the maximum, and the minimum price by make on a 0 to 50,000 scale. `|` joins the min and max charts horizontally. `&` stacks them.
    - The horizontal chart uses a two-column count table. `mark_text` with `dx=5` labels each bar.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does the height of a make bar mean when y is `count()`?
    2. What does `labelAngle=0` do?
    3. What is the difference between coloring by highway mpg and coloring by body style?
    4. What does `column="fuel_type"` add?
    5. Which bars are steel blue in the condition chart?
    6. What do `|` and `&` do with the min and max price charts?
    7. What does `dx=5` do to the count labels?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **The number of cars of that make.** `count()` counts rows.
2. **The labels stand upright.** The default angle tilts them.
3. **A shade versus a stack.** Highway mpg is a number, so the bar gets a shade. Body style is a category, so each style is a colored piece of the bar.
4. **One chart per fuel type, side by side.** `row` would put those charts one above the other.
5. **Toyota.** The condition tests `make == "toyota"`. Every other make is silver.
6. **Side by side, and one above the other.** `|` is horizontal. `&` is vertical.
7. **It shifts them five pixels to the right.** The label starts just past the end of the bar.
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
    - Altair. *Bar chart.* https://altair-viz.github.io/gallery/bar_chart.html
    """)
    return


if __name__ == "__main__":
    app.run()
