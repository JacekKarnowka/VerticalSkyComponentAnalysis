# Creating requirements.txt:  pip freeze > requirements.txt
#
#
import base64
import uuid
import os, shutil
import os.path
import dash_uploader as du
import dash
from dash import dcc
from dash import dash_table
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from dash import Input, Output, State, html, no_update
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.io as pio
import os
from zipfile import ZipFile
import xlsxwriter
import glob
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory

global main_project_name
global project_number
global img_base_path
global path_all
global def_option

plotly_template = pio.templates["plotly_dark"]

path_all = None

UPLOAD_DIRECTORY = "/project_tmp/app_uploaded_files"


def clear_directory(path):

    folder = ('{}'.format(urlquote(path)))
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

def_variable = "Vsc Scenario2"
def_sort_by = "Window Ref"

all_VCS = ['Vsc Scenario base', 'Vsc Scenario2', 'Scenario2/Scenario1']

text_font_size = 22
left_menu_font_size = '16px'

bar_chart_grid_width = 0.3
bar_chart_line_width = 0.3

PLOT_BGCOLOR = "#1e1e1e"
PAPER_BGCOLOR = "#1e1e1e"
GRAPH_LINES_COLOR = '#636363'
LEFT_MENU_COLOR = '#2b2b2b'

TABLE_CELL_STYLE = {
    'font-family': 'sans-serif',
    'font-color': 'grey',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'textAlign': 'right',
    'font_size': '13px',
    'height': '23px',
    'border': '1px solid {}'.format(GRAPH_LINES_COLOR),
    'backgroundColor': PLOT_BGCOLOR
}

TABLE_HEADER_STYLE = {
    'backgroundColor': PLOT_BGCOLOR,
    'color': 'white',
    'font-family': 'sans-serif',
    'fontWeight': 'bold',
    'height': '23px',
    'textAlign': 'right',
    'font_size': '15px',
    'border': '1px solid {}'.format(GRAPH_LINES_COLOR),
}

TABLE_DATA_STYLE = {
    'color': 'white'
}
TABLE_COLUMNS = [{'name': 'Option', 'id': 'Option'},
                 {'name': 'Window ref.', 'id': 'Window_ref'},
                 {'name': 'Floor', 'id': 'Floor'},
                 {'name': 'VSC scenario base', 'id': 'VSC_base'},
                 {'name': 'VSC scenario 2', 'id': 'VSC_scen_2'},
                 {'name': 'Ratio', 'id': 'ratio'},
                 {'name': 'Window orientation', 'id': 'Window_orien'}]

TABLE_CELL_CONDITION = [{'if': {'column_id': 'Option'},
                         'width': '200px'},
                        {'if': {'column_id': 'Window_ref'},
                         'width': '120px'},
                        {'if': {'column_id': 'Floor'},
                         'width': '100px'},
                        {'if': {'column_id': 'VSC_base'},
                         'width': '150'},
                        {'if': {'column_id': 'VSC_scen_2'},
                         'width': '150'},
                        {'if': {'column_id': 'ratio'},
                         'width': '100px'}]

TEXT_STYLE = {'fontSize': text_font_size,
              'paddingRight': '30px',
              'marginTop': '15px',
              'marginLeft': '15px'}

DROPDOWN_STYLE = {'marginTop': '15px',
                  'width': '95%',
                  'marginLeft': '30px',
                  'marginBottom': '10px',
                  'font-size': left_menu_font_size,
                  'color': '#657895'}

RADIOITEMS_STYLE = {'marginTop': '10px',
                    'marginLeft': '30px',
                    'font-size': left_menu_font_size}

CHECKLIST_STYLE = {'marginTop': '15px',
                   'width': '95%',
                   'marginLeft': '30px',
                   'marginBottom': '10px',
                   'font-size': left_menu_font_size,
                   'color': '#657895',
                   'max-height': '150px',
                   'overflow': 'auto'}

RADIOITEM_OPTIONS_SORT = ['Floor', 'Window Ref', 'Vsc Scenario base', 'Vsc Scenario2',
                          'Scenario2/Scenario1', 'Meets BRE Criteria', 'Window Orientation']

DROPDOWN_SHOW = ['Table', 'Bar plot']

