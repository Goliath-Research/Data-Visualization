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
    # Power Consumption Dashboard

    ## Objectives

    - Read the Tetouan power file and reduce it to one row per day.
    - Melt the three zone columns into one `Power` column.
    - Draw temperature, humidity, and wind speed against power, with a zone legend.
    - Filter those charts with a month slider.

    ## Background

    The file records three zones in Tetouan every 10 minutes during 2017. A daily mean is the average of those readings on each date. December 31 is not in the file, so the daily table has 364 days.

    Melting stacks Zone 1, Zone 2, and Zone 3 into `Zone` and `Power`. Each day then has three rows.

    The legend is a point selection on `Zone`. The scatters share that selection, so a click highlights one zone. Click and Shift adds another zone. The month control is a range binding on `Month`, starting at 1. `transform_filter` keeps that month.

    The charts show the daily mean power next to temperature, humidity, and wind speed. They do not measure a policy effect.

    ## Datasets Used

    - **Power consumption of Tetouan city**, from the UCI Machine Learning Repository. Three zones in Tetouan, Morocco, in 2017.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the file is read from

    Pandas can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website, and it can read `Tetuan-City-power-consumption.csv` from the Plotly-Dash folder.
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
    # Local file in the Plotly-Dash folder: Tetuan-City-power-consumption.csv
    return (power_file,)


@app.cell
def _(pd, power_file):
    power = pd.read_csv(power_file)
    power = power.rename(
        columns={
            "Zone 1 Power Consumption": "Zone 1",
            "Zone 2  Power Consumption": "Zone 2",
            "Zone 3  Power Consumption": "Zone 3",
        }
    )
    power = power.assign(DateTime=pd.to_datetime(power.DateTime))
    print(power.shape)
    return (power,)


