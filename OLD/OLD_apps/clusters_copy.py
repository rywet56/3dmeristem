import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np
import dash
import copy as cp

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

path = DATA_PATH.joinpath("confocal_states0-FilterWUSCLVtop100.csv")
ref = pd.read_csv(path, sep=",", index_col=0, decimal=".")

path = DATA_PATH.joinpath("umap_clusters.csv")
umap = pd.read_csv(path, sep=",", index_col=0, decimal=".")
umap['cluster'] = [str(clust) for clust in umap['cluster'].tolist()]

path = DATA_PATH.joinpath("3d_clusters.csv")
clust = pd.read_csv(path, sep=",", index_col=0, decimal=".")
cluster_names = clust.columns.values.tolist()
clust = clust * 1000  # otherwise ZeroDivisionError in np.arrange() because stepsize is sometimes 0
clust['x'] = ref['x'].tolist()
clust['y'] = ref['y'].tolist()
clust['z'] = ref['z'].tolist()

clust_card = dbc.Card(
    [
        dbc.CardBody(
            [
                # html.H4("Clustering In UMAP Space", className="card-title"),
                # html.P("this is some clustering...",
                #        className="text-success"),
                html.Div(
                    [
                        html.Div([
                            dcc.Dropdown(id='umap_dropdown', multi=False,
                                         options=[{'label': x, 'value': x} for x in cluster_names],
                                         value='cluster_1')
                            ], className='col-2 offset-5'
                        )
                    ], className='row', style={"margin-bottom":"1rem"}
                ),
                dbc.Row([
                    dbc.Col(dcc.Graph(id='umap_graph', figure={})),
                    dbc.Col(dcc.Graph(id='3D_cluster_graph', figure={}))
                ])
            ]
        ),
    ], className="card text-white border-primary mb-3",
    style={"background-color": "#060606", "color": "white", "margin": "3rem", "margin-top": "3rem"}
)

# clust_card = html.Div([
#     dbc.Row(
#         dbc.Col(
#             dcc.Dropdown(id='umap_dropdown', multi=False,
#                          options=[{'label': x, 'value': x} for x in cluster_names],
#                          value='cluster_1'),
#         )),
#     dbc.Row([
#         dbc.Card([dbc.CardBody([dbc.Col(dcc.Graph(id='umap_graph', figure={}))])]),
#         dbc.Card([dbc.CardBody([dbc.Col(dcc.Graph(id='3D_cluster_graph', figure={}))])]),
#
#     ])
# ])

umap_clust_menu_card = dbc.Card(
    [
        dbc.CardBody(
            [
                # dbc.Row(dbc.Col(html.H2("3D Flower Meristem"))),
                html.H5("Range of Values:"),
                dcc.RangeSlider(id='slider_clust', min=0, max=0, value=[],
                                marks={}, step=None, allowCross=False,
                                className="custom-range", verticalHeight=800),
                html.H5("Color Scheme:"),
                dcc.RadioItems(id='color_code_clust',
                               options=[
                                   {'label': 'blue-yellow-red', 'value': 'byr'},
                                   {'label': 'yellow-red', 'value': 'yr'},
                                   {'label': 'red-green', 'value': 'rg'}
                               ],
                               value='byr',
                               inputStyle={"margin-right": "5px"}
                               )
            ], style={"background-color": "#060606"}
        )
    ], className="card text-white bg-secondary mb-3", style={"margin-right": "3rem", "margin-top": "1rem"}
)

page_2 = html.Div(
    [
        # clust_card,
        dbc.Row(dbc.Col(clust_card)),
        dbc.Row(dbc.Col(umap_clust_menu_card, width={'size': 6, 'offset': 6}))
    ], style={
        "background-color": "#060606",
        # "background-color":"#ffcc99",
        "min-height": "100vh", "min-width": "100vw"}
)


