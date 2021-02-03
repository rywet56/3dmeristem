import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
import numpy as np
import copy as cp
import plotly.graph_objects as go

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

path = DATA_PATH.joinpath("confocal_states0-FilterWUSCLVtop100.csv")
ref = pd.read_csv(path, sep=",", index_col=0, decimal=".")
ref_genes = ref.columns.values.tolist()[5:28]

path = DATA_PATH.joinpath("ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100_1000genes.txt")
sdge = pd.read_csv(path, sep=",", index_col=0, decimal=".")
sdge = sdge.T
sdge_genes = sdge.columns.values.tolist()

ref_expr_card = html.Div(
    [
        html.Div([
            html.P("this binary expression has been reconstructed from 2D stacked confocal images"),
            dcc.Dropdown(id='ref_expr_dropdown', multi=False,
                         options=[{'label': x, 'value': x} for x in ref_genes],
                         value="AT1G62360"),
            dcc.Graph(id='ref_expr_graph', figure={})
        ], className="colm", style={"max-width": "100%"})
    ], className="rowm"
)

pre_expr_card = html.Div(
    [
        html.Div([
            html.P("this continuous expression has been reconstructed using novosparc"),
            dcc.Dropdown(id='pre_expr_dropdown', multi=False,
                         options=[{'label': x, 'value': x} for x in sdge_genes],
                         value="AT1G01010", style={"background-color": "black"}),
            dcc.Graph(id='pre_expr_graph', figure={})
        ], className="colm", style={"max-width": "100%"})
    ], className="rowm", style={"padding": "2rem"}
)

pre_expr_menu_card = html.Div(
    [
        html.Div([
            html.H5("Range of Values:"),
            dcc.RangeSlider(id='slider_pre', min=0, max=0, value=[],
                            marks={}, step=None, allowCross=False,
                            className="slider_expr", verticalHeight=800),
            html.H5("Color Scheme:"),
            dcc.RadioItems(id='color_code',
                           options=[
                               {'label': 'blue-yellow-red', 'value': 'byr'},
                               {'label': 'yellow-red', 'value': 'yr'},
                               {'label': 'red-green', 'value': 'rg'}
                           ],
                           value='byr',
                           # labelStyle={'display': 'inline-block', "box-sizing":"border-box", "margin-bottom":"0"},
                           # inputStyle={"margin-left":"-1.25rem", "box-sizing":"border-box", "padding":"0",
                           # "position":"absolute", "margin-top":"0.3rem", "overflow":"visible"},
                           inputStyle={"margin-right": "5px"}
                           # style={"position":"relative", "display":"block", "padding-left":"1.25rem",
                           # "box-sizing":"border-box", "text-align":"left"}
                           )
        ], className="colm", style={"max-width": "100%"})

    ], className="rowm", style={"padding": "2rem"}
)

ref_expr_menu_card = html.Div(
    [
        html.Div([
            html.H5("Color Scheme:"),
            dcc.RadioItems(id='color_code_ref',
                           options=[
                               {'label': 'blue-yellow-red', 'value': 'byr'},
                               {'label': 'yellow-red', 'value': 'yr'},
                               {'label': 'red-green', 'value': 'rg'}
                           ],
                           value='byr',
                           inputStyle={"margin-right": "5px"}
                           )
        ], className="colm", style={"max-width": "100%"})
    ], className="rowm", style={"padding": "2rem"}
)

# gg = dcc.Graph(figure=
#                go.Figure(data=[go.Scatter3d(x=ref['x'], y=ref['y'], z=ref['z'], mode='markers',
#                                             marker=dict(color=ref["AT1G62360"],
#                                                         showscale=True, colorscale=["yellow", "red"],
#                                                         colorbar=dict(thickness=30, tickcolor="white",
#                                                                       tickfont=dict(color="white"))),
#                                             showlegend=False
#
#                                             )],
#                          layout=go.Layout(scene=dict(bgcolor="#060606",
#                                                      xaxis=dict(showgrid=False, zeroline=False,
#                                                                 visible=False),
#                                                      yaxis=dict(showgrid=False, zeroline=False,
#                                                                 visible=False),
#                                                      zaxis=dict(showgrid=False, zeroline=False,
#                                                                 visible=False)
#                                                      ),
#                                           margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#060606"
#                                           )
#                          )
#                )

