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
    # First Dashboard

    ## Objectives

    - Turn the Tetouan readings into one row per day, with the three zones stacked in a `Zone` column.
    - Draw one zone as a line of daily power.
    - Build that choice as a dropdown: a Dash layout names the dropdown and the graph, and a callback redraws the line. The dropdown below does the same filtering in this file.

    ## Background

    A Dash program describes a page as a tree of components. `html.H1` is the title. `dcc.Dropdown` is the list of zones. `dcc.Graph` is the place where a Plotly figure will appear. A callback is a function Dash runs when an input changes. Its `Output` is the figure property of the graph, and its `Input` is the value of the dropdown.

    A Dash program serves its own page. This file does not start that program. The dropdown in the last section is a marimo control, and the figure under it is redrawn when the choice changes.

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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are 52,416 rows, one every 10 minutes, from 1 January 2017 through 30 December 2017. The daily mean has 364 days. December 31 is not in the file.
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
    daily = (
        power.groupby(pd.Grouper(key="DateTime", freq="D"))
        .mean(numeric_only=True)
        .reset_index()
    )
    print(daily.shape)
    return (daily,)


@app.cell
def _(daily, mo):
    mo.Html(daily.head(3).to_html())
    return


@app.cell
def _(daily):
    daily_zones = daily.melt(id_vars=["DateTime"], value_vars=["Zone1", "Zone2", "Zone3"])
    daily_zones = daily_zones.rename(columns={"variable": "Zone", "value": "Power"})
    print(daily_zones.head(3))
    return (daily_zones,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each zone is one line. `hover_data={"Power": ":.2f"}` shows power with two decimal places. The vertical scale follows the zone that is drawn.
    """)
    return


@app.cell
def _(daily_zones, px):
    _zone = daily_zones[daily_zones["Zone"] == "Zone1"]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title="Power consumption in Zone1",
    )
    _fig
    return _fig


@app.cell
def _(daily_zones, px):
    _zone = daily_zones[daily_zones["Zone"] == "Zone2"]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title="Power consumption in Zone2",
    )
    _fig
    return _fig


@app.cell
def _(daily_zones, px):
    _zone = daily_zones[daily_zones["Zone"] == "Zone3"]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title="Power consumption in Zone3",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Dash page

    The layout is one `html.Div`. Inside it, from top to bottom:

    - an `html.H1` title, centered
    - a `dcc.Dropdown` whose options are the zone names, starting at `Zone1`, with id `zone-drop`
    - a `dcc.Graph` with id `line-gr` and no figure yet

    The callback connects them. When `zone-drop` changes, Dash calls `update_graph` with the selected name and puts the returned figure into `line-gr`.

    ```python
    dash_app.layout = html.Div(
        children=[
            html.H1(
                "Power consumption in Tetouan, 2017",
                style={"textAlign": "center"},
            ),
            dcc.Dropdown(
                id="zone-drop",
                options=["Zone1", "Zone2", "Zone3"],
                value="Zone1",
                style={"width": "50%"},
            ),
            dcc.Graph(id="line-gr"),
        ]
    )

    @dash_app.callback(
        Output("line-gr", "figure"),
        Input("zone-drop", "value"),
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
        return figure
    ```

    Starting that program would open a separate page. The control below is the same filter, inside this file.
    """)
    return


@app.cell
def _(mo):
    zone_choice = mo.ui.dropdown(
        options=["Zone1", "Zone2", "Zone3"],
        value="Zone1",
        label="Zone",
    )
    zone_choice
    return (zone_choice,)


@app.cell
def _(daily_zones, px, zone_choice):
    _zone = daily_zones[daily_zones["Zone"] == zone_choice.value]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title=f"Power consumption in {zone_choice.value}",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_zone` picks the line. Which column of `daily_zones` is compared with that name?
    """)
    return


@app.cell
def _(daily_zones, px):
    student_zone = "Zone3"
    _zone = daily_zones[daily_zones["Zone"] == student_zone]
    _fig = px.line(
        _zone,
        x="DateTime",
        y="Power",
        hover_data={"Power": ":.2f"},
        title=f"Power consumption in {student_zone}",
    )
    _fig
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
**`Zone`.** The filter keeps rows whose `Zone` equals `student_zone`. With `Zone3`, the line is the daily mean power of Zone 3.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The daily table has 364 rows. Stacking the zones produces three rows per day, with `Zone` and `Power`.
    - A line of one zone uses the rows that match that zone name. The title repeats the name, and the power tooltip has two decimal places.
    - In Dash, the dropdown's `value` is the callback input and the graph's `figure` is the callback output.
    - The dropdown in this file sends the same zone name into the filter. Changing it redraws the line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How many daily rows are there, and which calendar day is absent?
    2. What do `Zone` and `Power` contain after `melt`?
    3. What is the input of the callback, and what is the output?
    4. Why does the graph component start without a figure?
    5. What does `hover_data={"Power": ":.2f"}` change?
    6. Does this line chart lock the vertical scale to one zone?
    7. What does the dropdown in this file change?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Show answers": mo.md(r"""
1. **364 days:** The readings run from 1 January through 30 December 2017. December 31 is not in the file.
2. **The zone name and the daily power:** Each old zone column becomes rows. `Zone` is `Zone1`, `Zone2`, or `Zone3`. `Power` is that day's mean.
3. **The dropdown value, and the graph figure:** `Input` reads `zone-drop`. `Output` writes the `figure` of `line-gr`.
4. **The callback fills it:** The layout only reserves the graph. The function builds the figure after a zone is chosen.
5. **The tooltip:** Power is shown with two decimal places.
6. **No:** Each zone is drawn on a scale that fits that zone's values.
7. **Which zone is filtered:** The line and the title follow `zone_choice.value`.
""")}, lazy=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Plotly. *Dash dropdown.* https://dash.plotly.com/dash-core-components/dropdown
    - Plotly. *Basic callbacks.* https://dash.plotly.com/basic-callbacks
    - Salam, A., and El Hibaoui, A. (2018). Comparison of Machine Learning Algorithms for the Power Consumption Prediction: Case Study of Tetouan city. In *2018 6th International Renewable and Sustainable Energy Conference (IRSEC)*, pp. 1–5.
    """)
    return


if __name__ == "__main__":
    app.run()
