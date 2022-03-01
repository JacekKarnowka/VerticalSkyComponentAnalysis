import dash
import dash_obj_in_3dmesh
from dash import Input, Output, State, html, no_update, Dash
from dash_obj_in_3dmesh import geometry_tools
from dash import dcc

model_name = "test" #.obj & .mtl files in data/obj

axis_template = {
    "showbackground": False,
    "visible" : False
}

plot_layout = {
    "title": "",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    "font": {"size": 12, "color": "white"},
    "showlegend": False,
    'uirevision':'same_all_the_time', #this keeps camera position etc the same when data changes.
    "scene": {
        "xaxis": axis_template,
        "yaxis": axis_template,
        "zaxis": axis_template,
        "aspectmode" : "data",
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}

def layout():
 return html.Div([dcc.Graph(
          id="graph",
          figure={
              "data": geometry_tools.import_geometry([model_name]),
              "layout": plot_layout,
          },
          config={"scrollZoom": True}, # activates wheel thingy on mouse to zoom and wotnot
      )])

app = Dash()
app.layout = layout

app.run_server()