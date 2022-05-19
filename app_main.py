# VSC Analysis project Jacek Karnowka
# Creating requirements.txt:  pip freeze > requirements.txt
# -----------------------

# Import libraries
import shutil
import os.path
import dash
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.io as pio
from zipfile import ZipFile
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory, send_file

import Styles
import Dash_app_layout
import run_app

# Define global variables
global main_project_name
global project_number
global img_base_path
global path_all
global def_option
global all_options

# Define plotly template
plotly_template = pio.templates["plotly_dark"]

path_all = None

# Define main project upload directory
UPLOAD_DIRECTORY = "/project_tmp/app_uploaded_files"

# Check if upload_directory exist, if not create
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Define static variables, lists and settings
def_variable = "Vsc Scenario2"
def_sort_by = "Window Ref"

all_VCS = ["Vsc Scenario base", "Vsc Scenario2", "Scenario2/Scenario1"]


RADIOITEM_OPTIONS_SORT = [
    "Floor",
    "Window Ref",
    "Vsc Scenario base",
    "Vsc Scenario2",
    "Scenario2/Scenario1",
    "Meets BRE Criteria",
    "Window Orientation",
]

DROPDOWN_SHOW = ["Bar plot"]

IMAGE_STYLE = {"height": "100%", "width": "100%", "marginLeft": "30px"}

COLOR_NAMES = ["Green", "Soft Green", "Soft Red", "Red"]

COLOR_RGB = ["rgb(0, 128, 0)", "rgb(144,238,144)", "rgb(240,128,128)", "rgb(220,20,60)"]

COLORRGB_BRE = ["rgb(220,20,60)", "rgb(0, 128, 0)"]

CLICKED_SIZE = 17
CLICKED_OPACITY = 1
CLICKED_COLOR = "rgb(255, 191, 0)"

#
# Functions:
#

# Clearing upload_directory
def clear_directory(path):
    folder = "{}".format(urlquote(path))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


# GET OPTIONS - Get generated options (csv files)
def get_all_options():
    global path_all
    global all_options

    # if path is None end function and return empty list
    if path_all is None:
        return []

    path, dirs, files = next(os.walk(path_all))
    all_options = [
        {"label": str(files[i]).split("_")[1], "value": files[i]}
        for i in range(1, len(files))
    ]

    return all_options


# Define statistic bar chart figure
def bar_chart_figure():
    # if path is '' just return 0
    if path_all == "":
        return 0

    # Get all options
    # Look for titles in bar_all_options which are generally return values of get_all_options()
    bar_all_options = get_all_options()

    try:
        titles = [str(op).split("_")[1] for op in bar_all_options]
    except IndexError:
        raise TypeError("Wrong files names")

    color_names = COLOR_NAMES
    column_names = ["Option", "Green", "Soft Green", "Soft Red", "Red"]

    # Create DataFrame containing all options
    df_all = pd.DataFrame(columns=column_names)
    df_all["Option"] = titles
    choices = COLOR_RGB

    try:
        # Get all options and for each option assign a color -> color_range (function)
        for i in range(1, len(bar_all_options) + 1):
            df = pd.read_csv(
                r"{}\{}".format(path_all, bar_all_options[i - 1]["value"]),
                index_col=False,
            )
            df = color_range(df)

            for tmp in range(0, len(color_names)):
                df_all.loc[df_all["Option"] == titles[i - 1], color_names[tmp]] = len(
                    df[df.Color == choices[tmp]]
                )
    except TypeError:
        raise TypeError("CSV files do not exist in path")

    # Create traces of barplot
    traces = []
    for i in range(0, len(color_names)):
        traces.append(
            go.Bar(
                x=df_all["Option"],
                y=df_all[color_names[i]],
                name=color_names[i],
                text=df_all[color_names[i]],
                marker={"color": choices[i]},
            )
        )
    layout1 = go.Layout(
        title=Styles.BAR_PLOT_TITLE,
        title_font=Styles.BAR_PLOT_TITLE_FONT,
        legend=Styles.BAR_PLOT_LEGEND,
        hovermode="closest",
        plot_bgcolor=Styles.PLOT_BGCOLOR,
        paper_bgcolor=Styles.PAPER_BGCOLOR,
        font=Styles.BAR_PLOT_GEN_FONT,
    )

    fig = go.Figure(data=traces, layout=layout1)

    fig.update_yaxes(
        title_text="Number",
        gridcolor=Styles.GRAPH_LINES_COLOR,
        linecolor=Styles.GRAPH_LINES_COLOR,
        gridwidth=Styles.bar_chart_grid_width,
        linewidth=Styles.bar_chart_line_width,
        zerolinecolor=Styles.GRAPH_LINES_COLOR,
    ),

    fig.update_xaxes(
        title_text="Option",
        gridcolor=Styles.GRAPH_LINES_COLOR,
        linecolor=Styles.GRAPH_LINES_COLOR,
        gridwidth=Styles.bar_chart_grid_width,
        linewidth=Styles.bar_chart_line_width,
        zerolinecolor=Styles.GRAPH_LINES_COLOR,
    )

    return fig


