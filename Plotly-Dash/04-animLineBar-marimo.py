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
    # Animated Line and Bar Charts

    ## Objectives

    - Read the Tetouan power file, name the three zone columns, and check that it has no missing values.
    - Average the readings by week, drop the row that falls in ISO week 52, and build a growing line with `animation_frame`.
    - Draw the three zone averages as animated bars, one frame per week and one frame per month.

    ## Background

    An animated chart is a stack of frames. `animation_frame` names the column that chooses the frame. Plotly adds a slider and a play button under the figure.

    A line that grows needs a row for every point that should be visible in that frame. The column `weekUntil` marks those copies. In the frame for week 3, the line contains weeks 1, 2, and 3.

    A bar chart can use the week number itself as the frame. Each frame shows only that week's three bars.

    ## Datasets Used

    - **Power consumption of Tetouan city**, from the UCI Machine Learning Repository. Three distribution zones in Tetouan, Morocco, in 2017, with temperature, humidity, wind speed, and diffuse flows. Salam and El Hibaoui collected the readings.
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
def _(mo, power_raw):
    mo.Html(power_raw.head(3).to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The file has 52,416 rows and 9 columns. The rows run from 1 January 2017 at 00:00 through 30 December 2017 at 23:50, one row every 10 minutes. December 31 is not in the file. There are no missing values.

    Two of the original zone names contain a double space. The new names are `Zone1`, `Zone2`, and `Zone3`. `diffuse flows` becomes `Diffuse Flows`.
    """)
    return


@app.cell
def _(power_raw):
    print("missing values:", int(power_raw.isnull().sum().sum()))
    return


@app.cell
def _(pd, power_raw):
    power = power_raw.rename(
        columns={
            "Zone 1 Power Consumption": "Zone1",
            "Zone 2  Power Consumption": "Zone2",
            "Zone 3  Power Consumption": "Zone3",
            "diffuse flows": "Diffuse Flows",
        }
    )
    power = power.assign(DateTime=pd.to_datetime(power["DateTime"]))
    print(power["DateTime"].min())
    print(power["DateTime"].max())
    return (power,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One row per week

    `Grouper` with `freq="7D"` averages each numeric column inside a 7-day bin. The first bin is dated 1 January 2017.

    ISO weeks start on Monday. Thursday is the middle of an ISO week, so 1 January 2017, a Sunday, belongs to week 52 of 2016. That row is removed. The table then starts on 8 January, which is ISO week 1, and ends on 24 December, ISO week 51. 51 weeks remain.
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
    print(weekly_all.shape)
    print(weekly_all.loc[0, "DateTime"], "week", int(weekly_all.loc[0, "Week"]))
    return (weekly_all,)


@app.cell
def _(weekly_all):
    weekly = weekly_all.iloc[1:].reset_index(drop=True)
    print(weekly.shape)
    print(weekly["DateTime"].iloc[0], "week", int(weekly["Week"].iloc[0]))
    print(weekly["DateTime"].iloc[-1], "week", int(weekly["Week"].iloc[-1]))
    return (weekly,)


@app.cell
def _(mo, weekly):
    mo.Html(weekly.head(3).to_html())
    return


@app.cell
def _(px, weekly):
    _fig = px.line(
        weekly,
        x="DateTime",
        y="Temperature",
        width=800,
        title="Weekly temperature in Tetouan, 2017",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A line that grows

    For each week number `w`, copy the rows whose week is `w` or earlier, and mark those copies with `weekUntil = w`.

    - Week 1 contributes 1 row, with `weekUntil` 1.
    - Week 2 contributes 2 rows, with `weekUntil` 2.
    - Week 51 contributes 51 rows, with `weekUntil` 51.

    The total is 1 + 2 + ... + 51 = 1,326 rows. `animation_frame="weekUntil"` plays those copies in order. `range_x` and `range_y` stay fixed so the axes do not jump.
    """)
    return


@app.cell
def _(pd, weekly):
    pieces = []
    for week in weekly.Week.unique():
        rows = weekly.loc[weekly.Week <= week].copy()
        rows["weekUntil"] = int(week)
        pieces.append(rows)
    weekly_anim = pd.concat(pieces, ignore_index=True)
    print(weekly_anim.shape)
    return (weekly_anim,)


