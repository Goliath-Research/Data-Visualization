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
    # A Slider for the Month

    ## Objectives

    - Add a month number to the daily Tetouan table.
    - Draw temperature against the three zone powers for one month, on axes that stay fixed.
    - Choose the month with a slider. In Dash the slider is vertical and starts at March. The slider below does the same filtering in this file.

    ## Background

    `dcc.Slider` runs from the smallest month to the largest, with a step of 1. `marks` labels the twelve months. `included=False` leaves the track unfilled. The callback receives the selected month and keeps the daily rows for that month.

    The horizontal axis runs from 0 to the largest daily temperature plus 5. The vertical axis runs from 0 to Zone 1's largest daily power plus 5,000. Those limits use the whole year, so March and August share one scale.

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
    month_names = (
        "",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    )
    return month_names, power_file


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
    print("months:", int(daily["month"].min()), "to", int(daily["month"].max()))
    return (daily,)


@app.cell
def _(daily):
    x_top = float(daily.Temperature.max() + 5)
    y_top = float(daily.Zone1.max() + 5000)
    print("temperature top:", round(x_top, 2))
    print("power top:", round(y_top, 2))
    return x_top, y_top


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    January is the worked example. Passing a list of zone names to `y` draws one series per zone. The hover names the zone and formats the power and the temperature.
    """)
    return


@app.cell
def _(daily, px, x_top, y_top):
    _january = daily[daily["month"] == 1]
    _fig = px.scatter(
        _january,
        x="Temperature",
        y=["Zone1", "Zone2", "Zone3"],
        color_discrete_sequence=["orangered", "darkorange", "seagreen"],
        hover_name="variable",
        hover_data={"variable": None, "value": ":.2f", "Temperature": ":.2f"},
        labels={"variable": "Zone", "value": "Power consumption"},
        title="January",
    )
    _fig.update_xaxes(range=[0, x_top])
    _fig.update_yaxes(range=[0, y_top])
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dash page

    The slider is vertical, from 1 to 12, and it starts at 3 (March). The graph id is `power-scatter`.

    ```python
    dcc.Slider(
        id="month-slider",
        min=1,
        max=12,
        step=1,
        value=3,
        included=False,
        vertical=True,
        marks={1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
               7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"},
    )

    @dash_app.callback(
        Output("power-scatter", "figure"),
        Input("month-slider", "value"),
    )
    def update_graph(selected_month):
        filtered = daily[daily["month"] == selected_month]
        figure = px.scatter(
            filtered,
            x="Temperature",
            y=["Zone1", "Zone2", "Zone3"],
            color_discrete_sequence=["orangered", "darkorange", "seagreen"],
            hover_name="variable",
            hover_data={"variable": None, "value": ":.2f", "Temperature": ":.2f"},
            labels={"variable": "Zone", "value": "Power consumption"},
        )
        figure.update_xaxes(range=[0, x_top])
        figure.update_yaxes(range=[0, y_top])
        return figure
    ```

    The slider below is vertical and starts at March.
    """)
    return


@app.cell
def _(mo):
    month_choice = mo.ui.slider(
        start=1,
        stop=12,
        step=1,
        value=3,
        orientation="vertical",
        show_value=True,
        label="Month",
    )
    return (month_choice,)


@app.cell
def _(daily, month_choice, month_names, px, x_top, y_top):
    _month = int(month_choice.value)
    _rows = daily[daily["month"] == _month]
    _fig = px.scatter(
        _rows,
        x="Temperature",
        y=["Zone1", "Zone2", "Zone3"],
        color_discrete_sequence=["orangered", "darkorange", "seagreen"],
        hover_name="variable",
        hover_data={"variable": None, "value": ":.2f", "Temperature": ":.2f"},
        labels={"variable": "Zone", "value": "Power consumption"},
        title=month_names[_month],
    )
    _fig.update_xaxes(range=[0, x_top])
    _fig.update_yaxes(range=[0, y_top])
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The slider starts at 3. Which month is that?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**March.** The month numbers run from 1 to 12. The chart title uses that name, and the points are the days of that month.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - Each daily row has a `month` from 1 to 12. The scatter plot keeps the rows for the selected month and draws Zone 1, Zone 2, and Zone 3 against temperature.
    - The axis limits come from the whole year: temperature plus 5, and Zone 1's power plus 5,000.
    - The Dash slider is vertical, starts at 3, and does not fill the track. Its value is the only callback input.
    - The slider in this file is the same control. The title is the month name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. What does the slider value select in the daily table?
    2. Which month is the value 3?
    3. Why do the axis limits use the whole year rather than the selected month?
    4. Which three columns are passed as `y`?
    5. What does `included=False` mean on the Dash slider?
    6. What is the callback input?
    7. Which color is Zone 1?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **One month of days:** The filter is `daily["month"] == selected_month`.
2. **March:** January is 1 and the names follow the calendar.
3. **So the months share a scale:** A hot day in August is plotted on the same axes as a cool day in January.
4. **`Zone1`, `Zone2`, and `Zone3`:** Each column is one series of daily power.
5. **The track is not filled:** The mark shows the chosen month, and the bar does not paint the span from the minimum.
6. **`month-slider`:** The callback reads its `value` and returns the figure for `power-scatter`.
7. **Orange-red:** The color list is orange-red, dark orange, then sea green.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash slider.* https://dash.plotly.com/dash-core-components/slider
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