# page_1 = html.Div([
#     html.Div(
#         [
#             html.Div([ref_expr_card], className="colm",
#                      style={"border": "0.25rem solid #2a9fd6", "border-radius": "2.5%", "max-width": "50%"}),
#             html.Div([pre_expr_card], className="colm space-left",
#                      style={"border": "0.15rem solid #2a9fd6", "border-radius": "2.5%", "background-color": "#282828",
#                             "max-width": "50%"}),
#         ], className="rowm"
#     ),
#     html.Div(
#         [
#             html.Div([ref_expr_menu_card], className="colm",
#                      style={"border": "0.25rem solid #2a9fd6", "border-radius": "2.5%", "max-width": "50%"}),
#             html.Div([pre_expr_menu_card], className="colm space-left",
#                      style={"border": "0.15rem solid #2a9fd6", "border-radius": "2.5%", "background-color": "#282828",
#                             "max-width": "50%"}),
#         ], className="rowm space-up"
#     )
# ], className="colm", style={"background-color": "#060606", "max-width": "100%"}
#     # CHANGED THAT to 100% ! WORKS NOW With new style sheet
# )

# pre_expr_card = html.Div(
#     [
#         html.Div([
#             # html.P("this continuous expression has been reconstructed using novosparc"),
#             ref_expr_graph
#         ], className="colm", style={"max-width": "100%", "width":"100%"})
#     ], className="rowm", style={"padding": "2rem"}
# )

ref_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([
                html.Div(["some text"], className="colm")
            ], className="rowm",  style={"margin":"0.5rem"}),
            # dropdown menu
            html.Div([
                html.Div([
                    dcc.Dropdown(id='ref_expr_dropdown', multi=False,
                                 options=[{'label': x, 'value': x} for x in ref_genes],
                                 value="AT1G62360")
                ], className="colm")
            ], className="rowm"),
            # the plot
            html.Div([
                html.Div([dcc.Graph(id='ref_expr_graph', figure={})], className="colm")], className="rowm")
        ], className="colm")], className="rowm"),

        # The menu part of the card
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Color Scheme:"),
                        dcc.RadioItems(id='color_code_ref',
                                       options=[
                                           {'label': 'blue-yellow-red', 'value': 'byr'},
                                           {'label': 'yellow-red', 'value': 'yr'},
                                           {'label': 'red-green', 'value': 'rg'}],
                                       value='byr')
                    ], className="colm"),
                ], className="rowm")
            ], className="colm")
        ], className="rowm"),
    ], className="colm"),
], className="rowm expr_card", style={"margin":"1rem 0.5rem 0 1rem"}
)

pre_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([
                html.Div(["some text"], className="colm")
            ], className="rowm", style={"margin":"0.5rem"}),
            # dropdown menu
            html.Div([
                html.Div([
                    dcc.Dropdown(id='pre_expr_dropdown', multi=False,
                                 options=[{'label': x, 'value': x} for x in sdge_genes],
                                 value="AT1G01010")
                ], className="colm")
            ], className="rowm"),
            # the plot
            html.Div([
                html.Div([dcc.Graph(id='pre_expr_graph', figure={})], className="colm")], className="rowm")
        ], className="colm")], className="rowm"),

        # The menu part of the card
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Color Scheme:"),
                        dcc.RadioItems(id='color_code',
                                       options=[{'label': 'blue-yellow-red', 'value': 'byr'},
                                           {'label': 'yellow-red', 'value': 'yr'},
                                           {'label': 'red-green', 'value': 'rg'}],
                                       value='byr')
                    ], className="colm"),
                ], className="rowm"),
                html.Div([
                    html.Div([
                        html.H5("Range of Values:"),
                        dcc.RangeSlider(id='slider_pre', min=0, max=0, value=[],
                                        marks={}, step=None, allowCross=False,
                                        className="slider_expr", verticalHeight=800),
                    ], className="colm")
                ], className="rowm")
            ], className="colm")
        ], className="rowm"),
    ], className="colm"),
], className="rowm expr_card", style={"margin":"1rem 1rem 0 0.5rem"}
)

page_1 = html.Div([
    # reference expression
    html.Div([ref_card], className="colm", style={"max-width": "50%"}),
    # predicted expression
    html.Div([pre_card], className="colm", style={"max-width": "50%"})
], className="rowm")