IMAGE_STYLE = {'height': '100%',
               'width': '100%',
               'marginLeft': '30px'}

COLOR_NAMES = ['Green', 'Soft Green', 'Soft Red', 'Red']

COLOR_RGB = ['rgb(0, 128, 0)', 'rgb(144,238,144)', 'rgb(240,128,128)', 'rgb(220,20,60)']

COLORRGB_BRE = ['rgb(220,20,60)', 'rgb(0, 128, 0)']

CLICKED_SIZE = 17
CLICKED_OPACITY = 1
CLICKED_COLOR = 'rgb(255, 191, 0)'


# GET OPTIONS - Get generated options (csv files)
def get_all_options():
    global path_all
    global all_options

    if path_all is None:
        return []

    # print("get all options: {}".format(path_all))
    path, dirs, files = next(os.walk(path_all))
    all_options = [{'label': str(files[i]).split('_')[1], 'value': files[i]} for i in range(1, len(files))]
    # print("get all options: {}".format(all_options))

    return all_options


def bar_chart_figure():
    if path_all == '':
        return 0

    bar_all_options = get_all_options()
    titles = [str(op).split('_')[1] for op in bar_all_options]

    color_names = COLOR_NAMES
    column_names = ['Option', 'Green', 'Soft Green', 'Soft Red', 'Red']

    df_all = pd.DataFrame(columns=column_names)
    df_all['Option'] = titles
    choices = COLOR_RGB

    for i in range(1, len(bar_all_options) + 1):
        df = pd.read_csv(r"{}\{}".format(path_all, bar_all_options[i - 1]['value']), index_col=False)
        df = color_range(df)

        for tmp in range(0, len(color_names)):
            df_all.loc[df_all['Option'] == titles[i - 1], color_names[tmp]] = len(df[df.Color == choices[tmp]])

    traces = []

    for i in range(0, len(color_names)):
        traces.append(go.Bar(x=df_all['Option'],
                             y=df_all[color_names[i]],
                             name=color_names[i],
                             text=df_all[color_names[i]],
                             marker={'color': choices[i]},
                             )
                      )

    layout1 = go.Layout(

        title={'text': "BRE Comparsion",
               'xanchor': 'left',
               'yanchor': 'top'
               },

        title_font={'size': 20,
                    'family': 'sans-serif',
                    'color': '#efb636'
                    },

        legend={'orientation': "h",
                'yanchor': "bottom",
                'y': 1.02,
                'xanchor': "right",
                'x': 1}
    )

    fig = go.Figure(data=traces, layout=layout1)

    fig.update_yaxes(title_text="Number",
                     gridcolor=GRAPH_LINES_COLOR,
                     linecolor=GRAPH_LINES_COLOR,
                     gridwidth=bar_chart_grid_width,
                     linewidth=bar_chart_line_width,
                     zerolinecolor=GRAPH_LINES_COLOR),

    fig.update_xaxes(title_text='Option',
                     gridcolor=GRAPH_LINES_COLOR,
                     linecolor=GRAPH_LINES_COLOR,
                     gridwidth=bar_chart_grid_width,
                     linewidth=bar_chart_line_width,
                     zerolinecolor=GRAPH_LINES_COLOR)

    fig.update_layout(hovermode='closest',
                      plot_bgcolor=PLOT_BGCOLOR,
                      paper_bgcolor=PAPER_BGCOLOR,
                      font={"color": "gray", 'family': 'sans-serif', 'size': 15}
                      )
    return fig


# COLOR RANGE for different ratio
def color_range(df):
    conditions = [
        (df['Scenario2/Scenario1'] <= 0.5),
        (df['Scenario2/Scenario1'] > 0.5) & (df['Scenario2/Scenario1'] <= 0.7),
        (df['Scenario2/Scenario1'] > 0.7) & (df['Scenario2/Scenario1'] <= 0.8),
        (df['Scenario2/Scenario1'] > 0.8),
    ]
    choices = COLOR_RGB[::-1]

    # Creating column with proper color
    df['Color'] = np.select(conditions, choices)
    return df