@app.cell
def _(mo, power):
    mo.Html(power.head().to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are 52,416 rows, one every 10 minutes, from 1 January 2017 through 30 December 2017. The daily mean has 364 days.
    """)
    return


@app.cell
def _(pd, power):
    daily = (
        power.groupby(pd.Grouper(key="DateTime", freq="1D"), as_index=False)
        .mean()
        .assign(Month=lambda frame: frame.DateTime.dt.month)
    )
    print(daily.shape)
    print("months:", sorted(daily.Month.dropna().unique().tolist()))
    return (daily,)


@app.cell
def _(mo, daily):
    mo.Html(daily.head().to_html())
    return


@app.cell
def _(daily, pd):
    melted = pd.melt(
        daily,
        id_vars=["Month", "Temperature", "Humidity", "Wind Speed"],
        value_vars=["Zone 1", "Zone 2", "Zone 3"],
    )
    melted = melted.rename(columns={"variable": "Zone", "value": "Power"})
    print(melted.shape)
    print(melted.head())
    return (melted,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zone legend

    The legend and the temperature scatter share one selection. Click a zone. Click and Shift to add another. Unselected zones turn light gray.
    """)
    return


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _temperature = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Temperature:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(
            width=230,
            height=250,
            title={"text": "Temperature vs. Power", "fontSize": 16},
        )
        .add_params(_zones)
    )
    _chart = _temperature | _legend
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Humidity and wind speed use the same legend pattern. Each pair has its own selection.
    """)
    return


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _humidity = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Humidity:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(
            width=230,
            height=250,
            title={"text": "Humidity vs. Power", "fontSize": 16},
        )
        .add_params(_zones)
    )
    _chart = _humidity | _legend
    _chart
    return _chart


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _wind = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            x=alt.X("Wind Speed:Q", scale=alt.Scale(zero=False)),
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(
            width=230,
            height=250,
            title={"text": "Wind Speed vs. Power", "fontSize": 16},
        )
        .add_params(_zones)
    )
    _chart = _wind | _legend
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## One dashboard

    Temperature, humidity, and wind speed sit in a row with the legend. The next cell places wind and the legend under the first two charts. All four views in a cell share one zone selection.
    """)
    return


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _base = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(width=230, height=250)
        .add_params(_zones)
    )
    _temperature = _base.encode(
        alt.X("Temperature:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Temperature vs. Power", "fontSize": 16})
    _humidity = _base.encode(
        alt.X("Humidity:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Humidity vs. Power", "fontSize": 16})
    _wind = _base.encode(
        alt.X("Wind Speed:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Wind Speed vs. Power", "fontSize": 16})
    _chart = _temperature | _humidity | _wind | _legend
    _chart
    return _chart


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _base = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(width=230, height=250)
        .add_params(_zones)
    )
    _temperature = _base.encode(
        alt.X("Temperature:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Temperature vs. Power", "fontSize": 16})
    _humidity = _base.encode(
        alt.X("Humidity:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Humidity vs. Power", "fontSize": 16})
    _wind = _base.encode(
        alt.X("Wind Speed:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Wind Speed vs. Power", "fontSize": 16})
    _chart = (_temperature | _humidity) & (_wind | _legend)
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A month slider

    The slider runs from 1 to 12 and starts at January. The filter keeps the selected month. The zone selection still works inside that month. The second layout puts wind and the legend on the lower row.
    """)
    return


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _month_slider = alt.binding_range(min=1, max=12, step=1, name="Month:")
    _month_pick = alt.selection_point(fields=["Month"], value=1, bind=_month_slider)
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _base = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(width=230, height=250)
        .add_params(_zones, _month_pick)
        .transform_filter(_month_pick)
    )
    _temperature = _base.encode(
        alt.X("Temperature:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Temperature vs. Power", "fontSize": 16})
    _humidity = _base.encode(
        alt.X("Humidity:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Humidity vs. Power", "fontSize": 16})
    _wind = _base.encode(
        alt.X("Wind Speed:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Wind Speed vs. Power", "fontSize": 16})
    _chart = _temperature | _humidity | _wind | _legend
    _chart
    return _chart


@app.cell
def _(alt, melted):
    _zones = alt.selection_point(fields=["Zone"])
    _month_slider = alt.binding_range(min=1, max=12, step=1, name="Month:")
    _month_pick = alt.selection_point(fields=["Month"], value=1, bind=_month_slider)
    _zone_color = alt.condition(
        _zones,
        alt.Color("Zone:N", legend=None),
        alt.value("lightgray"),
    )
    _legend = (
        alt.Chart(melted)
        .mark_circle(size=100)
        .encode(
            y=alt.Y("Zone:N", axis=alt.Axis(orient="left")),
            color=_zone_color,
        )
        .add_params(_zones)
    )
    _base = (
        alt.Chart(melted)
        .mark_circle(size=60)
        .encode(
            y=alt.Y("Power:Q", title="Power"),
            color=_zone_color,
            tooltip=["Power:Q"],
        )
        .properties(width=230, height=250)
        .add_params(_zones, _month_pick)
        .transform_filter(_month_pick)
    )
    _temperature = _base.encode(
        alt.X("Temperature:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Temperature vs. Power", "fontSize": 16})
    _humidity = _base.encode(
        alt.X("Humidity:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Humidity vs. Power", "fontSize": 16})
    _wind = _base.encode(
        alt.X("Wind Speed:Q", scale=alt.Scale(zero=False))
    ).properties(title={"text": "Wind Speed vs. Power", "fontSize": 16})
    _chart = (_temperature | _humidity) & (_wind | _legend)
    _chart
    return _chart


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `student_month` is 1. How many days of January are in a non-leap year such as 2017?
    """)
    return


@app.cell
def _(daily):
    student_month = 1
    print(int((daily.Month == student_month).sum()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**31 days.** January 2017 is complete in the daily table. December stops on the 30th, so the year has 364 daily rows.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The file has 52,416 rows, one every 10 minutes, from 1 January 2017 through 30 December 2017. The daily mean has 364 days. December 31 is absent.
    - Melting the three zone columns makes 1,092 rows: 364 days times 3 zones. `Zone` is the zone name and `Power` is that zone's daily mean.
    - The legend selects zones. Click and Shift selects more than one. Unselected zones are light gray. Temperature, humidity, and wind speed each have their own scatter against power.
    - The month slider starts at 1 and keeps one month. The same zone selection works inside that month.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. How many rows are in the original file?
    2. Why does the daily table have 364 rows?
    3. How many rows does the melted table have?
    4. What does a click on the legend do?
    5. How do you highlight two zones?
    6. What does the month slider filter?
    7. Which month is selected when the slider starts?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **52,416 rows.** That is one reading every 10 minutes.
2. **December 31 is missing.** 2017 would have 365 days. The file stops on 30 December.
3. **1,092 rows.** 364 days times the three zones.
4. **It highlights that zone.** The other zones turn light gray.
5. **Click and Shift.** The selection can hold more than one zone.
6. **The daily rows of one month.** Temperature, humidity, and wind speed all use that filter.
7. **January.** The selection value is 1.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Altair. *Interactive charts.* https://altair-viz.github.io/user_guide/interactions.html
    - UCI Machine Learning Repository. *Power consumption of Tetouan city.* https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city
    """)
    return


if __name__ == "__main__":
    app.run()