@app.cell
def _(px, weekly_anim):
    _fig = px.line(
        weekly_anim,
        x="DateTime",
        y="Temperature",
        range_x=["2017-01-01", "2017-12-24"],
        range_y=[5, 35],
        animation_frame="weekUntil",
        width=800,
        title="Weekly temperature, growing by week",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Temperature, humidity, and diffuse flows share one vertical axis in the next chart. Humidity and diffuse flows are much larger than temperature, so the scale runs to 150 and the temperature line sits near the bottom.
    """)
    return


@app.cell
def _(px, weekly_anim):
    _fig = px.line(
        weekly_anim,
        x="DateTime",
        y=["Temperature", "Humidity", "Diffuse Flows"],
        range_x=["2017-01-01", "2017-12-24"],
        range_y=[5, 150],
        animation_frame="weekUntil",
        width=800,
        title="Temperature, humidity, and diffuse flows",
    )
    return _fig


@app.cell
def _(px, weekly_anim):
    _fig = px.line(
        weekly_anim,
        x="DateTime",
        y=["Temperature", "Humidity", "Diffuse Flows"],
        range_x=["2017-01-01", "2017-12-24"],
        range_y=[5, 150],
        animation_frame="weekUntil",
        hover_data={"DateTime": False, "weekUntil": False, "value": ":.2f"},
        width=800,
        title="Shared hover at each date",
    )
    _fig.update_layout(hovermode="x unified")
    return _fig


@app.cell
def _(px, weekly_anim):
    _fig = px.line(
        weekly_anim,
        x="DateTime",
        y=["Zone1", "Zone2", "Zone3"],
        color_discrete_map={"Zone1": "salmon", "Zone2": "dodgerblue", "Zone3": "grey"},
        range_x=["2017-01-01", "2017-12-24"],
        range_y=[5, 40000],
        animation_frame="weekUntil",
        hover_data={"DateTime": False, "weekUntil": False, "value": ":.2f"},
        width=800,
        title="Weekly power by zone",
    )
    _fig.update_layout(hovermode="x unified")
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The animation table has one copy of the early weeks for every later frame. How many rows does `weekly_anim` have?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**1,326 rows.** There are 51 weeks, and the row count is 1 + 2 + ... + 51.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Animated bars

    `melt` stacks `Zone1`, `Zone2`, and `Zone3` into one `Power` column. `animation_frame="Week"` shows one week at a time. `range_color` uses the largest power in the whole table, so the color of a bar means the same thing in every frame.
    """)
    return


@app.cell
def _(weekly):
    weekly_zones = weekly.melt(
        id_vars=["Week", "Temperature"],
        value_vars=["Zone1", "Zone2", "Zone3"],
    )
    weekly_zones = weekly_zones.rename(columns={"variable": "Zone", "value": "Power"})
    print(weekly_zones.head(3))
    return (weekly_zones,)


@app.cell
def _(px, weekly_zones):
    _max_power = weekly_zones.Power.max()
    _fig = px.bar(
        weekly_zones,
        x="Zone",
        y="Power",
        color="Power",
        color_continuous_scale="portland",
        range_color=[0, _max_power],
        animation_frame="Week",
        animation_group="Zone",
        range_y=[0, _max_power],
        hover_data={"Zone": False, "Power": ":.2f"},
        width=800,
        title="Power by zone, one week at a time",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The same bars by month use `freq="ME"`, the month-end bin. Twelve months remain, numbered 1 through 12.
    """)
    return


@app.cell
def _(pd, power):
    monthly = (
        power.groupby(pd.Grouper(key="DateTime", freq="ME"))
        .mean(numeric_only=True)
        .reset_index()
    )
    monthly = monthly.assign(Month=monthly.DateTime.dt.month.astype(int))
    print(monthly.shape)
    return (monthly,)


@app.cell
def _(monthly):
    monthly_zones = monthly.melt(
        id_vars=["Month"],
        value_vars=["Zone1", "Zone2", "Zone3"],
    )
    monthly_zones = monthly_zones.rename(columns={"variable": "Zone", "value": "Power"})
    print(monthly_zones.head(3))
    return (monthly_zones,)


@app.cell
def _(monthly_zones, px):
    _max_power = monthly_zones.Power.max()
    _fig = px.bar(
        monthly_zones,
        x="Zone",
        y="Power",
        color="Power",
        color_continuous_scale="spectral",
        range_color=[0, _max_power],
        animation_frame="Month",
        animation_group="Zone",
        range_y=[0, _max_power],
        hover_data={"Zone": False, "Power": ":.2f"},
        width=800,
        title="Power by zone, one month at a time",
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    Why is the 1 January weekly row left out of `weekly`?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**It is ISO week 52.** 1 January 2017 falls in the last week of 2016. The animated weeks are 1 through 51.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The Tetouan file has 52,416 rows, one every 10 minutes, from 1 January through 30 December 2017. None of those values are missing.
    - Weekly means produce 52 bins. The first bin is ISO week 52 and is dropped. 51 weeks remain, from 8 January (week 1) through 24 December (week 51).
    - `weekUntil` copies every earlier week into the current frame, which is 1,326 rows. The line grows because later frames contain more dates. The axes stay fixed.
    - Temperature, humidity, and diffuse flows share one scale that runs to 150, so the temperature line sits low. The zone lines use a scale that runs to 40,000.
    - The bar frames show one week, or one month, at a time. The color scale is fixed to the largest power in that table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How often is a row recorded in the Tetouan file, and which day is missing?
    2. Why is the first weekly average labeled week 52?
    3. What does one value of `weekUntil` contain?
    4. Why does the temperature line look small when humidity is on the same chart?
    5. What does `hovermode="x unified"` change?
    6. Why is `range_color` set from the maximum of the whole bar table?
    7. How many frames does the monthly bar chart have?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **Every 10 minutes:** The file runs from 1 January 2017 through 30 December 2017. December 31 is not included.
2. **ISO weeks start on Monday:** 1 January 2017 is a Sunday in the last ISO week of 2016.
3. **That week and every earlier week:** Frame 3 holds the weekly rows for weeks 1, 2, and 3, each marked with `weekUntil` 3.
4. **One shared scale:** Humidity and diffuse flows are much larger than temperature. The axis runs to 150, and temperature stays near the bottom.
5. **One tooltip for the date:** The hover lists every series at that x position, instead of one series at a time.
6. **So the colors do not change meaning:** A given shade of the scale is the same power in week 1 and in week 51.
7. **12:** There is one month-end average for each month of 2017.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Plotly Express in Python.* https://plotly.com/python/plotly-express/
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
