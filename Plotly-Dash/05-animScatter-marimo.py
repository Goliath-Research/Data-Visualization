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
    import plotly.graph_objects as go

    return go, mo, pd, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Animated Scatter Plots and Custom Buttons

    ## Objectives

    - Average the Tetouan readings by day, drop 1 January, and draw power against temperature with one frame per month.
    - Use wind speed as the point size and the point color, then stack the three zones into one scatter plot.
    - Add buttons that switch a chart between a box and a violin, and buttons that show temperature, humidity, or both.

    ## Background

    `animation_frame` splits the points into frames and adds a slider under the figure. Fixed `range_x` and `range_y` keep the scale the same in every month, so a point in July can be compared with a point in January.

    Buttons live in the figure layout, in `updatemenus`. The `method` says what a click is allowed to change:

    - `restyle` changes the traces, such as the trace type.
    - `update` changes the traces and the layout together. The example uses it to hide a line and set the title.

    ## Datasets Used

    - **Power consumption of Tetouan city**, from the UCI Machine Learning Repository. Three zones in Tetouan, Morocco, in 2017. Salam and El Hibaoui collected the readings.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are 52,416 rows, one every 10 minutes, from 1 January 2017 through 30 December 2017. The zone names are shortened to `Zone1`, `Zone2`, and `Zone3`.
    """)
    return


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
    print("missing values:", int(power.isnull().sum().sum()))
    return (power,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One row per day

    A daily mean has 364 rows, from 1 January through 30 December. 1 January belongs to ISO week 52 of 2016, so that day is dropped. 363 days remain, and the first of them is 2 January, ISO week 1.
    """)
    return


@app.cell
def _(pd, power):
    daily_all = (
        power.groupby(pd.Grouper(key="DateTime", freq="D"))
        .mean(numeric_only=True)
        .reset_index()
    )
    daily_all = daily_all.assign(
        Week=daily_all.DateTime.dt.isocalendar().week.astype(int),
        Month=daily_all.DateTime.dt.month.astype(int),
    )
    print(daily_all.shape)
    print(daily_all.loc[0, "DateTime"], "week", int(daily_all.loc[0, "Week"]))
    return (daily_all,)


@app.cell
def _(daily_all):
    daily = daily_all.iloc[1:].reset_index(drop=True)
    print(daily.shape)
    print(daily["DateTime"].iloc[0], "week", int(daily["Week"].iloc[0]))
    return (daily,)


@app.cell
def _(daily, mo):
    mo.Html(daily.head(3).to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Power against temperature

    Each point is one day in Zone 1. The January chart is a single month. The animated chart uses every month, with the same axis ranges, so the cloud can be compared from month to month.
    """)
    return


@app.cell
def _(daily, px):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone1",
        width=800,
        height=500,
        title="Temperature and Zone 1 power",
    )
    return _fig


@app.cell
def _(daily, px):
    _fig = px.scatter(
        daily[daily["Month"] == 1],
        x="Temperature",
        y="Zone1",
        range_x=[5, 35],
        range_y=[26000, 40000],
        width=800,
        height=500,
        title="Zone 1 in January",
    )
    return _fig


@app.cell
def _(daily, px):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone1",
        animation_frame="Month",
        range_x=[5, 35],
        range_y=[26000, 40000],
        width=800,
        height=500,
        title="Zone 1 by month",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `size` makes a windier day a larger point. `color` uses the same wind speed, and `range_color` is the smallest and largest daily wind speed in the table, so the colors mean the same thing in every month.
    """)
    return


@app.cell
def _(daily):
    wind_min = float(daily["Wind Speed"].min())
    wind_max = float(daily["Wind Speed"].max())
    print(round(wind_min, 3), round(wind_max, 3))
    return wind_max, wind_min


@app.cell
def _(daily, px):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone1",
        animation_frame="Month",
        size="Wind Speed",
        range_x=[5, 35],
        range_y=[26000, 40000],
        width=800,
        height=500,
        title="Zone 1, point size is wind speed",
    )
    return _fig