# layout = html.Div([
#     dbc.Row(
#         dbc.Col(
#             html.H2('3D UMAP cluster assignment '),
#             width={'size': 7, 'offset': 3}
#         )
#     ),
#     dbc.Row([
#         dbc.Col(
#             dcc.Dropdown(id='my-dropdown_4', multi=False,
#                          options=[{'label': x, 'value': x} for x in cluster_names],
#                          value='cluster_1'),
#             width={'size': 2, 'offset': 5}
#         )
#     ]),
#     dbc.Row([
#         dbc.Col(
#             dcc.Graph(id='graph-output_3', figure={}),
#             width={'size': 6, 'offset': 0}
#         ),
#         dbc.Col(
#             dcc.Graph(id='graph-output_4', figure={}),
#             width={'size': 6, 'offset': 0}
#         )
#     ])
# ])


@app.callback([Output('slider_clust', 'min'), Output('slider_clust', 'max'),
               Output('slider_clust', 'marks'), Output('slider_clust', 'value')],
              [Input('umap_dropdown', 'value')])
def update_range_slider_clust(val_chosen_2):
    # get currently selected expression values
    expr = clust[val_chosen_2].tolist()
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


@app.callback(Output('3D_cluster_graph', 'figure'),
              [Input('umap_dropdown', 'value'), Input('slider_clust', 'value'),
               Input('color_code_clust', 'value')])
def update_pre_clust(val_chosen_2, ranges, color_code):
    # obtain color code
    col_code = []
    if color_code == 'byr':
        col_code = ["blue", "yellow", "red"]
    elif color_code == 'yr':
        col_code = ["yellow", "red"]
    elif color_code == 'rg':
        col_code = ["red", "green"]

    # adjust range of values to display
    clust_cp = cp.deepcopy(clust)
    clust_cp[clust_cp < ranges[0]] = ranges[0]
    clust_cp[clust_cp > ranges[1]] = ranges[1]
    clust_cp['x'] = ref['x'].tolist()
    clust_cp['y'] = ref['y'].tolist()
    clust_cp['z'] = ref['z'].tolist()

    # create 3D cluster plot
    fig_2 = go.Figure(data=[go.Scatter3d(x=clust_cp['x'], y=clust_cp['y'], z=clust_cp['z'], mode='markers',
                                         marker=dict(color=clust_cp[val_chosen_2],
                                                     showscale=True, colorscale=col_code,
                                                     colorbar=dict(thickness=30, tickcolor="white",
                                                                   tickfont=dict(color="white"))),
                                         showlegend=False

                                         )],
                      layout=go.Layout(scene=dict(bgcolor="#060606",
                                                  xaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  yaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  zaxis=dict(showgrid=False, zeroline=False, visible=False)
                                                  ),
                                       margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#060606"
                                       )
                      )
    # fig_2 = px.scatter_3d(data_frame=clust_cp, x='x', y='y', z='z',
    #                       color=val_chosen_2, color_continuous_scale=col_code)
    # fig_2.update_layout(scene=dict(
    #     xaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     yaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     zaxis=dict(showgrid=False, zeroline=False, visible=False),
    #     bgcolor="#060606"),
    #     margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#060606"
    # )
    del clust_cp
    return fig_2


@app.callback(Output('umap_graph', 'figure'),
              [Input('umap_dropdown', 'value')])
def update_umap_clust(val_chosen_2):
    cols = px.colors.qualitative.Dark24[0:13]
    cluster_cols = [cols[int(cluster_no)] for cluster_no in umap['cluster']]
    clust_focus = val_chosen_2.split("_")[1]
    umap_sub = umap[umap['cluster'] == clust_focus]
    cluster_cols_sub = [cols[int(clust_focus)]] * umap_sub.shape[0]
    fig_1 = go.Figure(data=[go.Scatter(x=umap["UMAP_1"], y=umap["UMAP_2"], mode='markers',
                                       marker=dict(size=6, color=cluster_cols), opacity=0.3
                                       ),
                            go.Scatter(x=umap_sub["UMAP_1"], y=umap_sub["UMAP_2"], mode='markers',
                                       marker=dict(size=6, color=cluster_cols_sub), opacity=1
                                       )
                            ],
                      layout=go.Layout(showlegend=False, plot_bgcolor="#060606",
                                       margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#060606",
                                       xaxis=dict(visible=True, color="white", title=dict(text="UMAP1"), showline=True,
                                                  showgrid=False, zeroline=False),
                                       yaxis=dict(visible=True, color="white", title=dict(text="UMAP2"), showline=True,
                                                  showgrid=False, zeroline=False)
                                       )
                      )
    return fig_1