# COLOR RANGE BRE CRITERIUM - range for sortating by 'meets bra criterium'
def color_range_BRE(df):
    conditions = [
        (df['Scenario2/Scenario1'] < 0.8),
        (df['Scenario2/Scenario1'] >= 0.8),
    ]
    choices = COLORRGB_BRE

    # Creating column with proper color
    df['Color'] = np.select(conditions, choices)
    return df


# Encoding image based on path parameter
def encode_image(image_path):
    encoded_image = base64.b64encode(open(image_path, 'rb').read())
    return 'data:image/Jpeg;base64,{}'.format(encoded_image.decode())


# GET PROPER IMG PATH
# windows number from graph
# Option_picked- creating proper image path based on picked option
def get_images(window_number, option_picked):
    global img_base_path
    option_path = str(option_picked).split('_')[1]  # Get project name, between underscores

    directory = ('{}\{}\VSC'.format(img_base_path, option_path))
    path, dirs, files = next(os.walk(directory))

    # Find image based on window number
    file = ''
    for index, name in enumerate(files):
        if name.find(window_number) != -1:
            file = files[index]
            break

    return "{}\{}".format(directory, file)


def parse_contents(contents, number):
    margin = 0 if number == 0 else 1

    return html.Div([html.H4('Clicked image:',
                             style={'fontSize': 18,
                                    'fontFamily': 'sans-serif',
                                    'color': '#efb636',
                                    # 'marginTop': '10%'
                                    'marginTop': '{}%'.format(75 * margin)
                                    }
                             ),
                     html.Img(src=contents,
                              style={'height': '95%',
                                     'width': '95%',
                                     'marginLeft': '30px',
                                     'marginTop': '{}px'.format('5px')
                                     }
                              )
                     ])


def get_upload_component(id):
    return du.Upload(
        id=id,
        max_file_size=1800,  # 1800 Mb
        filetypes=['csv', 'zip'],
        upload_id='uploaded_folder',  # Unique session id
    )


def open_zip(file_name):
    if 'Data' not in os.listdir('{}'.format(UPLOAD_DIRECTORY)):
        os.mkdir('{}/Data'.format(UPLOAD_DIRECTORY))

    with ZipFile(file_name, 'r') as zip:
        # zip.printdir()
        zip.extractall('{}/Data'.format(UPLOAD_DIRECTORY))
    # get_a_list('{}/Data/Data'.format(UPLOAD_DIRECTORY))

def update_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])


def default_graph():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=[0], y=[0],
                             mode='markers',
                             marker={'size': 1,
                                     'opacity': 1,
                                     'color': 'rgb(255,255,255)',
                                     'line': {'width': 1.5,
                                              'color': 'black'},
                                     }, ))
    fig['layout'].update(
        title_text="Upload data and choose proper option",
        title_x=0.5,
        showlegend=False,
        height=450,
        plot_bgcolor=PLOT_BGCOLOR,
        paper_bgcolor=PAPER_BGCOLOR,
        font={"color": "gray",
              'family': 'sans-serif',
              'size': 15})

    fig.update_yaxes(title_text="Y variable",
                     gridcolor=GRAPH_LINES_COLOR,
                     linecolor=GRAPH_LINES_COLOR,
                     gridwidth=0.3, linewidth=0.3,
                     zerolinecolor=GRAPH_LINES_COLOR),

    fig.update_xaxes(title_text='X variable',
                     gridcolor=GRAPH_LINES_COLOR,
                     linecolor=GRAPH_LINES_COLOR,
                     gridwidth=0.3,
                     linewidth=0.3,
                     zerolinecolor=GRAPH_LINES_COLOR)

    fig.update_annotations(font={'size': 20,
                                 'family': 'sans-serif',
                                 'color': '#efb636'})
    return fig

clear_directory(UPLOAD_DIRECTORY)
print(os.listdir('{}'.format(UPLOAD_DIRECTORY)))

server = Flask(__name__)