@app.cell
def _(daily, px, wind_max, wind_min):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone1",
        animation_frame="Month",
        size="Wind Speed",
        color="Wind Speed",
        range_color=[wind_min, wind_max],
        color_continuous_scale="spectral",
        range_x=[5, 35],
        range_y=[26000, 40000],
        width=800,
        height=500,
        title="Zone 1, color is wind speed",
    )
    return _fig


@app.cell
def _(daily, px, wind_max, wind_min):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone2",
        animation_frame="Month",
        size="Wind Speed",
        color="Wind Speed",
        range_color=[wind_min, wind_max],
        color_continuous_scale="spectral",
        range_x=[5, 35],
        range_y=[12000, 30000],
        width=800,
        height=500,
        title="Zone 2 by month",
    )
    return _fig


@app.cell
def _(daily, px, wind_max, wind_min):
    _fig = px.scatter(
        daily,
        x="Temperature",
        y="Zone3",
        animation_frame="Month",
        size="Wind Speed",
        color="Wind Speed",
        range_color=[wind_min, wind_max],
        color_continuous_scale="spectral",
        range_x=[5, 35],
        range_y=[5000, 40000],
        width=800,
        height=500,
        title="Zone 3 by month",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### All three zones

    `melt` stacks the three zone columns. `color="Zone"` gives each zone its own color. The vertical range runs from 5,000 to 40,000 so all three zones fit on one scale.
    """)
    return


@app.cell
def _(daily):
    daily_zones = daily.melt(
        id_vars=["Week", "Month", "Temperature", "Wind Speed"],
        value_vars=["Zone1", "Zone2", "Zone3"],
    )
    daily_zones = daily_zones.rename(columns={"variable": "Zone", "value": "Power"})
    print(daily_zones.shape)
    return (daily_zones,)


@app.cell
def _(daily_zones, px):
    _fig = px.scatter(
        daily_zones,
        x="Temperature",
        y="Power",
        animation_frame="Month",
        size="Wind Speed",
        color="Zone",
        range_x=[5, 35],
        range_y=[5000, 40000],
        width=800,
        height=500,
        title="Three zones by month",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `animation_frame` is `"Month"`. What do the points in a single frame have in common?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**The same month.** Each frame keeps the days whose `Month` equals the slider value. The axis ranges do not change with the frame.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Buttons that restyle the traces

    A box and a violin of the same three zones are drawn first, as separate figures. The button chart starts as three boxes. `method="restyle"` with `args=["type", "violin"]` changes the trace type. A second menu uses `type="dropdown"` for the same two choices.
    """)
    return


@app.cell
def _(daily_zones, px):
    _fig = px.box(
        daily_zones,
        x="Zone",
        y="Power",
        color="Zone",
        width=800,
        title="Power by zone",
    )
    return _fig


@app.cell
def _(daily_zones, px):
    _fig = px.violin(
        daily_zones,
        x="Zone",
        y="Power",
        color="Zone",
        width=800,
        title="Power by zone",
    )
    return _fig


@app.cell
def _(daily, go):
    box_buttons = go.Figure()
    box_buttons.add_trace(go.Box(y=daily.Zone1, name="Zone 1"))
    box_buttons.add_trace(go.Box(y=daily.Zone2, name="Zone 2"))
    box_buttons.add_trace(go.Box(y=daily.Zone3, name="Zone 3"))
    box_buttons.update_layout(
        width=800,
        title="Box or violin",
        updatemenus=[
            go.layout.Updatemenu(
                type="buttons",
                direction="up",
                showactive=True,
                buttons=[
                    dict(args=["type", "box"], label="Box", method="restyle"),
                    dict(args=["type", "violin"], label="Violin", method="restyle"),
                ],
            )
        ],
    )
    return box_buttons


