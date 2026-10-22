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
    # Visualizing Distributions and Trends

    ## Objectives

    - Draw a histogram of car length, then set the bins with `bin`, `maxbins`, `extent`, and `step`.
    - Add rules at the minimum, the mean, and the maximum length.
    - Split width and height by fuel type, using the full car table.
    - Fold length, width, and height into overlapping bars, lines, and areas.

    ## Background

    A histogram counts rows inside equal intervals. `bin=True` lets Altair choose the intervals. `alt.Bin(maxbins=20)` asks for at most 20 bins. `extent` is the start and end of the axis that gets binned. `step` is the width of each bin. The argument name is `extent`.

    A rule is a line at one aggregate, such as `mean(length)`. Layering uses `+`.

    The wide table has one row per car and one column for length, one for width, and one for height. `transform_fold` turns those three columns into two: `dimension` and `value`. Each car then contributes three rows. That is the long form used by the overlapping charts.

    The bin settings in this lesson are written in the code. There is no bin slider.

    ## Datasets Used

    - **Automobile Dataset** from the UCI Machine Learning Repository. Length, width, height, and fuel type are complete for all 205 cars.
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
def _(cars):
    dimens = cars[["length", "width", "height"]]
    print(dimens.head())
    return (dimens,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Histograms of length

    The first chart bins length with Altair's default. `bin=True` states the binning. `maxbins=20` asks for more, thinner bars.
    """)
    return


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar()
        .encode(alt.X("length:Q", bin=True), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar()
        .encode(alt.X("length:Q", bin=alt.Bin(maxbins=20)), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Length runs from 141.1 to 208.1. `extent=[140, 210]` covers that range. `step=5` makes bins 5 units wide. `step=10` makes them 10 units wide.
    """)
    return


