# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "pandas",
#     "bokeh",
#     "scipy",
# ]
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from io import StringIO
    import urllib.request

    import marimo as mo
    import pandas as pd
    from bokeh.models import ColumnDataSource, FactorRange
    from bokeh.palettes import Greens, Spectral
    from bokeh.plotting import figure
    from bokeh.transform import factor_cmap
    from scipy.io.arff import loadarff

    return (
        ColumnDataSource,
        FactorRange,
        Greens,
        Spectral,
        StringIO,
        factor_cmap,
        figure,
        loadarff,
        mo,
        pd,
        urllib,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Bar Plots with Bokeh

    ## Objectives

    - Read the student academics file and decode the text columns.
    - Draw a vertical bar chart of the father's occupation and a horizontal bar chart of the mother's occupation.
    - Stack father and mother counts on one bar, after giving both columns the same occupation names.
    - Draw the same counts as grouped bars, one bar for the father and one for the mother.

    ## Background

    A vertical bar uses `vbar`. A horizontal bar uses `hbar`. `x_range` or `y_range` is the list of category names, so each bar has a slot.

    `ColumnDataSource` holds the columns the glyphs read. `Greens` and `Spectral` are dictionaries of color tuples. The key is how many colors you ask for. This file has five occupations in each column, and both palettes have a 5-color entry.

    A stacked bar needs the same category names in both series. The mother's column uses Housewife where the father's column uses Farmer. The stacked charts copy the table and replace Housewife with Farmer so the five names line up. That replacement is only so the bars share labels.

    ## Datasets Used

    - **Student Academics Performance** from the UCI Machine Learning Repository. The file is `Sapfile1.arff`. `fo` is the father's occupation. `mo` is the mother's occupation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where the file is read from

    Python can read a file directly from a web address. Whether that works depends on **where Python is running**.

    - **On your computer.** Python can download a file from the UCI website.
    - **Inside a web browser.** This lesson can run inside a web page. The browser only lets a page download files from websites that allow it. This security rule is called **CORS**. The UCI website does not allow it, so the browser blocks that download.

    This lesson reads a copy of the file stored on GitHub. GitHub allows a browser page to read its files, so the copy works in both places. The original UCI address is kept in a comment.
    """)
    return


@app.cell
def _():
    student_file = (
        "https://raw.githubusercontent.com/Goliath-Research/"
        "Data-Visualization/main/Bokeh-Altair/Sapfile1.arff"
    )
    # UCI address, blocked in the browser:
    # https://archive.ics.uci.edu/ml/machine-learning-databases/00467/Sapfile1.arff
    return (student_file,)


@app.cell
def _(StringIO, loadarff, student_file, urllib):
    with urllib.request.urlopen(student_file) as _resp:
        arff_rows, _meta = loadarff(StringIO(_resp.read().decode("utf-8")))
    student_columns = list(_meta._attributes.keys())
    print(student_columns)
    return arff_rows, student_columns


@app.cell
def _(arff_rows, pd, student_columns):
    students_raw = pd.DataFrame(arff_rows, columns=student_columns)
    print(students_raw.shape)
    return (students_raw,)


@app.cell
def _(mo, students_raw):
    mo.Html(students_raw.head(3).to_html())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The text columns arrive as bytes, so a value looks like `b'Service'`. This cell builds a new table and decodes those columns to ordinary strings.
    """)
    return


@app.cell
def _(students_raw):
    def _decode(column):
        if column.dtype == object and isinstance(column.iloc[0], (bytes, bytearray)):
            return column.str.decode("utf-8")
        return column

    students = students_raw.apply(_decode)
    print(students.fo.head(3).tolist())
    return (students,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Father's occupation

    `fo` has five labels: Service, Business, Others, Farmer, and Retired. `value_counts` orders them from the most common to the least common.
    """)
    return


@app.cell
def _(students):
    father_counts = students.fo.value_counts()
    print(father_counts)
    return (father_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vertical bars

    The source has one row per occupation: the name, the count, and a green. `vbar` reads `values` as the category and `counts` as the height. The bar width is 0.8 of the category slot.
    """)
    return


@app.cell
def _(ColumnDataSource, Greens, father_counts):
    father_source = ColumnDataSource(
        data=dict(
            values=list(father_counts.index),
            counts=father_counts,
            color=Greens[len(father_counts)],
        )
    )
    print(list(father_source.data.keys()))
    return (father_source,)


