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
    # A Radio List of Zones

    ## Objectives

    - Build the daily Tetouan table and stack the three zones into `Zone` and `Power`.
    - Draw one zone as an orange-red line on a vertical scale that stays fixed.
    - Select the zone with a radio list. In Dash that list is `dcc.RadioItems`. The radio buttons below do the same selection in this file.

    ## Background

    A radio list shows every choice at once and keeps one choice selected. The Dash callback has one input, the radio value, and one output, the figure.

    The vertical range is computed from Zone 1: 0 through that zone's maximum daily power, plus 5,000. Zone 2 and Zone 3 stay inside that range, so changing the zone does not rescale the chart. The line color stays orange-red for every zone.

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
    print(daily.shape)
    return (daily,)


@app.cell
def _(daily):
    daily_zones = daily.melt(id_vars=["DateTime"], value_vars=["Zone1", "Zone2", "Zone3"])
    daily_zones = daily_zones.rename(columns={"variable": "Zone", "value": "Power"})
    y_top = float(daily.Zone1.max() + 5000)
    print("vertical top:", round(y_top, 2))
    return daily_zones, y_top


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The top of the axis is Zone 1's largest daily mean plus 5,000. The example below draws Zone 3 on that fixed scale, in orange-red.
    """)
    return


@app.cell
def _(daily_zones, px, y_top):
    _zone = daily_zones[daily_zones["Zone"] == "Zone3"]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title="Power consumption in Zone3",
    )
    _fig.update_yaxes(range=[0, y_top])
    _fig.update_traces(line_color="orangered")
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dash page

    `dcc.RadioItems` lists `Zone1`, `Zone2`, and `Zone3` on one row. The starting value is `Zone1`. The graph id is `line-gr`.

    ```python
    dcc.RadioItems(
        id="radio-id",
        options=["Zone1", "Zone2", "Zone3"],
        value="Zone1",
        labelStyle={"display": "inline-block", "margin-right": "30px"},
    )

    @dash_app.callback(
        Output("line-gr", "figure"),
        Input("radio-id", "value"),
    )
    def update_graph(selected_zone):
        filtered = daily_zones[daily_zones["Zone"] == selected_zone]
        figure = px.line(
            filtered,
            x="DateTime",
            y="Power",
            hover_data={"Power": ":.2f"},
            title=f"Power consumption in {selected_zone}",
        )
        figure.update_yaxes(range=[0, y_top])
        figure.update_traces(line_color="orangered")
        return figure
    ```

    The radio buttons below call the same filter.
    """)
    return


@app.cell
def _(mo):
    zone_choice = mo.ui.radio(
        options=["Zone1", "Zone2", "Zone3"],
        value="Zone1",
        label="Zone",
        inline=True,
    )
    zone_choice
    return (zone_choice,)


@app.cell
def _(daily_zones, px, y_top, zone_choice):
    _zone = daily_zones[daily_zones["Zone"] == zone_choice.value]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title=f"Power consumption in {zone_choice.value}",
    )
    _fig.update_yaxes(range=[0, y_top])
    _fig.update_traces(line_color="orangered")
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    The scale is taken from Zone 1. If the selected line is Zone 2, does the top of the axis change?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**No.** `y_top` is Zone 1's maximum plus 5,000. Every zone uses that same range, and the line stays orange-red.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The radio list has one selected zone. The line uses the matching rows of `daily_zones`.
    - The vertical axis always runs from 0 to Zone 1's maximum daily power plus 5,000. Zone 2 and Zone 3 fit inside that range.
    - The line color is orange-red for every choice.
    - In Dash, `dcc.RadioItems` is the callback input and the graph figure is the output. The radio control in this file does that selection directly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How many choices can a radio list have selected?
    2. Which zone sets the top of the vertical axis?
    3. Do Zone 2 and Zone 3 fit under that top?
    4. What color is the line after a new zone is chosen?
    5. What is the id of the radio input in the Dash callback?
    6. What does the callback return?
    7. Why is a fixed scale useful when the zone changes?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **One:** A radio list keeps a single value. This list starts at `Zone1`.
2. **Zone 1:** The top is that zone's largest daily mean, plus 5,000.
3. **Yes:** Their largest daily means are below that top.
4. **Orange-red:** `update_traces` sets `line_color="orangered"` for every zone.
5. **`radio-id`:** The `Input` reads its `value`.
6. **The line figure:** That figure is written to the `figure` property of `line-gr`.
7. **The height stays comparable:** A peak in Zone 3 is drawn on the same axis as a peak in Zone 1.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash radio items.* https://dash.plotly.com/dash-core-components/radioitems
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