app = dash.Dash('VSC-analysis', external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# server = app.server

@server.route("/download1/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


UPLOAD_FOLDER_ROOT = r".\Project"

du.configure_upload(app, UPLOAD_FOLDER_ROOT)

app.layout = html.Div(children=[

    html.Div(children=[

        html.Div(children=[

            html.Div(children=[

                html.H1(children='VSC analysis \n',
                        style={
                            'textAlign': 'center',
                            'color': '#efb636'
                        })
            ],
                className='col-8',
                style={'padding-top': '12%'}
            )
        ],

            style={'height': '4%',
                   'background-color': LEFT_MENU_COLOR,
                   'border': '0px solid black',
                   'marginLeft': '10px'
                   }
        ),
        html.Div([
            html.Div(
                [
                    # get_upload_component(id='dash-uploader'),
                    dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    ["Drag and drop or select a file to upload."]
                                ),
                                style={
                                    "width": "90%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                                multiple=True,
                            ),
                    html.Div(id='callback-output'),
                    dcc.Link(html.Button(id='Refresh',
                                         n_clicks=0,
                                         children='Refresh',
                                         style={'marginTop': '10px',
                                                'marginLeft': '0px',
                                                'color': '#657895',
                                                'border': '1px solid {}'.format(GRAPH_LINES_COLOR),
                                                'background': LEFT_MENU_COLOR
                                                }
                                         ), refresh=True, href='/page-1'),
                ],
                style={
                    'textAlign': 'center',
                    'width': '100%',
                    'padding': '10px',
                    'display': 'inline-block'
                }),
            html.H4("File List", style= TEXT_STYLE),
            html.Ul(id="file-list"),
            html.H4('Choose option:', style=TEXT_STYLE),

            dcc.Checklist(
                id='option_picker',
                # value = def_option,
                options=get_all_options(),
                labelStyle={'display': 'block'},
                style=CHECKLIST_STYLE
            ),

            html.H4('Choose variable:',
                    style=TEXT_STYLE),

            dcc.RadioItems(
                id='variable_picker',
                labelStyle={'display': 'block'},
                value=def_variable,
                options=all_VCS,
                style=RADIOITEMS_STYLE
            ),

            html.H4('Sort by:',
                    style=TEXT_STYLE),

            dcc.RadioItems(
                id='sortby_picker',
                labelStyle={'display': 'block'},
                value=def_sort_by,
                options=RADIOITEM_OPTIONS_SORT,
                style=RADIOITEMS_STYLE
            ),

            html.H4('Show statistic: ', style=TEXT_STYLE),

            dcc.Checklist(
                id='plot_picker',
                options=DROPDOWN_SHOW,
                labelStyle={'display': 'block'},
                style=CHECKLIST_STYLE
            )
        ],
            style={
                'padding-top': '20%'
            }),

    ], style={'display': 'inline-block',
              'verticalAlign': 'top',
              'width': '21%',
              'marginLeft': '0px',
              'marginTop': '0px',
              'border': '0px solid black',
              'height': '1200px',
              'color': '#657895',
              'white-space': 'nowrap',
              'text-overflow': 'ellipsis',
              'background-color': LEFT_MENU_COLOR
              }
    ),

    html.Div(children=[
        html.Div(children=[

            dcc.Graph(
                id='my_graph',
                figure=default_graph(),
                clear_on_unhover=True
            ),
            dcc.Tooltip(id="graph-tooltip",
                        loading_text="LOADING",
                        direction="top")

        ], style={'display': 'inline-block',
                  'width': '72%',
                  'font-family': 'sans-serif',
                  'marginTop': '0%',
                  'marginLeft': '5%',
                  'marginBottom': '5%',
                  }
        ),

        html.Div(id='images',
                 style={'display': 'inline-block',
                        'verticalAlign': 'top',
                        'width': '18%',
                        'marginTop': '115px',
                        'marginLeft': '0px',
                        'background-color': PLOT_BGCOLOR
                        }
                 ),

        html.Div(children=[
            dbc.Collapse([
                html.H4('Saved data:',
                        style={'fontSize': 20,
                               'fontFamily': 'sans-serif',
                               'color': '#efb636',
                               }
                        ),

                dash_table.DataTable(id='datatable',
                                     columns=TABLE_COLUMNS,
                                     data=[],
                                     tooltip_data=[],
                                     row_deletable=True,
                                     sort_action="native",
                                     sort_mode="multi",
                                     style_cell=TABLE_CELL_STYLE,
                                     style_header=TABLE_HEADER_STYLE,
                                     style_data=TABLE_DATA_STYLE
                                     ),
                dcc.Tooltip(id="table-tooltip",
                            loading_text="LOADING",
                            direction="top"),

                html.Button(id='Reset_button',
                            n_clicks=0,
                            children='Reset Table',
                            style={'marginTop': '10px',
                                   'marginLeft': '0px',
                                   'color': 'white',
                                   'border': '1px solid {}'.format(GRAPH_LINES_COLOR),
                                   'background': PLOT_BGCOLOR
                                   }
                            ),

                html.Button(id='Generate_excel',
                            n_clicks=0,
                            children='Save to excel',

                            style={'marginLeft': '10px',
                                   'marginTop': '10px',
                                   'color': 'white',
                                   'border': '1px solid {}'.format(GRAPH_LINES_COLOR),
                                   'background': PLOT_BGCOLOR
                                   }
                            ),

            ],
                id="collapse",
                is_open=False,
                style={'marginTop': '0px'}

            )
        ], style={
            'display': 'inline-block',
            'marginLeft': '100px',
            'width': '65%'
        }),

        html.Div(children=[
            dbc.Collapse(
                [dcc.Graph(
                    id='Bar_chart',
                    figure=bar_chart_figure()
                )
                ],
                id="collapse2",
                is_open=False,
            )
        ], style={
            'display': 'inline-block',
            'verticalAlign': 'top',
            'width': '70%',
            'marginTop': '20px',
            'marginLeft': '90px'
        }),

    ], style={'display': 'inline-block',
              'verticalAlign': 'top',
              'width': '79%',
              'marginLeft': '0px',
              'marginTop': '0px',
              'border': '0px solid black',
              'height': '1200px',
              'maxHeight': '1200px',
              'overflow': 'auto',
              'background-color': PLOT_BGCOLOR,
              'position': 'absolute'
              }
    ),
    html.Div(html.H4(id='test'))
])


@app.callback(Output('option_picker', 'options'),
              # [Input('option_picker', 'value'),
              [Input('Refresh', 'n_clicks')])
def option_refresh(value):
    open_files()
    # open_zip('{}/Data.zip'.format(UPLOAD_DIRECTORY))

    return get_all_options()


@app.callback(Output('Bar_chart', 'figure'),
              # [Input('plot_picker', 'value'),
              [Input('Refresh', 'n_clicks')])
def option_refresh(value):
    return bar_chart_figure()


# @app.callback(
#     Output('callback-output', 'children'),
#     [Input("upload-data", "filename"), Input("upload-data", "contents")]
# )
#
# def get_a_list(filenames):
#     # open_zip('{}\Data.zip'.format(urlquote(UPLOAD_DIRECTORY)))
#
#     global img_base_path
#     global path_all
#     global main_project_name
#     global project_number
#     global all_options
#     global def_option
#
#     main_project_name = os.listdir('{}\Data'.format(urlquote(UPLOAD_DIRECTORY)))
#
#     project_number = str(main_project_name[0]).split('-')[1]
#
#     img_base_path = r'{}\Data\{}\Results'.format(urlquote(UPLOAD_DIRECTORY), main_project_name[0])
#     path_all = r'{}\Data\{}\{}-3d-VSC-APSH-template_Waldram\Reports'.format(urlquote(UPLOAD_DIRECTORY), main_project_name[0], project_number)
#     all_options = get_all_options()
#     def_option = all_options[0]
#     # bar_chart_figure()
#     return "Uploaded successfully!"


@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    [Input("my_graph", "hoverData"),
     Input('option_picker', 'value')]
)
def display_hover(hoverData, option_picked):
    if hoverData is None:
        return False, no_update, no_update
    if option_picked is None:
        return False, no_update, no_update

    if hoverData:
        window_number = hoverData['points'][0]['x']
        graph_number = hoverData['points'][0]['curveNumber']
    else:
        window_number = 'W120'
        graph_number = '0'

    source = get_images(window_number, option_picked[graph_number])
    bbox = hoverData['points'][0]['bbox']

    children = [
        html.Div([
            html.Img(src=encode_image(source),
                     style={"width": "100%"}
                     ),

            html.H5(id='Tooltip_number',
                    children='Window number:  {}'.format(window_number),
                    style={'fontSize': 18,
                           'fontFamily': 'sans-serif'
                           }
                    )
        ], style={'width': '250px',
                  'white-space': 'normal',
                  'background_color': GRAPH_LINES_COLOR
                  })
    ]

    return True, bbox, children


