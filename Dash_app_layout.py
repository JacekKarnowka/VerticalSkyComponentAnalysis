from dash import html, dcc
import dash_bootstrap_components as dbc

# Import files
import app_main
import Styles


def get_layout():
    layout = html.Div(
        children=[
            # Left menu DIV
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.H1(
                                        children="VSC analysis \n",
                                        style={
                                            "textAlign": "center",
                                            "color": Styles.YELLOW_FONT_COLOR,
                                        },
                                    )
                                ],
                                style={"padding-top": "12%"},
                            )
                        ],
                        style={
                            "height": "4%",
                            "background-color": Styles.LEFT_MENU_COLOR,
                        },
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Upload(
                                        id="upload-data",
                                        children=html.Div(
                                            ["Select file to upload and click refresh"]
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
                                    dcc.Link(
                                        html.Button(
                                            id="Refresh",
                                            n_clicks=0,
                                            children="Refresh",
                                            style={
                                                "marginTop": "10px",
                                                "marginLeft": "0px",
                                                "color": Styles.LEFT_MENU_TEXT_COLOR,
                                                "border": "1px solid {}".format(
                                                    Styles.GRAPH_LINES_COLOR
                                                ),
                                                "background": Styles.LEFT_MENU_COLOR,
                                            },
                                        ),
                                        refresh=True,
                                        href="/",
                                    ),
                                ],
                                style={
                                    "textAlign": "center",
                                    "width": "100%",
                                    "padding": "10px",
                                    "display": "inline-block",
                                },
                            ),
                            html.H4("Uploaded file:", style=Styles.TEXT_STYLE),
                            html.Ul(id="file-list"),
                            html.H4("Choose option:", style=Styles.TEXT_STYLE),
                            # Option picker after uploading files
                            dcc.Checklist(
                                id="option_picker",
                                options=app_main.get_all_options(),
                                labelStyle={"display": "block"},
                                style=Styles.CHECKLIST_STYLE,
                            ),
                            html.H4("Choose variable:", style=Styles.TEXT_STYLE),
                            # Choose variable for plot X axis
                            dcc.RadioItems(
                                id="variable_picker",
                                labelStyle={"display": "block"},
                                value=app_main.def_variable,
                                options=app_main.all_VCS,
                                style=Styles.RADIOITEMS_STYLE,
                            ),
                            html.H4("Sort by:", style=Styles.TEXT_STYLE),
                            # Choose variable to sort by
                            dcc.RadioItems(
                                id="sortby_picker",
                                labelStyle={"display": "block"},
                                value=app_main.def_sort_by,
                                options=app_main.RADIOITEM_OPTIONS_SORT,
                                style=Styles.RADIOITEMS_STYLE,
                            ),
                            html.H4("Show statistic: ", style=Styles.TEXT_STYLE),
                            dcc.Checklist(
                                id="plot_picker",
                                options=app_main.DROPDOWN_SHOW,
                                labelStyle={"display": "block"},
                                style=Styles.CHECKLIST_STYLE,
                            ),
                        ],
                        style={"padding-top": "20%"},
                    ),
                ],
                style={
                    "display": "inline-block",
                    "width": "21%",
                    "height": "900px",
                    "color": Styles.LEFT_MENU_TEXT_COLOR,
                    "white-space": "nowrap",
                    "text-overflow": "ellipsis",
                    "background-color": Styles.LEFT_MENU_COLOR,
                },
            ),
            # Right menu DIV:
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                id="my_graph",
                                figure=app_main.default_graph(),
                                clear_on_unhover=True,
                            ),
                            dcc.Tooltip(
                                id="graph-tooltip",
                                loading_text="LOADING",
                                direction="top",
                            ),
                        ],
                        style={
                            "display": "inline-block",
                            "width": "72%",
                            "font-family": "sans-serif",
                            "marginTop": "0%",
                            "marginLeft": "5%",
                            "marginBottom": "5%",
                        },
                    ),
                    html.Div(
                        id="images",
                        style={
                            "display": "inline-block",
                            "verticalAlign": "top",
                            "width": "18%",
                            "marginTop": "115px",
                            "marginLeft": "0px",
                            "background-color": Styles.PLOT_BGCOLOR,
                        },
                    ),
                    html.Div(
                        children=[
                            dbc.Collapse(
                                [
                                    dcc.Graph(
                                        id="Bar_chart",
                                        figure=app_main.bar_chart_figure(),
                                    )
                                ],
                                id="collapse2",
                                is_open=False,
                            )
                        ],
                        style={
                            "display": "inline-block",
                            "verticalAlign": "top",
                            "width": "70%",
                            "marginTop": "20px",
                            "marginLeft": "90px",
                        },
                    ),
                ],
                style={
                    "display": "inline-block",
                    "verticalAlign": "top",
                    "width": "79%",
                    "marginLeft": "0px",
                    "marginTop": "0px",
                    "border": "0px solid black",
                    "height": "900px",
                    "maxHeight": "900px",
                    "overflow": "auto",
                    "background-color": Styles.PLOT_BGCOLOR,
                    "position": "absolute",
                },
            ),
            html.Div(html.H4(id="test")),
        ]
    )
    return layout
