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
    # A Checklist of Zones

    ## Objectives

    - Draw the daily power of Zone 1, Zone 2, and Zone 3 as lines on one fixed vertical scale.
    - Let a checklist turn zones on and off. In Dash the component is `dcc.Checklist`, and it starts with all three zones checked.
    - Keep the vertical scale tied to Zone 1 so a checked zone does not resize the chart.

    ## Background

    A checklist can have several values at once. The callback receives a list of the checked names. The line chart passes that list as `y`, so each checked zone is one line.

    The list can be empty. The chart then has a title and no lines.

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
    return power_file, zone_order


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
    print(daily.shape)
    return (daily,)


@app.cell
def _(daily):
    y_top = float(daily.Zone1.max() + 5000)
    print("vertical top:", round(y_top, 2))
    return (y_top,)


@app.cell
def _(daily, px, y_top, zone_order):
    _fig = px.line(
        daily,
        x="DateTime",
        y=zone_order,
        hover_data={"value": ":.2f"},
        title="Power consumption",
    )
    _fig.update_yaxes(range=[0, y_top])
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dash page

    The checklist options use a dictionary: the key is the column name, and the label is the text on the page. `value` starts as all three keys. The callback keeps a zone only when its name is in that list, and it keeps the Zone 1, Zone 2, Zone 3 order.

    ```python
    dcc.Checklist(
        id="zone-check",
        options={"Zone1": "Zone 1", "Zone2": "Zone 2", "Zone3": "Zone 3"},
        value=["Zone1", "Zone2", "Zone3"],
        labelStyle={"display": "inline-block", "margin-right": "20px"},
    )

    @dash_app.callback(
        Output("line-gr", "figure"),
        Input("zone-check", "value"),
    )
    def update_graph(selected_zones):
        zones = [zone for zone in ["Zone1", "Zone2", "Zone3"] if zone in selected_zones]
        figure = px.line(
            daily,
            x="DateTime",
            y=zones,
            hover_data={"value": ":.2f"},
            title="Power consumption",
        )
        figure.update_yaxes(range=[0, y_top])
        return figure
    ```

    The checklist below starts with the same three zones.
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
def _(daily, px, y_top, zone_order, zone_pick):
    _zones = [zone for zone in zone_order if zone in zone_pick.value]
    if len(_zones) == 0:
        _fig = px.line(title="Select at least one zone")
    else:
        _fig = px.line(
            daily,
            x="DateTime",
            y=_zones,
            hover_data={"value": ":.2f"},
            title="Power consumption",
        )
        _fig.update_yaxes(range=[0, y_top])
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_zones` is a list with Zone 1 and Zone 3. Which zone is left out of the line chart?
    """)
    return


@app.cell
def _(daily, px, y_top, zone_order):
    student_zones = ["Zone1", "Zone3"]
    _zones = [zone for zone in zone_order if zone in student_zones]
    _fig = px.line(
        daily,
        x="DateTime",
        y=_zones,
        hover_data={"value": ":.2f"},
        title="Zone 1 and Zone 3",
    )
    _fig.update_yaxes(range=[0, y_top])
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**Zone 2.** The list is walked in the order Zone 1, Zone 2, Zone 3, and a name is kept only when it is in `student_zones`.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The checklist value is a list of zone names. All three start checked.
    - The line chart draws one line per checked name, in the order Zone 1, Zone 2, Zone 3.
    - The vertical axis stays at Zone 1's maximum plus 5,000, including when a zone is unchecked.
    - An empty list draws no lines. In this file, the title asks for at least one zone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How is a checklist value different from a radio value?
    2. What is the starting list?
    3. Why does the callback walk `["Zone1", "Zone2", "Zone3"]` instead of using the checklist order?
    4. What is the vertical range?
    5. What happens when no zone is checked?
    6. What does `hover_data={"value": ":.2f"}` refer to?
    7. Which Dash property is the callback output?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **A list, not one name:** Several zones can be checked together. A radio list holds one name.
2. **All three zones:** `Zone1`, `Zone2`, and `Zone3`.
3. **To keep a stable order:** A checked zone is drawn in that fixed order, whichever way the checklist returns the names.
4. **0 to Zone 1's maximum plus 5,000:** Unchecking a zone does not move the axis.
5. **No lines:** In this file, the figure title is "Select at least one zone".
6. **The power values Plotly stacked:** A wide line chart stores the zone columns in one `value` field. The format shows two decimal places.
7. **The figure of `line-gr`:** The input is the `value` of `zone-check`.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash checklist.* https://dash.plotly.com/dash-core-components/checklist
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
