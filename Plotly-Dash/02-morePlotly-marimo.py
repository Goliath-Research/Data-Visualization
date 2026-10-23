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
    # More on Plotly Express

    ## Objectives

    - Compare price across categories with a box, a strip, and a violin.
    - Draw city fuel economy against highway fuel economy, with price as the size and the color, and add a marginal plot on each axis.
    - Turn a cross-table into a wide table and a long table, and see which arguments `px.bar` needs for each.
    - Change the hover tooltip and set discrete colors or a continuous color scale.

    ## Background

    A box, a strip, and a violin all show how a number is spread inside each category. A box marks the median and the quartiles. A strip draws every row as a point. A violin adds the shape of the distribution, so two clusters can show up as two peaks.

    Plotly Express also accepts the same counts in two shapes. A wide table has one column per category. A long table has one row per category and a column that holds the count. The bar chart arguments depend on that shape.

    ## Datasets Used

    - **Automobile Dataset** from the UCI Machine Learning Repository. The charts use the 159 rows that have no missing value.
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
    Rows with a missing value are dropped so that every chart in this lesson uses the same 159 cars.
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
    ## Box, strip, and violin

    The box draws the median as a line inside the box. The box itself runs from the first quartile to the third quartile. The whiskers run out toward the lower and upper prices. `points="all"` adds every car on top of that summary.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.box(cars, x="make", y="price", width=800, title="Price by make")
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.box(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        width=800,
        title="Price by body style",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.box(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        points="all",
        width=800,
        title="Price by body style, every car",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A strip plot keeps the points and leaves out the box. Each dot is one car.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.strip(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        width=800,
        title="Price by body style",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A violin draws the density: where the shape is wide, more cars have a price near that height. `box=True` puts the box inside the violin. `points="all"` adds the cars as well.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.violin(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        width=800,
        title="Price by body style",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.violin(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        points="all",
        width=800,
        title="Price by body style, every car",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.violin(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        box=True,
        width=800,
        title="Violin with a box inside",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.violin(
        cars,
        x="body_style",
        y="price",
        color="body_style",
        box=True,
        points="all",
        width=800,
        title="Violin with a box and every car",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    This strip plot uses horsepower. What does one dot stand for?
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.strip(
        cars,
        x="body_style",
        y="horsepower",
        color="body_style",
        width=800,
        title="Horsepower by body style",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**One car.** The height is that car's `horsepower`. Cars with the same body style share a column.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Scatter plots

    Each point is one car. `size` and `color` both use `price`, so a more expensive car is both larger and darker on the color scale.

    `marginal_x` draws a summary of the horizontal variable above the scatter. `marginal_y` draws a summary of the vertical variable beside it. The two sides can use different summaries.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        width=800,
        title="City MPG vs highway MPG",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        size="price",
        color="price",
        width=800,
        title="City MPG vs highway MPG, sized by price",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        size="price",
        color="price",
        marginal_x="box",
        marginal_y="box",
        width=700,
        height=500,
        title="Box margins",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        size="price",
        color="price",
        marginal_x="violin",
        marginal_y="violin",
        width=700,
        height=500,
        title="Violin margins",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        size="price",
        color="price",
        marginal_x="histogram",
        marginal_y="histogram",
        width=700,
        height=500,
        title="Histogram margins",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.scatter(
        cars,
        x="city_mpg",
        y="highway_mpg",
        size="price",
        color="price",
        marginal_x="violin",
        marginal_y="box",
        width=700,
        height=500,
        title="Violin on x, box on y",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Wide form and long form

    A wide table stores one category across columns. A long table stores that category down a column.

    `pd.crosstab` counts cars for each pair of `num_doors` and `body_style`. The result is wide: two rows (`four` and `two`) and one column per body style. The table has five data columns, so it is shown as HTML.
    """)
    return


@app.cell
def _(cars, pd):
    wide_counts = pd.crosstab(cars.num_doors, cars.body_style)
    return (wide_counts,)


@app.cell
def _(mo, wide_counts):
    mo.Html(wide_counts.to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `melt` turns those body-style columns into rows. `value` holds the count. This long table has three columns.
    """)
    return


@app.cell
def _(wide_counts):
    long_counts = wide_counts.reset_index().melt(id_vars=["num_doors"])
    print(long_counts)
    return (long_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bars from the wide table

    Plotly Express can read the wide table without `x` and `y`. Each body-style column becomes one set of bars, and the row labels (`four` and `two`) become the horizontal axis.

    `facet_col` and `facet_row` give each body style its own panel.
    """)
    return


@app.cell
def _(px, wide_counts):
    _fig = px.bar(
        wide_counts,
        x=wide_counts.index,
        y=wide_counts.columns,
        width=800,
        title="Doors and body style",
    )
    _fig
    return _fig


@app.cell
def _(px, wide_counts):
    _fig = px.bar(wide_counts, width=800, title="Doors and body style")
    _fig
    return _fig


@app.cell
def _(px, wide_counts):
    _fig = px.bar(
        wide_counts,
        facet_col="body_style",
        width=900,
        title="One panel per column",
    )
    _fig
    return _fig


@app.cell
def _(px, wide_counts):
    _fig = px.bar(
        wide_counts,
        facet_row="body_style",
        width=600,
        height=900,
        title="One panel per row",
    )
    _fig
    return _fig


@app.cell
def _(wide_counts):
    print(wide_counts.T)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After the transpose, the columns are the door counts. `facet_row="num_doors"` puts each door count in its own panel.
    """)
    return


@app.cell
def _(px, wide_counts):
    _fig = px.bar(
        wide_counts.T,
        facet_row="num_doors",
        width=800,
        title="Panels by number of doors",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bars from the long table

    Plotly Express treats a call with no `x` and no `y` as a wide table. This long table has text columns and a numeric `value` column, so that guess fails. The next cell prints this error: `ValueError: Plotly Express cannot process wide-form data with columns of different type`. The cell after it names `x="body_style"` and `y="value"`.
    """)
    return


@app.cell
def _(long_counts, px):
    try:
        px.bar(long_counts, width=800, title="This cell stops")
    except ValueError as error:
        print("ValueError:", error)
    return


@app.cell
def _(long_counts, px):
    _fig = px.bar(
        long_counts,
        x="body_style",
        y="value",
        width=800,
        title="Doors and body style",
    )
    _fig
    return _fig


@app.cell
def _(long_counts, px):
    _fig = px.bar(
        long_counts,
        x="body_style",
        y="value",
        color="num_doors",
        width=800,
        title="Colored by number of doors",
    )
    _fig
    return _fig


@app.cell
def _(long_counts, px):
    _fig = px.line(
        long_counts,
        x="body_style",
        y="value",
        color="num_doors",
        width=800,
        title="The same counts as lines",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `line_dash` uses a column the way `color` does, but it changes the dash pattern. Using both on `num_doors` gives each door count its own color and its own dash.
    """)
    return


@app.cell
def _(long_counts, px):
    _fig = px.line(
        long_counts,
        x="body_style",
        y="value",
        line_dash="num_doors",
        width=800,
        title="Dash pattern by number of doors",
    )
    _fig
    return _fig


@app.cell
def _(long_counts, px):
    _fig = px.line(
        long_counts,
        x="body_style",
        y="value",
        color="num_doors",
        line_dash="num_doors",
        width=800,
        title="Color and dash by number of doors",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The long-table bar needs `x` and `y`. Which column must be `y` if the bar height is the count of cars?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**`value`.** That column holds the count from the cross-table. `body_style` is the category along the horizontal axis.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hover tooltips

    Move the pointer over a bar to read the tooltip.

    - `hover_data` can hide a field with `False`, or format a number. `":.1f"` keeps one decimal place.
    - `labels` renames a field in the tooltip and in the legend.
    - `hover_name` prints that value at the top of the tooltip.

    The first chart shows fuel type. The second sets `hover_data={"fuel_type": False}`, so fuel type stays in the legend and leaves the tooltip.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.histogram(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        histfunc="avg",
        width=800,
        title="Average price by make and fuel type",
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
        histfunc="avg",
        hover_data={"fuel_type": False},
        width=800,
        title="Fuel type hidden in the tooltip",
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
        histfunc="avg",
        hover_data={"fuel_type": False},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="Renamed tooltip fields",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The same labels on a bar chart rename the legend as well. `px.bar` adds the price of every car in that make and fuel type, so the height is a sum. Each car is one piece of the bar, and its tooltip shows that car's price. `":.1f"` shows it with one decimal place. `hover_name="horsepower"` puts a horsepower value at the top of the tooltip.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        hover_data={"fuel_type": False},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="Sum of price by make and fuel type",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        hover_data={"fuel_type": False, "price": ":.1f"},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="Price with one decimal place",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        hover_data={"fuel_type": False, "price": ":.1f"},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        hover_name="horsepower",
        width=800,
        title="Horsepower at the top of the tooltip",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The format string on `price` is `":.0f"`. How many decimal places does the tooltip show?
    """)
    return


@app.cell
def _(cars, px):
    price_format = ":.0f"
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        hover_data={"price": price_format},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="Price with no decimal places",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**None.** `:.0f` rounds the `price` to a whole number.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Color

    `color_discrete_sequence` is a list. The first color goes to the first category. `color_discrete_map` is a dictionary from a category name to a color, so gas and diesel keep the colors you name.

    `color_continuous_scale` is for a numeric color. Here `price` is both the height and the color, and `"ice_r"` is the scale.
    """)
    return


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        color_discrete_sequence=["green", "orange"],
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="A list of colors",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="fuel_type",
        color_discrete_map={"gas": "grey", "diesel": "brown"},
        labels={"price": "Price", "make": "Make", "fuel_type": "Fuel type"},
        width=800,
        title="A dictionary of colors",
    )
    _fig
    return _fig


@app.cell
def _(cars, px):
    _fig = px.bar(
        cars,
        x="make",
        y="price",
        color="price",
        color_continuous_scale="ice_r",
        labels={"price": "Price", "make": "Make"},
        width=800,
        title="A continuous price scale",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The lesson uses the 159 Automobile rows that have no missing value.
    - A box shows the median and the quartiles. A strip shows every car. A violin shows the density, and it can include the box and the points.
    - On the scatter plot, `marginal_x` and `marginal_y` can be a box, a violin, or a histogram, and the two axes can differ.
    - The door-and-body-style counts are wide in the cross-table and long after `melt`. The wide table can be drawn without `x` and `y`. The long table needs `x="body_style"` and `y="value"`. Without those arguments Plotly reports that it cannot process wide-form data with columns of different type.
    - `hover_data` hides or formats a tooltip field. `labels` renames fields, including the legend. `hover_name` fills the top line of the tooltip.
    - A discrete color can be a list or a dictionary. A numeric color uses `color_continuous_scale`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What do the ends of the box represent?
    2. What does `points="all"` add to a box or a violin?
    3. On the scatter plot, which argument sizes the points, and which colors them?
    4. Why can the wide cross-table be drawn without `x` and `y`?
    5. Why does `px.bar(long_counts)` stop with an error?
    6. What does `hover_data={"fuel_type": False}` change?
    7. When would you use `color_continuous_scale` instead of `color_discrete_map`?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **The first and third quartiles:** The line inside the box is the median. The whiskers continue toward the lower and upper prices.
2. **Every row:** Each car is drawn as a point on top of the summary.
3. **`size="price"` and `color="price"`:** Both use the price. One changes the area of the point, and the other picks a color from the scale.
4. **The columns are the categories:** Each body style is already a column of counts, and the row index is the number of doors.
5. **The columns have different types:** With no `x` or `y`, Plotly tries to read the table as wide data. Text columns and the numeric `value` column cannot share that path. Naming `x` and `y` tells it which columns to use.
6. **The tooltip:** Fuel type remains the color and the legend. It is left out of the hover text.
7. **When the color column is numeric:** `color_discrete_map` names a color for each category. `color_continuous_scale` maps a range of numbers, such as price, onto a scale.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Plotly Express in Python.* https://plotly.com/python/plotly-express/
    - Plotly. *Box plots in Python.* https://plotly.com/python/box-plots/
    - Plotly. *Violin plots in Python.* https://plotly.com/python/violin/
    """)
    return


if __name__ == "__main__":
    app.run()
