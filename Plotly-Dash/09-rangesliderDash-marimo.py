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
    # A Range Slider for Months

    ## Objectives

    - Keep every daily row whose month falls inside a start month and an end month.
    - Draw humidity against the three zone powers, on axes fixed from the whole year.
    - Choose that span with a range slider. In Dash the component is `dcc.RangeSlider`, and it starts at January through March. The slider below does the same filtering in this file.

    ## Background

    A range slider has two handles. Its value is a pair of numbers, the low month and the high month. The filter keeps months from the low value through the high value, including both ends.

    The chart uses humidity on the horizontal axis. The limits still come from the whole year: humidity plus 5, and Zone 1's power plus 5,000.

    ## Datasets Used

    - **Power consumption of Tetouan city**, from the UCI Machine Learning Repository. Three zones in Tetouan, Morocco, in 2017.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the file is read from

    Pandas can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website, and it can read `Tetuan-City-power-consumption.csv` from this folder.
    - **Inside a web browser.** This lesson can run inside a web page. The browser only lets a page download files from websites that allow it. This security rule is called **CORS**. The UCI website does not allow it, so the browser blocks that download.

    This lesson reads a GitHub copy of the file. GitHub allows a browser page to read its files, so the copy works in both places. The UCI address and the local file name are kept in comments.
    """)
    return


@app.cell
def _():
    power_file = (
        "https://raw.githubusercontent.com/Goliath-Research/"
        "Data-Visualization/main/Plotly-Dash/"
        "Tetuan-City-power-consumption.csv"
    )
    # UCI address, blocked in the browser:
    # https://archive.ics.uci.edu/ml/machine-learning-databases/00616/Tetuan%20City%20power%20consumption.csv
    # Local file in this folder: Tetuan-City-power-consumption.csv
    return (power_file,)


@app.cell
def _(pd, power_file):
    power_raw = pd.read_csv(power_file)
    print(power_raw.shape)
    return (power_raw,)


@app.cell
def _(pd, power_raw):
    power = power_raw.rename(
        columns={
            "Zone 1 Power Consumption": "Zone1",
            "Zone 2  Power Consumption": "Zone2",
            "Zone 3  Power Consumption": "Zone3",
        }
    )
    power = power.assign(DateTime=pd.to_datetime(power["DateTime"]))
    daily = (
        power.groupby(pd.Grouper(key="DateTime", freq="D"))
        .mean(numeric_only=True)
        .reset_index()
    )
    daily = daily.assign(month=daily.DateTime.dt.month.astype(int))
    print(daily.shape)
    return (daily,)


@app.cell
def _(daily):
    x_top = float(daily.Humidity.max() + 5)
    y_top = float(daily.Zone1.max() + 5000)
    print("humidity top:", round(x_top, 2))
    print("power top:", round(y_top, 2))
    return x_top, y_top


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The worked example keeps months 1, 2, and 3. Both ends are included.
    """)
    return


@app.cell
def _(daily):
    first_quarter = daily[(1 <= daily["month"]) & (daily["month"] <= 3)]
    print(len(first_quarter))
    return (first_quarter,)


@app.cell
def _(first_quarter, px, x_top, y_top):
    _fig = px.scatter(
        first_quarter,
        x="Humidity",
        y=["Zone1", "Zone2", "Zone3"],
        color_discrete_sequence=["orangered", "darkorange", "seagreen"],
        hover_name="variable",
        hover_data={"variable": None, "value": ":.2f", "Humidity": ":.2f"},
        labels={"variable": "Zone", "value": "Power consumption"},
        title="January through March",
    )
    _fig.update_xaxes(range=[0, x_top])
    _fig.update_yaxes(range=[0, y_top])
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    January, February, and March have 90 days in this file. 2017 is not a leap year, and 31 December is absent, so those three months are complete.

    ## The Dash page

    `dcc.RangeSlider` sits under the graph. `value=[1, 3]` is the starting pair. The callback reads that pair with `min` and `max`, so the order of the two handles does not matter.

    ```python
    dcc.RangeSlider(
        id="range-slider",
        min=1,
        max=12,
        step=1,
        value=[1, 3],
        marks={1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"},
    )

    @dash_app.callback(
        Output("power-scatter", "figure"),
        Input("range-slider", "value"),
    )
    def update_graph(selected_span):
        low = min(selected_span)
        high = max(selected_span)
        filtered = daily[(low <= daily["month"]) & (daily["month"] <= high)]
        figure = px.scatter(
            filtered,
            x="Humidity",
            y=["Zone1", "Zone2", "Zone3"],
            color_discrete_sequence=["orangered", "darkorange", "seagreen"],
            hover_name="variable",
            hover_data={"variable": None, "value": ":.2f", "Humidity": ":.2f"},
            labels={"variable": "Zone", "value": "Power consumption"},
        )
        figure.update_xaxes(range=[0, x_top])
        figure.update_yaxes(range=[0, y_top])
        return figure
    ```

    The range slider below starts at the same pair.
    """)
    return


@app.cell
def _(mo):
    month_span = mo.ui.range_slider(
        start=1,
        stop=12,
        step=1,
        value=[1, 3],
        show_value=True,
        label="Months",
        full_width=True,
    )
    month_span
    return (month_span,)


@app.cell
def _(daily, month_span, px, x_top, y_top):
    _low = int(min(month_span.value))
    _high = int(max(month_span.value))
    _rows = daily[(_low <= daily["month"]) & (daily["month"] <= _high)]
    _fig = px.scatter(
        _rows,
        x="Humidity",
        y=["Zone1", "Zone2", "Zone3"],
        color_discrete_sequence=["orangered", "darkorange", "seagreen"],
        hover_name="variable",
        hover_data={"variable": None, "value": ":.2f", "Humidity": ":.2f"},
        labels={"variable": "Zone", "value": "Power consumption"},
        title=f"Months {_low} through {_high}",
    )
    _fig.update_xaxes(range=[0, x_top])
    _fig.update_yaxes(range=[0, y_top])
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The starting value is `[1, 3]`. Are the end months included in the filter?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Yes.** The test is `low <= month <= high`. Months 1, 2, and 3 are all kept. That is 90 days.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - A range slider returns two month numbers. The daily rows between those months are kept, including both ends.
    - The scatter plot uses humidity and the three zone columns. The axis limits come from the whole year.
    - January through March is 90 days in this file.
    - In Dash, `dcc.RangeSlider` is the only callback input. The control in this file returns the same pair of months.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does the range slider's value contain?
    2. Why does the callback take `min` and `max` of that pair?
    3. How many days are in months 1 through 3 here?
    4. Which column is on the horizontal axis?
    5. Where do the axis limits come from?
    6. What is the id of the Dash graph?
    7. Does the filter drop the months that sit strictly between the handles?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **Two month numbers:** The starting pair is 1 and 3.
2. **The handles can sit in either order:** The lower number is the start month and the higher number is the end month.
3. **90:** January, February, and March of 2017 are complete in this file.
4. **Humidity:** Power in the three zones is on the vertical axis.
5. **The whole year:** The horizontal top is the largest daily humidity plus 5. The vertical top is Zone 1's largest daily power plus 5,000.
6. **`power-scatter`:** The callback writes its figure property.
7. **No:** Every month from the low handle through the high handle is kept.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash range slider.* https://dash.plotly.com/dash-core-components/rangeslider
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
