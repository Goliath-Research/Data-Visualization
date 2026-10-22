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
    # Adding Data Driven Inputs

    ## Objectives

    - Drag an interval on horsepower against highway mpg, and limit that interval to x or to y.
    - Click a make bar, then highlight a make by hovering.
    - Select body style from a legend, then select the pair body style and fuel type.
    - Bind a dropdown and a set of radio buttons to body style, and filter the points.
    - Color cars red when the price is above a slider value.

    ## Background

    `selection_interval` is a rectangle you drag. `encodings=["x"]` keeps the rectangle full height, so only the x range matters. `encodings=["y"]` keeps it full width.

    `selection_point` selects marks. The default event is a click. `on="mouseover"` selects while the pointer is over a bar. `fields` says which columns define a selection. One field selects every point with that body style. Two fields select the body style and fuel type pair.

    A binding attaches a widget to a selection. `binding_select` is a dropdown. `binding_radio` is a set of radio buttons. `binding_range` is a slider. `alt.param` holds the slider value. `transform_filter` keeps the rows the selection accepts.

    Each chart below creates its own selection. Click and Shift on a legend selects more than one entry.

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
    print(cars.body_style.unique())
    return (cars,)


@app.cell
def _(cars, mo):
    mo.Html(cars.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interval selection

    Drag a rectangle. Points inside keep the fuel-type color. Points outside turn light grey. The next two charts limit the drag to the x axis, then to the y axis.
    """)
    return


@app.cell
def _(alt, cars):
    interval = alt.selection_interval()
    _chart = (
        alt.Chart(cars)
        .mark_point(size=50)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(interval, "fuel_type:N", alt.value("lightgrey")),
        )
        .add_params(interval)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    interval_x = alt.selection_interval(encodings=["x"])
    _chart = (
        alt.Chart(cars)
        .mark_point(size=50)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(interval_x, "fuel_type:N", alt.value("lightgrey")),
        )
        .add_params(interval_x)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    interval_y = alt.selection_interval(encodings=["y"])
    _chart = (
        alt.Chart(cars)
        .mark_point(size=50)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(interval_y, "fuel_type:N", alt.value("lightgrey")),
        )
        .add_params(interval_y)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Point selection

    Click a bar to color that make by fuel type. The other makes turn light grey. The second chart uses `on="mouseover"` and `nearest=True`, so the bar under the pointer is the selected one.
    """)
    return


@app.cell
def _(alt, cars):
    point = alt.selection_point()
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            color=alt.condition(point, "fuel_type:N", alt.value("lightgrey")),
        )
        .add_params(point)
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    point_nearest = alt.selection_point(on="mouseover", nearest=True)
    _chart = (
        alt.Chart(cars)
        .mark_bar()
        .encode(
            alt.X("make:N", title="Make"),
            alt.Y("count()", title="Count"),
            color=alt.condition(point_nearest, "fuel_type:N", alt.value("lightgrey")),
        )
        .add_params(point_nearest)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A legend of one field

    The selection field is `body_style`. The scatter and the legend share that selection. Click a body style on the legend. Click and Shift to add another. Points of the selected styles keep their color. The others turn light gray.
    """)
    return


@app.cell
def _(alt, cars):
    styles = alt.selection_point(fields=["body_style"])
    style_color = alt.condition(
        styles,
        alt.Color("body_style:N", legend=None),
        alt.value("lightgray"),
    )
    scatter = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=style_color,
            tooltip="make:N",
        )
    )
    legend = (
        alt.Chart(cars)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("body_style:N", axis=alt.Axis(orient="right")),
            color=style_color,
        )
        .add_params(styles)
    )
    _chart = scatter | legend
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A legend of two fields

    The fields are `body_style` and `fuel_type`. The legend is a grid of those two columns. A click selects one pair.
    """)
    return