@app.cell
def _(father_counts, father_source, figure):
    _fig = figure(
        x_range=list(father_counts.index),
        height=350,
        title="Father Occupation",
    )
    _fig.vbar(x="values", top="counts", width=0.8, source=father_source)
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `color="color"` paints each bar from the source. `legend_field="values"` uses the occupation name as the legend label.
    """)
    return


@app.cell
def _(father_counts, father_source, figure):
    _fig = figure(
        x_range=list(father_counts.index),
        height=350,
        title="Father Occupation",
    )
    _fig.vbar(
        x="values",
        top="counts",
        width=0.8,
        color="color",
        legend_field="values",
        source=father_source,
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Try it yourself

    `Greens` is keyed by the number of colors. There are five father occupations. How many greens does `Greens[5]` hold?
    """)
    return


@app.cell
def _(Greens):
    student_greens = Greens[5]
    print(len(student_greens))
    print(student_greens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
**Five greens.** The key is the number of colors in the tuple. Five occupations ask for `Greens[5]`.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Mother's occupation

    `mo` also has five labels. Housewife is the largest group. The horizontal chart uses `hbar`, so the categories go on `y_range` and the counts go to the right.
    """)
    return


@app.cell
def _(students):
    mother_counts = students.mo.value_counts()
    print(mother_counts)
    return (mother_counts,)


@app.cell
def _(ColumnDataSource, Spectral, figure, mother_counts):
    _source = ColumnDataSource(
        data=dict(
            values=list(mother_counts.index),
            counts=mother_counts,
            color=Spectral[len(mother_counts)],
        )
    )
    _fig = figure(
        y_range=list(mother_counts.index),
        height=400,
        title="Mother Occupation",
    )
    _fig.hbar(
        y="values",
        right="counts",
        color="color",
        height=0.8,
        legend_field="values",
        source=_source,
    )
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Stacked bars

    The stacked chart needs one row per occupation and two count columns, Father and Mother, in the same order. Sorting both counts by name puts Business, Farmer, Others, Retired, and Service in the same row positions.

    Housewife is renamed Farmer on a copy. The original mother counts above stay as they were read.
    """)
    return


@app.cell
def _(students):
    aligned = students.assign(mo=students.mo.replace({"Housewife": "Farmer"}))
    occupations = aligned.mo.value_counts().sort_index().index.tolist()
    father_sorted = aligned.fo.value_counts().sort_index()
    mother_sorted = aligned.mo.value_counts().sort_index()
    print("occupations:", occupations)
    print(father_sorted)
    print(mother_sorted)
    return father_sorted, mother_sorted, occupations


@app.cell
def _(father_sorted, mother_sorted, occupations):
    parent = ["Father", "Mother"]
    stacked_data = {
        "occupations": occupations,
        "Father": list(father_sorted),
        "Mother": list(mother_sorted),
    }
    print(stacked_data)
    return parent, stacked_data


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `vbar_stack` draws one stack per occupation. The hover reads the stack name and the count: `($name) @occupations: @$name`. The legend is vertical, at the top right. The y axis starts at 0.
    """)
    return


@app.cell
def _(figure, occupations, parent, stacked_data):
    _fig = figure(
        x_range=occupations,
        height=350,
        title="Parents' Occupations",
        toolbar_location=None,
        tools="hover",
        tooltips="($name) @occupations: @$name",
    )
    _fig.vbar_stack(
        parent,
        x="occupations",
        width=0.8,
        color=["skyblue", "salmon"],
        source=stacked_data,
        legend_label=parent,
    )
    _fig.y_range.start = 0
    _fig.x_range.range_padding = 0.1
    _fig.legend.location = "top_right"
    _fig.legend.orientation = "vertical"
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a new figure with the same stacks. The legend is horizontal, and the colors are steel blue and coral.
    """)
    return