# Color range choice based on condition.
# Created for bar plot
def color_range(df):
    try:
        conditions = [
            (df["Scenario2/Scenario1"] <= 0.5),
            (df["Scenario2/Scenario1"] > 0.5) & (df["Scenario2/Scenario1"] <= 0.7),
            (df["Scenario2/Scenario1"] > 0.7) & (df["Scenario2/Scenario1"] <= 0.8),
            (df["Scenario2/Scenario1"] > 0.8),
        ]
        choices = COLOR_RGB[::-1]
    except TypeError:
        raise TypeError("String value in Scenario2/Scenarion1 column")

    # Creating column with proper color
    df["Color"] = np.select(conditions, choices)
    return df


# COLOR RANGE BRE CRITERIUM - range for sortating by 'meets bra criterium'
def color_range_BRE(df):
    conditions = [
        (df["Scenario2/Scenario1"] < 0.8),
        (df["Scenario2/Scenario1"] >= 0.8),
    ]
    choices = COLORRGB_BRE

    # Creating column with proper color
    df["Color"] = np.select(conditions, choices)
    return df


# Encoding image based on path parameter
def encode_image(image_path):
    if os.path.isfile(image_path):
        encoded_image = base64.b64encode(open(image_path, "rb").read())
        return "data:image/Jpeg;base64,{}".format(encoded_image.decode())


# GET PROPER IMG PATH
# windows number from graph
# Option_picked- creating proper image path based on picked option
def get_images(window_number, option_picked):
    global img_base_path
    option_path = str(option_picked).split("_")[
        1
    ]  # Get project name, between underscores

    directory = "{}\{}\VSC".format(img_base_path, option_path)
    path, dirs, files = next(os.walk(directory))

    # Find image based on window number
    file = ""
    for index, name in enumerate(files):
        if name.find(window_number) != -1:
            file = files[index]
            break

    return "{}\{}".format(directory, file)


def parse_contents(contents, number):
    margin = 0 if number == 0 else 1

    parsed_content = html.Div(
        [
            html.H4(
                "Clicked image:",
                style={
                    "fontSize": 18,
                    "fontFamily": "sans-serif",
                    "color": Styles.YELLOW_FONT_COLOR,
                    "marginTop": "{}%".format(75 * margin),
                },
            ),
            html.Img(
                src=contents,
                style={
                    "height": "95%",
                    "width": "95%",
                    "marginLeft": "30px",
                    "marginTop": "{}px".format("5px"),
                },
            ),
        ]
    )

    return parsed_content


# Open uploaded zip file in uploaded_directory
def open_zip(file_name):
    if "Data" not in os.listdir("{}".format(UPLOAD_DIRECTORY)):
        os.mkdir("{}/Data".format(UPLOAD_DIRECTORY))

    with ZipFile(file_name, "r") as zip_file:
        zip_file.extractall("{}/Data".format(UPLOAD_DIRECTORY))