@app.callback(Output("collapse", "is_open"),
              [Input("plot_picker", "value")],
              [State("collapse", "is_open")],
              )
def toggle_collapse(n, is_open):
    if n is None:
        return False

    if 'Table' in n:
        return True
    return False


@app.callback(Output('collapse2', 'is_open'),
              [Input('plot_picker', 'value')],
              [State('collapse2', 'is_open')])
def bar_plot_collapse(n, is_open):
    if n is None:
        return False

    if 'Bar plot' in n:
        return True
    return False


# CREATING IMAGES
@app.callback(Output('images', 'children'),
              [Input('my_graph', 'clickData'),
               Input('option_picker', 'value')])
def print_images(clickData, option_picked):
    if clickData:
        window_number = clickData['points'][0]['x']
        graph_number = clickData['points'][0]['curveNumber']
    else:
        window_number = 'W120'
        graph_number = '0'

    source = []

    for i in range(1, len(option_picked) + 1):
        source.append(get_images(window_number, option_picked[graph_number]))

    children = [parse_contents(encode_image(imgs), number) for number, imgs in enumerate(source)]
    return children


# CREATE GRAPH
@app.callback(Output('my_graph', 'figure'),
              [Input('option_picker', 'value'),
               Input('sortby_picker', 'value'),
               Input('variable_picker', 'value'),
               Input('my_graph', 'clickData')])
