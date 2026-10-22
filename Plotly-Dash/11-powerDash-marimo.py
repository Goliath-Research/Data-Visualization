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
    # Power Consumption Dashboard

    ## Objectives

    - Filter the daily Tetouan table to one month and to a list of zones.
    - Draw three scatter plots for that selection: power against temperature, humidity, and wind speed.
    - Wire both choices into one Dash callback with two inputs and three outputs. The checklist and the slider below apply the same filter in this file.

    ## Background

    The page has a checklist of zones and a month slider on one row, then a horizontal rule, then three graphs. In Dash, `display: inline-block` and a width on each component place them side by side. The checklist is about 20% of the row and the slider about 67%. Each graph is about 28% of the next row.

    One callback receives the month and the list of checked zones. It returns three figures, in the same order as the three `Output` lines.

    The program that serves this page is `power_dash.py` in this folder. Running that file opens http://127.0.0.1:8050/. This lesson does not start that program.

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
    zone_order = ["Zone1", "Zone2", "Zone3"]
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
    return month_names, power_file, zone_order


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
    daily = daily.assign(Month=daily.DateTime.dt.month.astype(int))
    print(daily.shape)
    return (daily,)


@app.cell
def _(daily, mo):
    mo.Html(daily.head(3).to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    January has 31 days. The worked example draws Zone 1 and Zone 3. The selection is a list of names. A name is kept when it is in that list.
    """)
    return


@app.cell
def _(daily):
    january = daily[daily["Month"] == 1]
    print(len(january))
    return (january,)


@app.cell
def _(zone_order):
    example_zones = ["Zone1", "Zone3"]
    zones = [zone for zone in zone_order if zone in example_zones]
    print(zones)
    return (zones,)


@app.cell
def _(january, px, zones):
    _fig = px.scatter(
        january,
        x="Temperature",
        y=zones,
        hover_data={"Temperature": ":.2f", "value": ":.2f"},
        width=800,
        title="January, temperature",
    )
    _fig
    return _fig


@app.cell
def _(january, px, zones):
    _fig = px.scatter(
        january,
        x="Humidity",
        y=zones,
        hover_data={"Humidity": ":.2f", "value": ":.2f"},
        width=800,
        title="January, humidity",
    )
    _fig
    return _fig


@app.cell
def _(january, px, zones):
    _fig = px.scatter(
        january,
        x="Wind Speed",
        y=zones,
        hover_data={"Wind Speed": ":.2f", "value": ":.2f"},
        width=800,
        title="January, wind speed",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dash page

    The callback lists three outputs and two inputs. The function arguments follow the input order: month first, then the checked zones.

    ```python
    @dash_app.callback(
        Output("fig-s1", "figure"),
        Output("fig-s2", "figure"),
        Output("fig-s3", "figure"),
        Input("month-slider", "value"),
        Input("zone-check", "value"),
    )
    def update_graphs(selected_month, selected_zones):
        rows = daily[daily["Month"] == selected_month]
        zones = [zone for zone in ["Zone1", "Zone2", "Zone3"] if zone in selected_zones]
        temperature = px.scatter(
            rows, x="Temperature", y=zones,
            hover_data={"Temperature": ":.2f", "value": ":.2f"},
            title="Temperature vs power consumption",
        )
        humidity = px.scatter(
            rows, x="Humidity", y=zones,
            hover_data={"Humidity": ":.2f", "value": ":.2f"},
            title="Humidity vs power consumption",
        )
        wind = px.scatter(
            rows, x="Wind Speed", y=zones,
            hover_data={"Wind Speed": ":.2f", "value": ":.2f"},
            title="Wind speed vs power consumption",
        )
        return temperature, humidity, wind
    ```

    `power_dash.py` is that program, including the layout. Its server uses the default address, http://127.0.0.1:8050/.

    The checklist and the slider below feed the three figures in this file.
    """)
    return


@app.cell
def _(mo, zone_order):
    zone_pick = mo.ui.multiselect(
        options=zone_order,
        value=zone_order,
        label="Zones",
    )
    zone_pick
    return (zone_pick,)