# Main graph default settings:
#   - Option is not choosen
#   - Proper file is not uploaded
def default_graph():
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker={
                "size": 1,
                "opacity": 1,
                "color": "rgb(255,255,255)",
                "line": {"width": 1.5, "color": "black"},
            },
        )
    )
    fig["layout"].update(
        title_text="Upload data and choose proper option",
        title_x=0.5,
        showlegend=False,
        height=450,
        plot_bgcolor=Styles.PLOT_BGCOLOR,
        paper_bgcolor=Styles.PAPER_BGCOLOR,
        font={"color": "gray", "family": "sans-serif", "size": 15},
    )

    fig.update_yaxes(
        title_text="Y variable",
        gridcolor=Styles.GRAPH_LINES_COLOR,
        linecolor=Styles.GRAPH_LINES_COLOR,
        gridwidth=0.3,
        linewidth=0.3,
        zerolinecolor=Styles.GRAPH_LINES_COLOR,
    ),

    fig.update_xaxes(
        title_text="X variable",
        gridcolor=Styles.GRAPH_LINES_COLOR,
        linecolor=Styles.GRAPH_LINES_COLOR,
        gridwidth=0.3,
        linewidth=0.3,
        zerolinecolor=Styles.GRAPH_LINES_COLOR,
    )

    fig.update_annotations(
        font={"size": 20, "family": "sans-serif", "color": Styles.YELLOW_FONT_COLOR}
    )
    return fig

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download1/{}".format(urlquote(filename))
    return html.A(filename, href=location)


def open_files():
    global img_base_path
    global path_all
    global main_project_name
    global project_number
    global all_options
    global def_option

    if os.path.isfile("{}/Data.zip".format(UPLOAD_DIRECTORY)):
        open_zip("{}/Data.zip".format(UPLOAD_DIRECTORY))
        main_project_name = os.listdir(
            "{}/Data/Data".format(urlquote(UPLOAD_DIRECTORY))
        )

        project_number = str(main_project_name[0]).split("-")[1]

        img_base_path = r"{}/Data/Data/{}/Results".format(
            urlquote(UPLOAD_DIRECTORY), main_project_name[0]
        )
        path_all = r"{}/Data/Data/{}/{}-3d-VSC-APSH-template_Waldram/Reports".format(
            urlquote(UPLOAD_DIRECTORY), main_project_name[0], project_number
        )
        all_options = get_all_options()
        def_option = all_options[0]
    else:
        return None

# Clear directory
# Run Flask server
# Create dash app, based on external stylesheets and Flask server
clear_directory(UPLOAD_DIRECTORY)


# Define route for downloading files
@run_app.server.route("/download1/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


# Main app layout, get from Dash_app_layout
run_app.app.layout = Dash_app_layout.get_layout()


@run_app.app.callback(
    Output("option_picker", "options"),
    Output("Bar_chart", "figure"),
    [Input("Refresh", "n_clicks")],
)
def option_refresh(value):
    open_files()
    return get_all_options(), bar_chart_figure()


@run_app.app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    [Input("my_graph", "hoverData"), Input("option_picker", "value")],
)
def display_hover(hoverData, option_picked):

    # If no hoverData or option was not picked, there is nothing to display
    if hoverData is None:
        return False, no_update, no_update
    if option_picked is None:
        return False, no_update, no_update

    # If there is hoverData, return two variables, window_number as a 'x' value, which is just number of
    # window from graph, graph_number as a "curveNumber" which is number of displayed graph.
    if hoverData:
        window_number = hoverData["points"][0]["x"]
        graph_number = hoverData["points"][0]["curveNumber"]
    else:
        window_number = "W120"
        graph_number = "0"

    # Get images based on picked window number and graph number
    source = get_images(window_number, option_picked[graph_number])
    bbox = hoverData["points"][0]["bbox"]

    children = [
        html.Div(
            [
                html.Img(src=encode_image(source), style={"width": "100%"}),
                html.H5(
                    id="Tooltip_number",
                    children="Window number:  {}".format(window_number),
                    style={"fontSize": 18, "fontFamily": "sans-serif"},
                ),
            ],
            style={
                "width": "250px",
                "white-space": "normal",
                "background_color": Styles.GRAPH_LINES_COLOR,
            },
        )
    ]

    return True, bbox, children


@run_app.app.callback(
    Output("collapse2", "is_open"),
    [Input("plot_picker", "value")],
    [State("collapse2", "is_open")],
)
def bar_plot_collapse(n, is_open):
    if n is None:
        return False

    if "Bar plot" in n:
        return True
    return False