def graph_update(option, sort_by, variable, clickData):
    global path_all

    # print("graph update: {}".format(path_all))
    titles = [str(op).split('_')[1] for op in option]

    if clickData:
        clicked = clickData['points'][0]['x']
    else:
        clicked = '0'

    fig = make_subplots(rows=len(option),
                        cols=1, subplot_titles=titles,
                        shared_xaxes=False)

    for i in range(1, len(option) + 1):

        df = pd.read_csv(r"{}\{}".format(path_all, option[i - 1]), index_col=False)

        if sort_by == 'Window Ref':

            df['Window_int'] = df['Window Ref']
            df['Window_int'] = df['Window_int'].apply(lambda x: int(str(x)[1:]))

            df.sort_values('Window_int', inplace=True)
        else:
            df.sort_values(sort_by, inplace=True)

        df['Size'] = 12
        df['Opacity'] = 0.6

        if sort_by == 'Meets BRE Criteria':
            df = color_range_BRE(df)
        else:
            df = color_range(df)

        df.loc[df['Window Ref'] == clicked, 'Color'] = CLICKED_COLOR
        df.loc[df['Window Ref'] == clicked, 'Size'] = CLICKED_SIZE
        df.loc[df['Window Ref'] == clicked, 'Opacity'] = CLICKED_OPACITY

        x_variable = df['Window Ref']
        y_variable = df[variable]

        fig.add_trace(go.Scatter(
            x=x_variable,
            y=y_variable,
            mode='markers',
            marker={'size': df['Size'],
                    'opacity': df['Opacity'],
                    'color': df['Color'],
                    'line': {'width': 1.5,
                             'color': 'black'},
                    },

        ), row=i, col=1)

        fig['layout'].update(
            showlegend=False,
            height=450 * i,
            plot_bgcolor=PLOT_BGCOLOR,
            paper_bgcolor=PAPER_BGCOLOR,
            font={"color": "gray",
                  'family': 'sans-serif',
                  'size': 15},
        )

        fig.update_yaxes(title_text=variable,
                         gridcolor=GRAPH_LINES_COLOR,
                         linecolor=GRAPH_LINES_COLOR,
                         gridwidth=0.3, linewidth=0.3,
                         zerolinecolor=GRAPH_LINES_COLOR,
                         row=i, col=1),

        fig.update_xaxes(title_text='Window Ref',
                         gridcolor=GRAPH_LINES_COLOR,
                         linecolor=GRAPH_LINES_COLOR,
                         gridwidth=0.3,
                         linewidth=0.3,
                         zerolinecolor=GRAPH_LINES_COLOR,
                         row=i, col=1)

        fig.update_annotations(font={'size': 20,
                                     'family': 'sans-serif',
                                     'color': '#efb636'},
                               )
        fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