@app.cell
def _(figure, occupations, parent, stacked_data):
    _fig = figure(
        x_range=occupations,
        height=350,
        title="Parents' Occupations",
        toolbar_location=None,
        tools="hover",
        tooltips="($name) @occupations: @$name",
    )
    _fig.vbar_stack(
        parent,
        x="occupations",
        width=0.8,
        color=["steelblue", "coral"],
        source=stacked_data,
        legend_label=parent,
    )
    _fig.y_range.start = 0
    _fig.x_range.range_padding = 0.1
    _fig.legend.location = "top_right"
    _fig.legend.orientation = "horizontal"
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Horizontal stacks

    `hbar_stack` uses the occupation on the y axis. The count runs to the right. The first figure keeps a vertical legend. The second figure places a horizontal legend at the center.
    """)
    return


@app.cell
def _(figure, occupations, parent, stacked_data):
    _fig = figure(
        y_range=occupations,
        width=600,
        height=400,
        title="Parents' Occupations",
        toolbar_location=None,
        tools="hover",
        tooltips="($name) @occupations: @$name",
    )
    _fig.hbar_stack(
        parent,
        y="occupations",
        height=0.9,
        color=["skyblue", "salmon"],
        source=stacked_data,
        legend_label=parent,
    )
    _fig.x_range.start = 0
    _fig.y_range.range_padding = 0.1
    _fig.legend.location = "top_right"
    _fig.legend.orientation = "vertical"
    return _fig


@app.cell
def _(figure, occupations, parent, stacked_data):
    _fig = figure(
        y_range=occupations,
        width=600,
        height=400,
        title="Parents' Occupations",
        toolbar_location=None,
        tools="hover",
        tooltips="($name) @occupations: @$name",
    )
    _fig.hbar_stack(
        parent,
        y="occupations",
        height=0.9,
        color=["steelblue", "coral"],
        source=stacked_data,
        legend_label=parent,
    )
    _fig.x_range.start = 0
    _fig.y_range.range_padding = 0.1
    _fig.legend.location = "center"
    _fig.legend.orientation = "horizontal"
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Grouped bars

    Each bar is one pair `(occupation, parent)`. `FactorRange` makes a slot for every pair. `zip` walks the father counts and the mother counts together, so the count list is father, mother, father, mother, and so on.

    `factor_cmap` colors by the parent, which is the second part of the pair (`start=1`, `end=2`).
    """)
    return


@app.cell
def _(occupations, parent, stacked_data):
    grouped_x = [(occ, par) for occ in occupations for par in parent]
    grouped_counts = sum(zip(stacked_data["Father"], stacked_data["Mother"]), ())
    print(grouped_x)
    print(grouped_counts)
    return grouped_counts, grouped_x


@app.cell
def _(ColumnDataSource, FactorRange, factor_cmap, figure, grouped_counts, grouped_x, parent):
    _source = ColumnDataSource(data=dict(x=grouped_x, counts=grouped_counts))
    _fig = figure(
        x_range=FactorRange(*grouped_x),
        width=700,
        height=350,
        title="Parents' Occupations",
        toolbar_location=None,
        tools="hover",
        tooltips="@counts",
    )
    _fig.vbar(
        x="x",
        top="counts",
        width=0.9,
        source=_source,
        line_color="white",
        fill_color=factor_cmap(
            "x",
            palette=["lightskyblue", "pink"],
            factors=parent,
            start=1,
            end=2,
        ),
    )
    _fig.y_range.start = 0
    _fig.x_range.range_padding = 0.1
    _fig.xaxis.major_label_orientation = 1
    _fig.xgrid.grid_line_color = None
    return _fig


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conclusions

    - The file has 131 students and 22 columns. Text values are decoded from bytes before the counts.
    - Fathers: Service 38, Business 34, Others 29, Farmer 27, Retired 3. The vertical bars use `Greens[5]` in that order.
    - Mothers: Housewife 115, Service 12, Others 2, Business 1, Retired 1. The horizontal bars use `Spectral[5]`.
    - The stacked charts rename Housewife to Farmer on a copy, then sort both columns alphabetically so each stack is one occupation. Hover shows the parent name and the count.
    - The grouped chart makes a `(occupation, parent)` pair for every bar and colors the bar by the parent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check your understanding

    1. Why are the text columns decoded?
    2. How many students are in the file?
    3. Which father occupation has the most students?
    4. Which mother occupation has the most students, before any renaming?
    5. Why does the stacked chart replace Housewife with Farmer?
    6. What does `legend.orientation = "horizontal"` change?
    7. In the grouped chart, what does one x label stand for?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion(
        {
            "Show answers": mo.md(r"""
1. **They arrive as bytes.** A label looks like `b'Service'` until `str.decode` turns it into `Service`.
2. **131 students.** The table has 131 rows and 22 columns.
3. **Service.** 38 fathers are in Service.
4. **Housewife.** 115 mothers are in Housewife.
5. **So the names match.** The father column has Farmer and no Housewife. The stacked bars need the same five names in the same order.
6. **The legend entries sit in a row.** The counts and the colors stay the same.
7. **One occupation and one parent.** A label such as `(Business, Father)` is the father's count for that occupation.
""")
        },
        lazy=True,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## References

    - Hussain, S., Dahan, N. A., Ba-Alwi, F. M., and Ribata, N. Educational Data Mining and Analysis of Students' Academic Performance Using WEKA. *Indonesian Journal of Electrical Engineering and Computer Science*, 2018, Vol. 9, No. 2, pp. 447–459.
    - Bokeh. *Documentation.* https://docs.bokeh.org/en/latest/
    - Bokeh. *Bar charts.* https://docs.bokeh.org/en/latest/docs/user_guide/basic/bars.html
    """)
    return


if __name__ == "__main__":
    app.run()