# CREATING IMAGES
# based on clicked value on graph
@run_app.app.callback(
    Output("images", "children"),
    [Input("my_graph", "clickData"), Input("option_picker", "value")],
)
def print_images(clickData, option_picked):
    # Get window numeber of clicked point on graph
    if clickData:
        window_number = clickData["points"][0]["x"]
    else:
        window_number = "W120"

    source = []
    if option_picked is None:
        return 0

    # For every picked option, append source list with window images, based on every option
    for i in option_picked:
        source.append(get_images(window_number, i))

    # To display images, update Div from layout, to make it easier firstly parse content based on
    # 'source' list of images
    children = [
        parse_contents(encode_image(imgs), number) for number, imgs in enumerate(source)
    ]

    return children


# CREATE GRAPH
@run_app.app.callback(
    Output("my_graph", "figure"),
    [
        Input("option_picker", "value"),
        Input("sortby_picker", "value"),
        Input("variable_picker", "value"),
        Input("my_graph", "clickData"),
    ],
)
def graph_update(option, sort_by, variable, clickData):
    global path_all

    # Return default_graph() if there is no option picked
    if option is None or len(option) == 0:
        return default_graph()

    # Get titles based on picked options
    titles = [str(op).split("_")[1] for op in option]

    if clickData:
        clicked = clickData["points"][0]["x"]
    else:
        clicked = "0"

    # Create as many subplots as there are different graphs
    fig = make_subplots(
        rows=len(option), cols=1, subplot_titles=titles, shared_xaxes=False
    )

    # For every single option and create dataFrame base on CSV data
    for i in range(1, len(option) + 1):

        df = pd.read_csv(r"{}\{}".format(path_all, option[i - 1]), index_col=False)

        # Create new column with window number as int value
        df["Window_int"] = df["Window Ref"].apply(lambda x: int(str(x)[1:]))

        # Sort values based on picked sort option, if 'Window Ref' is picked, sort by
        # 'windows int' to sort numerically not alphabetically
        df.sort_values(
            sort_by if sort_by != "Window Ref" else "Window_int", inplace=True
        )

        df["Size"] = 12
        df["Opacity"] = 0.6

        if sort_by == "Meets BRE Criteria":
            df = color_range_BRE(df)
        else:
            df = color_range(df)

        df.loc[df["Window Ref"] == clicked, "Color"] = CLICKED_COLOR
        df.loc[df["Window Ref"] == clicked, "Size"] = CLICKED_SIZE
        df.loc[df["Window Ref"] == clicked, "Opacity"] = CLICKED_OPACITY

        x_variable = df["Window Ref"]
        y_variable = df[variable]

        fig.add_trace(
            go.Scatter(
                x=x_variable,
                y=y_variable,
                mode="markers",
                marker={
                    "size": df["Size"],
                    "opacity": df["Opacity"],
                    "color": df["Color"],
                    "line": {"width": 1.5, "color": "black"},
                },
            ),
            row=i,
            col=1,
        )

        fig["layout"].update(
            showlegend=False,
            height=450 * i,
            plot_bgcolor=Styles.PLOT_BGCOLOR,
            paper_bgcolor=Styles.PAPER_BGCOLOR,
            font={"color": "gray", "family": "sans-serif", "size": 15},
        )

        fig.update_yaxes(
            title_text=variable,
            gridcolor=Styles.GRAPH_LINES_COLOR,
            linecolor=Styles.GRAPH_LINES_COLOR,
            gridwidth=0.3,
            linewidth=0.3,
            zerolinecolor=Styles.GRAPH_LINES_COLOR,
            row=i,
            col=1,
        ),

        fig.update_xaxes(
            title_text="Window Ref",
            gridcolor=Styles.GRAPH_LINES_COLOR,
            linecolor=Styles.GRAPH_LINES_COLOR,
            gridwidth=0.3,
            linewidth=0.3,
            zerolinecolor=Styles.GRAPH_LINES_COLOR,
            row=i,
            col=1,
        )

        fig.update_annotations(
            font={
                "size": 20,
                "family": "sans-serif",
                "color": Styles.YELLOW_FONT_COLOR,
            },
        )
        fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


@run_app.server.route("/")
def download1(path):
    """Serve a file from the upload directory."""
    print(os.listdir("{}".format(UPLOAD_DIRECTORY)))
    print(os.listdir("{}/Excel_file".format(UPLOAD_DIRECTORY)))
    main_path = "Excel_file"
    full = os.path.join(UPLOAD_DIRECTORY, main_path)
    print(full)
    return send_file(full, path, as_attachment=True)

@run_app.app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()

    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]




# if __name__ == "__main__":
#    app.run_server(debug=True)