@app.cell
def _(alt, cars):
    pairs = alt.selection_point(fields=["body_style", "fuel_type"])
    pair_color = alt.condition(
        pairs,
        alt.Color("body_style:N", legend=None),
        alt.value("lightgray"),
    )
    scatter_pairs = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=pair_color,
            tooltip="make:N",
        )
    )
    legend_pairs = (
        alt.Chart(cars)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("body_style:N", axis=alt.Axis(orient="right")),
            x="fuel_type:N",
            color=pair_color,
        )
        .add_params(pairs)
    )
    _chart = scatter_pairs | legend_pairs
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Dropdown

    | Input | What it draws |
    | --- | --- |
    | `binding_select` | A dropdown of one item from a list |
    | `binding_radio` | Radio buttons, one choice |
    | `binding_range` | A slider |
    | `binding_checkbox` | Checkboxes |

    The first dropdown lists the body styles and starts on sedan. Empty means no style is selected, so the points are light gray until you choose one.
    """)
    return


@app.cell
def _(alt, cars):
    body_options = list(cars.body_style.unique())
    print(body_options)
    dropdown = alt.binding_select(options=body_options, name="Body: ")
    chosen = alt.selection_point(
        fields=["body_style"],
        bind=dropdown,
        value="sedan",
    )
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(
                chosen,
                alt.Color("body_style:N", legend=None),
                alt.value("lightgray"),
            ),
            tooltip="make:N",
        )
        .add_params(chosen)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This dropdown adds an empty choice, `None`, before the five body styles. `transform_filter` keeps only the chosen style. With `None`, no extra filter is applied.
    """)
    return


@app.cell
def _(alt, cars):
    body_with_none = [None, "convertible", "hatchback", "sedan", "wagon", "hardtop"]
    dropdown_none = alt.binding_select(options=body_with_none, name="Body: ")
    chosen_none = alt.selection_point(fields=["body_style"], bind=dropdown_none)
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(
                chosen_none,
                alt.Color("body_style:N", legend=None),
                alt.value("lightgray"),
            ),
            tooltip="make:N",
        )
        .add_params(chosen_none)
        .transform_filter(chosen_none)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Radio buttons

    The options are an empty choice plus the body styles in the file. One button is selected at a time.
    """)
    return


@app.cell
def _(alt, cars):
    radio = alt.binding_radio(
        options=[None, *list(cars.body_style.unique())],
        name="Body: ",
    )
    chosen_radio = alt.selection_point(fields=["body_style"], bind=radio)
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=80)
        .encode(
            x=alt.X("horsepower:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(
                chosen_radio,
                alt.Color("body_style:N", legend=None),
                alt.value("lightgray"),
            ),
            tooltip="make:N",
        )
        .add_params(chosen_radio)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A price slider

    The slider runs from 0 to 50,000 in steps of 10 and starts at 20,000. A car is red when its price is greater than the slider. Otherwise it is silver.
    """)
    return


@app.cell
def _(alt, cars):
    price_slider = alt.binding_range(min=0, max=50000, step=10, name="Price: ")
    price_cut = alt.param(bind=price_slider, value=20000)
    _chart = (
        alt.Chart(cars)
        .mark_circle(size=60)
        .encode(
            x=alt.X("price:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("highway_mpg:Q", scale=alt.Scale(zero=False)),
            color=alt.condition(
                alt.datum.price > price_cut,
                alt.value("red"),
                alt.value("silver"),
            ),
            tooltip="make:N",
        )
        .add_params(price_cut)
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_price` is 20000. A car priced at 18500 is compared with `price > student_price`. Is that car red or silver?
    """)
    return


@app.cell
def _():
    student_price = 20000
    student_car = 18500
    print("red" if student_car > student_price else "silver")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Silver.** 18500 is not greater than 20000, so the condition uses the second color.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - An interval selection colors the points inside the drag by fuel type. Limiting `encodings` to `"x"` or `"y"` keeps only that axis in the test.
    - A point selection on the make bars colors the clicked make. `on="mouseover"` moves that highlight with the pointer.
    - A legend selection on `body_style` highlights every car of the clicked styles. Adding `fuel_type` highlights one pair. Click and Shift adds another selection.
    - The body-style dropdown starts at sedan. A second dropdown includes an empty choice and can filter the points. The radio buttons offer the same styles, one at a time.
    - The price slider starts at 20,000. Prices above the slider are red. Prices at or below it are silver.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does a drag do on the first interval chart?
    2. What changes when the interval encodings are only `"x"`?
    3. How do you select a make bar without clicking?
    4. What does Click and Shift do on the body-style legend?
    5. What does the two-field legend select?
    6. What does `transform_filter` do on the dropdown chart?
    7. Which prices are red when the slider is at 20,000?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **It colors the points inside the rectangle.** Points outside turn light grey. The color inside is fuel type.
2. **Only the horizontal range matters.** The band covers the full height.
3. **Hover.** That chart uses `on="mouseover"` and `nearest=True`.
4. **It adds another body style.** One click selects a single style.
5. **A body style and a fuel type together.** Both fields have to match.
6. **It keeps the chosen body style.** The empty choice leaves the points unfiltered.
7. **Prices above 20,000.** A price equal to 20,000 stays silver.
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
    - Altair. *Interactive charts.* https://altair-viz.github.io/user_guide/interactions.html
    """)
    return


if __name__ == "__main__":
    app.run()