@app.cell
def _(daily, go):
    box_menu = go.Figure()
    box_menu.add_trace(go.Box(y=daily.Zone1, name="Zone 1"))
    box_menu.add_trace(go.Box(y=daily.Zone2, name="Zone 2"))
    box_menu.add_trace(go.Box(y=daily.Zone3, name="Zone 3"))
    box_menu.update_layout(
        width=800,
        title="Box or violin",
        updatemenus=[
            go.layout.Updatemenu(
                type="dropdown",
                direction="down",
                showactive=True,
                buttons=[
                    dict(args=["type", "box"], label="Box", method="restyle"),
                    dict(args=["type", "violin"], label="Violin", method="restyle"),
                ],
            )
        ],
    )
    return box_menu


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Buttons that update the layout

    The lines are weekly means, so each date and each temperature come from the same weekly row. There are 51 weeks after ISO week 52 is dropped.

    Both lines are drawn. Each button sets `visible` to a pair of true or false values, one per trace, and sets the title in the same click. That is `method="update"`, because the click changes the data and the layout.
    """)
    return


@app.cell
def _(pd, power):
    weekly_all = (
        power.groupby(pd.Grouper(key="DateTime", freq="7D"))
        .mean(numeric_only=True)
        .reset_index()
    )
    weekly_all = weekly_all.assign(
        Week=weekly_all.DateTime.dt.isocalendar().week.astype(int)
    )
    weekly = weekly_all.iloc[1:].reset_index(drop=True)
    print(weekly.shape)
    return (weekly,)


@app.cell
def _(go, weekly):
    weather_lines = go.Figure()
    weather_lines.add_trace(
        go.Scatter(
            x=weekly.DateTime,
            y=weekly.Temperature,
            name="Temperature",
            line=dict(color="#F06A6A"),
        )
    )
    weather_lines.add_trace(
        go.Scatter(
            x=weekly.DateTime,
            y=weekly.Humidity,
            name="Humidity",
            line=dict(color="#9999FF"),
        )
    )
    weather_lines.update_layout(
        width=800,
        title="Temperature and humidity in Tetouan, 2017",
        updatemenus=[
            go.layout.Updatemenu(
                type="buttons",
                direction="down",
                buttons=[
                    dict(
                        label="Temperature",
                        method="update",
                        args=[{"visible": [True, False]}, {"title": "Temperature"}],
                    ),
                    dict(
                        label="Humidity",
                        method="update",
                        args=[{"visible": [False, True]}, {"title": "Humidity"}],
                    ),
                    dict(
                        label="Both",
                        method="update",
                        args=[
                            {"visible": [True, True]},
                            {"title": "Temperature and humidity in Tetouan, 2017"},
                        ],
                    ),
                ],
            )
        ],
    )
    return weather_lines


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The Humidity button uses `visible: [False, True]`. Which line stays on the chart?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Humidity.** The first flag belongs to the first trace, temperature. The second flag belongs to humidity.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - Daily means cover 364 days. Dropping 1 January leaves 363 days, starting on 2 January.
    - `animation_frame="Month"` shows one month at a time. The axis ranges are fixed. Wind speed controls the point size, and on the later charts it also controls the color.
    - Zone 1 uses a vertical range of 26,000 to 40,000, Zone 2 uses 12,000 to 30,000, and Zone 3 uses 5,000 to 40,000. The combined chart uses 5,000 to 40,000.
    - `restyle` changes the trace type between box and violin. `update` sets which weekly line is visible and changes the title in the same click.
    - The weekly lines have 51 points. The date, the temperature, and the humidity all come from that weekly table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. Why is 1 January removed from the daily table?
    2. What does a fixed `range_y` do when the month frame changes?
    3. Which column sets both the size and the color of the Zone 1 points?
    4. How many rows does the three-zone table have?
    5. What is the difference between `restyle` and `update` in these menus?
    6. What does `visible: [True, False]` show?
    7. Why do the temperature and humidity lines use the weekly table for both `x` and `y`?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **ISO week 52:** 1 January 2017 belongs to the last week of 2016. The next day, 2 January, is ISO week 1.
2. **The scale stays put:** A high day in July is drawn on the same axis as a high day in January.
3. **`Wind Speed`:** `size` and `color` both use that column. `range_color` is the minimum and maximum daily wind speed.
4. **1,089:** 363 days times 3 zones.
5. **Traces, or traces plus layout:** `restyle` switches the type of the existing traces. `update` also sets the title.
6. **Temperature only:** The flags follow the order of the traces. Temperature is first.
7. **Each point is one week:** The date and the two measurements have to be the same length and the same row. The weekly table has 51 rows after week 52 is dropped.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Plotly Express in Python.* https://plotly.com/python/plotly-express/
    - Plotly. *Custom buttons in Python.* https://plotly.com/python/custom-buttons/
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