# CREATE TABLE
# Create table based on data from proper csv file
# change_id  ->  checking if n_click from 'Reset_button' has changed if so, button was pressed -> clear data
@app.callback(Output('datatable', 'data'),
              [Input('my_graph', 'clickData'),
               Input('Reset_button', 'n_clicks')],
              [State('option_picker', 'value'),
               State('sortby_picker', 'value'),
               State('datatable', 'data')])
def print_table(hoverData, nclicks, option, sort_by, data):
    Window_number = hoverData['points'][0]['x']
    graph_number = hoverData['points'][0]['curveNumber']

    df = pd.read_csv(r"{}\{}".format(path_all, option[graph_number]), index_col=False)
    df.sort_values(sort_by, inplace=True)

    df = color_range(df)
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'Reset_button' in changed_id:
        data.clear()

    else:

        data.append({'Option': str(option[graph_number]).split('_')[1],
                     'Window_ref': Window_number,
                     'Floor': df[df['Window Ref'] == Window_number]['Floor'],
                     'VSC_base': round(df[df['Window Ref'] == Window_number]['Vsc Scenario base'], 1),
                     'VSC_scen_2': round(df[df['Window Ref'] == Window_number]['Vsc Scenario2'], 1),
                     'ratio': round(df[df['Window Ref'] == Window_number]['Scenario2/Scenario1'], 2),
                     'Window_orien': df[df['Window Ref'] == Window_number]['Window Orientation']})

    return data


# RESET BUTTON
# Create reset button for clearing table
@app.callback(Output('Reset_button', 'n_clicks'),
              [Input('Reset_button', 'n_clicks')])
def button_reset(reset):
    return 0


# GENERATE EXCEL
# Generating excel with dataframe from table,
# Add image to excel, based on window ref from data table
@app.callback(Output('Generate_excel', 'n_clicks'),
              [Input('Generate_excel', 'n_clicks'),
               Input('datatable', 'data'),
               Input('option_picker', 'value')])
def generate_excel(n_clicks, data, option):
    global path_all

    df_img = pd.DataFrame(data)
    df_img['VSC_base'] = df_img['VSC_base'].str[0]
    df_img['VSC_scen_2'] = df_img['VSC_scen_2'].str[0]
    df_img['ratio'] = df_img['ratio'].str[0]
    df_img['Window_orien'] = df_img['Window_orien'].str[0]
    df_img['Floor'] = df_img['Floor'].str[0]

    path, dirs, files = next(os.walk(path_all))
    proper = []
    for row in df_img['Option']:
        for name in files:
            if name.find(row) != -1:
                proper.append(name)
                break

    df_img = df_img.reset_index()
    writer = pd.ExcelWriter('Generated_Data.xlsx', engine='xlsxwriter')

    df_img.to_excel(writer, sheet_name='Generated_Data', index=False)
    worksheet = writer.sheets['Generated_Data']

    worksheet.set_column(0, 0, 15)
    worksheet.set_column(1, 1, 25)
    worksheet.set_column(2, 7, 15)
    worksheet.set_column(8, 8, 24)

    for i in range(len(df_img)):
        worksheet.set_row(i + 1, 110)
        worksheet.insert_image("I{}".format(i + 2), get_images(df_img['Window_ref'][i], proper[i]),
                               {'x_scale': 0.2, 'y_scale': 0.2})
    writer.save()
    return 0


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


@app.callback(
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

# #
#
#
def open_files():
    global path_all
    global img_base_path
    global def_option

    open_zip('{}/Data.zip'.format(UPLOAD_DIRECTORY))
    main_project_name = os.listdir('{}/Data/Data'.format(urlquote(UPLOAD_DIRECTORY)))

    project_number = str(main_project_name[0]).split('-')[1]

    img_base_path = r'{}/Data/Data/{}/Results'.format(urlquote(UPLOAD_DIRECTORY), main_project_name[0])
    path_all = r'{}/Data/Data/{}/{}-3d-VSC-APSH-template_Waldram/Reports'.format(urlquote(UPLOAD_DIRECTORY), main_project_name[0], project_number)
    all_options = get_all_options()
    def_option = all_options[0]


if __name__ == '__main__':
    app.run_server(debug= False)