@app.cell
def _(cars):
    print("Min(Length) =", cars.length.min())
    print("Max(Length) =", cars.length.max())
    return


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar()
        .encode(
            alt.X("length:Q", bin=alt.Bin(extent=[140, 210], step=5)),
            y="count()",
        )
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar()
        .encode(
            alt.X("length:Q", bin=alt.Bin(extent=[140, 210], step=10)),
            y="count()",
        )
        .properties(
            title={"text": "Car Length", "fontSize": 16},
            width=500,
            height=300,
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_step` is 10. Are those length bins wider or narrower than bins with `step=5`?
    """)
    return


@app.cell
def _(alt, dimens):
    student_step = 10
    _chart = (
        alt.Chart(dimens)
        .mark_bar()
        .encode(
            alt.X("length:Q", bin=alt.Bin(extent=[140, 210], step=student_step)),
            y="count()",
        )
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Wider.** `step` is the width of each bin. 10 covers twice the length of 5.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Minimum, mean, and maximum

    The wheat bars use `extent` 140 to 210 and `step` 10. The thick black rule is the mean length. The thin rules are the minimum and the maximum. `+` layers them on one chart.
    """)
    return


@app.cell
def _(alt, dimens):
    base = alt.Chart(dimens)
    bars = (
        base.mark_bar(color="wheat")
        .encode(
            alt.X("length:Q", bin=alt.Bin(extent=[140, 210], step=10)),
            y="count()",
        )
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    mean_rule = base.mark_rule(color="black").encode(
        x="mean(length):Q",
        size=alt.value(4),
    )
    min_rule = base.mark_rule(color="black").encode(
        x="min(length):Q",
        size=alt.value(1),
    )
    max_rule = base.mark_rule(color="black").encode(
        x="max(length):Q",
        size=alt.value(1),
    )
    _chart = bars + min_rule + mean_rule + max_rule
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Width and height by fuel type

    The width and height charts can use `dimens`. The fuel-type split needs `cars`, because `dimens` has only length, width, and height. `row` stacks gas and diesel. `column` places them side by side.
    """)
    return


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar(color="darksalmon")
        .encode(alt.X("width:Q", bin=True), y="count()")
        .properties(title={"text": "Car Width", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar(color="darksalmon")
        .encode(
            alt.X("width:Q", bin=True),
            y="count()",
            row="fuel_type:N",
        )
        .properties(title={"text": "Car Width", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_bar(color="skyblue")
        .encode(alt.X("height:Q", bin=True), y="count()")
        .properties(title={"text": "Car Height", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_bar(color="skyblue")
        .encode(
            alt.X("height:Q", bin=True),
            y="count()",
            column="fuel_type:N",
        )
        .properties(title={"text": "Car Height", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Overlapping histograms

    `dimens.head()` is wide: one column per dimension. `melt` shows the long form, one row per car and dimension. `transform_fold` does that reshape inside the chart. `maxbins=100` and a low opacity let the three histograms share one axis.
    """)
    return


@app.cell
def _(dimens):
    long_dimens = dimens.melt(var_name="dimension", value_name="value")
    print(long_dimens.head())
    print(long_dimens.shape)
    return


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .transform_fold(["length", "width", "height"], as_=["dimension", "value"])
        .mark_bar(opacity=0.7, binSpacing=0)
        .encode(
            alt.X("value:Q", bin=alt.Bin(maxbins=100)),
            alt.Y("count()"),
            alt.Color("dimension:N"),
        )
        .properties(
            width=500,
            title={
                "text": ["Overlapping Histograms", "(length, width, and height)"],
                "fontSize": 20,
            },
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lines

    `mark_line` with `count()` connects the counts of the distinct length values. `point` adds a marker on that line. The second line uses a larger marker.

    The overlapping lines fold the three dimensions, the same way the overlapping bars do.
    """)
    return


@app.cell
def _(alt, cars):
    _chart = (
        alt.Chart(cars)
        .mark_line()
        .encode(alt.X("length:Q"), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_line(point=alt.OverlayMarkDef(color="darkred", size=80))
        .encode(alt.X("length:Q"), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .transform_fold(["length", "width", "height"], as_=["dimension", "value"])
        .mark_line(opacity=0.7)
        .encode(
            alt.X("value:Q"),
            alt.Y("count()"),
            alt.Color("dimension:N"),
        )
        .properties(title={"text": "Overlapping Lines", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Areas

    `mark_area` fills under the counts. `interpolate="step"` makes a staircase. `line=True` draws the boundary. The last chart drops the boundary and keeps the step fill, still colored by dimension.
    """)
    return


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_area(opacity=0.7, color="silver", line=True)
        .encode(alt.X("length:Q"), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .mark_area(opacity=0.7, color="silver", interpolate="step", line=True)
        .encode(alt.X("length:Q"), y="count()")
        .properties(title={"text": "Car Length", "fontSize": 16})
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .transform_fold(["length", "width", "height"], as_=["dimension", "value"])
        .mark_area(opacity=0.7, interpolate="step", line=True)
        .encode(
            alt.X("value:Q"),
            alt.Y("count()"),
            alt.Color("dimension:N"),
        )
        .properties(
            width=500,
            title={"text": "Overlapping Areas", "fontSize": 16},
        )
    )
    _chart
    return _chart


@app.cell
def _(alt, dimens):
    _chart = (
        alt.Chart(dimens)
        .transform_fold(["length", "width", "height"], as_=["dimension", "value"])
        .mark_area(opacity=0.7, interpolate="step")
        .encode(
            alt.X("value:Q"),
            alt.Y("count()"),
            alt.Color("dimension:N"),
        )
        .properties(
            width=500,
            title={"text": "Overlapping Areas", "fontSize": 16},
        )
    )
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - Length, width, and height are complete for all 205 cars. Length runs from 141.1 to 208.1.
    - `bin=True` and `maxbins` set how many bars Altair may draw. `extent=[140, 210]` sets the length range, and `step` sets the bin width. Step 10 is wider than step 5.
    - The layered length chart draws the histogram plus a thin minimum rule, a thick mean rule, and a thin maximum rule.
    - Width by fuel type uses `row`. Height by fuel type uses `column`. Both use `cars`, because the three-column table has no fuel type.
    - The wide table has one column per dimension. Folding it makes 615 rows (205 cars times 3). The overlapping bars, lines, and areas count those long-form values. The bins are fixed in the code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does `alt.Bin(maxbins=20)` limit?
    2. What do `extent` and `step` set?
    3. Which three rules are layered on the wheat length bars?
    4. Why do the fuel-type histograms use `cars`?
    5. What does the wide `dimens` table contain?
    6. What does `transform_fold` produce?
    7. What does `interpolate="step"` do to an area chart?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **The number of bins.** Altair uses at most 20 bins.
2. **The range and the bin width.** `extent` is the start and end. `step` is how wide each bin is.
3. **Minimum, mean, and maximum.** The mean rule is thicker (`size` 4). The other two use `size` 1.
4. **`dimens` has no fuel type.** It only has length, width, and height.
5. **One row per car and three columns.** The columns are length, width, and height.
6. **One row per car and dimension.** The new columns are `dimension` and `value`. 205 cars become 615 rows.
7. **A staircase.** The area rises and falls in steps instead of a smooth slope.
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
    - Altair. *Bin.* https://altair-viz.github.io/user_guide/generated/channels/altair.Bin.html
    - Altair. *Fold transform.* https://altair-viz.github.io/user_guide/transform/fold.html
    """)
    return


if __name__ == "__main__":
    app.run()