# KEEP FOR TESTs
# page_1 = html.Div([
#     html.Div(
#         [
#             html.Div([ref_expr_graph], className='col-4 offset-0', style={"border":"0.25rem solid #f80", "border-radius": "2.5%"}),
#             html.Div([ref_expr_graph], className='col-4 offset-0', style={"border":"0.25rem solid #f80", "border-radius": "2.5%"}),
#             html.Div([ref_expr_graph], className='col-4 offset-0', style={"border":"0.25rem solid #f80", "border-radius": "2.5%"})
#         ], className='row'
#     ),
# ], style={"background-color": "#060606"})


# Plot of reference expression
@app.callback(Output('ref_expr_graph', 'figure'),
              [Input('ref_expr_dropdown', 'value'), Input('color_code_ref', 'value')])
def update_ref_expr(val_chosen_2, color_code):
    # obtain color code
    col_code = []
    if color_code == 'byr':
        col_code = ["blue", "yellow", "red"]
    elif color_code == 'yr':
        col_code = ["yellow", "red"]
    elif color_code == 'rg':
        col_code = ["red", "green"]

    # plot figures
    fig = go.Figure(data=[go.Scatter3d(x=ref['x'], y=ref['y'], z=ref['z'], mode='markers',
                                       marker=dict(color=ref[val_chosen_2],
                                                   showscale=True, colorscale=col_code,
                                                   colorbar=dict(thickness=30, tickcolor="white",
                                                                 tickfont=dict(color="white"))),
                                       showlegend=False

                                       )],
                    layout=go.Layout(scene=dict(bgcolor="#282828",
                                                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                yaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                zaxis=dict(showgrid=False, zeroline=False, visible=False)
                                                ),
                                     margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#282828"
                                     )
                    )
    return fig


# Plot of predicted expression
@app.callback([Output('slider_pre', 'min'), Output('slider_pre', 'max'),
               Output('slider_pre', 'marks'), Output('slider_pre', 'value')],
              [Input('pre_expr_dropdown', 'value')])
def update_range_slider_pre(val_chosen_2):
    # get currently selected expression values
    expr = sdge[val_chosen_2].tolist()
    MIN = min(expr)
    MAX = max(expr)
    # generate steps
    no_steps = 1000
    RANGE = MAX - MIN
    step_size = round(RANGE / no_steps, 4)
    values = np.arange(MIN, MAX, step_size).tolist()
    MARKS = {v: "" for v in values}
    MARKS[MAX] = ""  # to make sure that the MAX value can also be selected
    return MIN, MAX, MARKS, [MIN, MAX]


@app.callback(Output('pre_expr_graph', 'figure'),
              [Input('pre_expr_dropdown', 'value'), Input('slider_pre', 'value'),
               Input('color_code', 'value')])
def update_pre_expr(val_chosen_2, ranges, color_code):
    # obtain color code
    col_code = []
    if color_code == 'byr':
        col_code = ["blue", "yellow", "red"]
    elif color_code == 'yr':
        col_code = ["yellow", "red"]
    elif color_code == 'rg':
        col_code = ["red", "green"]
    # apply Max and Min
    dge_cp = cp.deepcopy(sdge)
    dge_cp[dge_cp < ranges[0]] = ranges[0]
    dge_cp[dge_cp > ranges[1]] = ranges[1]
    dge_cp['x'] = ref['x'].tolist()
    dge_cp['y'] = ref['y'].tolist()
    dge_cp['z'] = ref['z'].tolist()

    fig_2 = go.Figure(data=[go.Scatter3d(x=dge_cp['x'], y=dge_cp['y'], z=dge_cp['z'], mode='markers',
                                         marker=dict(color=dge_cp[val_chosen_2],
                                                     showscale=True, colorscale=col_code,
                                                     colorbar=dict(thickness=30, tickcolor="white",
                                                                   tickfont=dict(color="white"))),
                                         showlegend=False

                                         )],
                      layout=go.Layout(scene=dict(bgcolor="#282828",
                                                  xaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  yaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  zaxis=dict(showgrid=False, zeroline=False, visible=False)
                                                  ),
                                       margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#282828"
                                       )
                      )

    # fig_2 = px.scatter_3d(data_frame=dge_cp, x='x', y='y', z='z',
    #                       color=val_chosen_2,
    #                       color_continuous_scale=col_code)
    # fig_2.update_layout(scene=dict(
    #     xaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     yaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     zaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     bgcolor='#7a8288'),
    #     margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#7a8288"
    # )
    del dge_cp
    return fig_2