@app.cell
def _(mo):
    month_choice = mo.ui.slider(
        start=1,
        stop=12,
        step=1,
        value=1,
        show_value=True,
        label="Month",
        full_width=True,
    )
    month_choice
    return (month_choice,)


@app.cell
def _(daily, month_choice, month_names, px, zone_order, zone_pick):
    _month = int(month_choice.value)
    _rows = daily[daily["Month"] == _month]
    _zones = [zone for zone in zone_order if zone in zone_pick.value]
    _title = f"{month_names[_month]}, temperature"
    if len(_zones) == 0:
        _fig = px.scatter(title="Select at least one zone")
    else:
        _fig = px.scatter(
            _rows,
            x="Temperature",
            y=_zones,
            hover_data={"Temperature": ":.2f", "value": ":.2f"},
            title=_title,
        )
    _fig
    return _fig


@app.cell
def _(daily, month_choice, month_names, px, zone_order, zone_pick):
    _month = int(month_choice.value)
    _rows = daily[daily["Month"] == _month]
    _zones = [zone for zone in zone_order if zone in zone_pick.value]
    _title = f"{month_names[_month]}, humidity"
    if len(_zones) == 0:
        _fig = px.scatter(title="Select at least one zone")
    else:
        _fig = px.scatter(
            _rows,
            x="Humidity",
            y=_zones,
            hover_data={"Humidity": ":.2f", "value": ":.2f"},
            title=_title,
        )
    _fig
    return _fig


@app.cell
def _(daily, month_choice, month_names, px, zone_order, zone_pick):
    _month = int(month_choice.value)
    _rows = daily[daily["Month"] == _month]
    _zones = [zone for zone in zone_order if zone in zone_pick.value]
    _title = f"{month_names[_month]}, wind speed"
    if len(_zones) == 0:
        _fig = px.scatter(title="Select at least one zone")
    else:
        _fig = px.scatter(
            _rows,
            x="Wind Speed",
            y=_zones,
            hover_data={"Wind Speed": ":.2f", "value": ":.2f"},
            title=_title,
        )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The worked example uses `["Zone1", "Zone3"]`. How many zones does the filter keep, and in what order?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Two zones, Zone 1 then Zone 3.** The order comes from `zone_order`. Zone 2 is not in the example list, so it is left out.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - One month and a list of zones select the points. January is 31 days. The example list draws Zone 1 and Zone 3, in that order.
    - The three charts share that filter. The horizontal variable is temperature, humidity, or wind speed.
    - The Dash callback has two inputs and returns three figures. `power_dash.py` serves that page at http://127.0.0.1:8050/.
    - The checklist and the month slider in this file apply the same two filters to the three scatter plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How many inputs and outputs does the callback have?
    2. Which argument of `update_graphs` is the month?
    3. What does the example list `["Zone1", "Zone3"]` leave out?
    4. How many days does January contribute?
    5. What is different among the three scatter plots?
    6. Where does `power_dash.py` serve the page?
    7. What do the three figures do when the month slider moves?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **Two inputs and three outputs:** The inputs are the month slider and the checklist. The outputs are the three graph figures.
2. **The first argument:** The `Input` lines list the slider before the checklist, and the function arguments follow that order.
3. **Zone 2:** Only names in the list are drawn, and they stay in Zone 1, Zone 2, Zone 3 order.
4. **31:** The daily table includes every day of January 2017.
5. **The horizontal column:** Temperature, humidity, and wind speed. The month and the zones are the same.
6. **http://127.0.0.1:8050/:** That file starts the Dash server on the default port.
7. **They all use the new month:** Each figure filters `daily` with the same slider value and the same checked zones.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash checklist.* https://dash.plotly.com/dash-core-components/checklist
    - Plotly. *Dash slider.* https://dash.plotly.com/dash-core-components/slider
    - Plotly. *Dash layout.* https://dash.plotly.com/layout
    - Plotly. *Basic callbacks.* https://dash.plotly.com/basic-callbacks
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
