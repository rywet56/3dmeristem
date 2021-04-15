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

path = DATA_PATH.joinpath("cluster_anno.csv")
clust_anno = pd.read_csv(path, sep=",")

clust_umap_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([
                html.Div([
                    html.H2(["single-cell clusters in UMAP space"], className="card-title-big"),
                ], className="colm"
                    # , style={"background-color": "red"}
                )
                # html.Div(["some text"], className="colm")
            ], className="rowm", style={"margin": "0.5rem"}),
            # the plot
            html.Div([
                html.Div([dcc.Graph(id='umap_graph', figure={})], className="colm")], className="rowm")
        ], className="colm")], className="rowm"),
    ], className="colm"),
], className="rowm"
)

clust_3d_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([html.Div([
                    html.H2(["3D Cluster Assignment"], className="card-title-big"),
                ], className="colm")], className="rowm", style={"margin": "0.5rem"}),
            # the plot
            html.Div([html.Div([
                dcc.Graph(id='3D_cluster_graph', figure={})
                ], className="colm")], className="rowm")
            ], className="colm")
        ], className="rowm"),

        # The menu part of the card
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5("Color Scheme:"),
                        dcc.RadioItems(id='color_code_clust',
                                       options=[
                                           {'label': 'blue-yellow-red', 'value': 'byr'},
                                           {'label': 'yellow-red', 'value': 'yr'},
                                           {'label': 'red-green', 'value': 'rg'}
                                       ], value='byr')
                    ], className="colm"),
                ], className="rowm"),
                html.Div([
                    html.Div([
                        html.H5("Range of Values:"),
                        dcc.RangeSlider(id='slider_clust', min=0, max=0, value=[],
                                        marks={}, step=None, allowCross=False,
                                        className="custom-range", verticalHeight=800)
                    ], className="colm")
                ], className="rowm")
            ], className="colm")
        ], className="rowm"),
    ], className="colm"),
], className="rowm"
)

# clust_data = "The UMAP plot (lower left plot) describes the lower dimensional representation of cells from the scRNA-seq " \
#              "dataset which was fed into novosparc + (together with marker genes) to predict the unknown 3D expression " \
#              "profiles shown in '3D expression'. Additionally cells were clustered into 12 groups, visualized with " \
#              "different colors. By using a probablistic assignment of single-cells from the scRNA-seq data to cells " \
#              "in the 3D model, the clusters in the UMAP plot could be mapped onto the 3D model (lower right plot). " \
#              "The color of a cell in the 3D model describes the probability that this cell belongs to a particular " \
#              "cluster (the one chosen through the dropdown). "
clust_data = 'The UMAP plot (lower left plot) describes the lower dimensional representation of nuclei from the snRNA-seq dataset generated from flower meristems. Each color represents one of the 12 cell clusters identified in the analysis. By using a probabilistic assignment of single cells from the snRNA-seq data to cells in the 3D model, the clusters in the UMAP plot could be mapped onto the 3D model (lower right plot). The color of a cell in the 3D model describes the probability that this cell belongs to a particular cluster (the one chosen through the dropdown menu).'
# usage = "The 3D Cluster Mapping makes it possible to view the location of single-cell UMAP clusters in the 3D " \
#         "mersitem model. This enables the verification and possibly the dicovery of new cell types in a 3D context."
# menu = "In order to visualize the 3D cluster assignment as well as the postion of cells in the UMAP plot, choose" \
#        "a cluster in the Drop-Down meny below. The choosen cluster will be highlighted in the UMAP plot and a 3D " \
#        "Cluster mapping for this selected cluster will be shown on the right. The color scheme as well as Maximum " \
#        "and Minimum for the displayed probabilities can be changed via the Radiobuttons and Rangeslider to " \
#        "optimize visualizaiton."
menu = 'In order to visualize the 3D cluster assignment as well as the position of cells in the UMAP plot, choose a cluster in the dropdown menu below. The chosen cluster will be highlighted in the UMAP plot and a 3D mapping result for this selected cluster will be shown on the right. The color scheme as well as the scale can be changed.'

# def get_clust_titles(gene, use_pep, pep):
#     if use_pep:
#         v = pep.loc[[gene], ["tair", "symbol", "top_spear_cor"]]
#         v = v.values.tolist()[0]
#         v[2] = round(v[2], 4)
#         # if v[1] == 'None':
#         #     v = [v[0], v[2]]
#         # v = ' - '.join(str(e) for e in v)
#
#         if v[1] == 'None':
#             v = str(v[0]) + ' (PEP: ' + str(v[2]) + ")"
#         else:
#             v = str(v[0]) + ' - ' + str(v[1]) + ' (PEP: ' + str(v[2]) + ")"
#     else:
#         v = pep.loc[[gene], ["tair", "symbol"]]
#         v = v.values.tolist()[0]
#         v = ' - '.join(str(e) for e in v)
#     return v

def get_clust_anno_list(ca):
    no_clusters = ca.shape[0]
    cs_list = []
    for i in range(no_clusters):
        cs_list.append(ca.loc[[i],].values[0].tolist())
    return cs_list

page_2 = html.Div([
    html.Div([
        # Description
        html.Div([
            html.Div([
                html.P(["Generation of the Data:"], className="card-title-small"),
                html.P([clust_data], className="card-text"),
                # html.P(["Purpose of this visualization:"], className="card-title-small"),
                # html.P([usage], className="card-text"),
                html.P(["How to use this resource:"], className="card-title-small"),
                html.P([menu], className="card-text"),

            ], className="colm"
                # , style={"background-color": "red"}
            )
        ], className="rowm", style={"margin": "0.5rem"}),

        # the dropdown (row)
        html.Div([
            html.Div([""], className="colm", style={"flex": "2 2 auto"}),  # SPACER
            html.Div([
                # dcc.Dropdown(id='umap_dropdown', multi=False,
                #              options=[{'label': x, 'value': x} for x in cluster_names],
                #              value='cluster_1')
                dcc.Dropdown(id='umap_dropdown', multi=False,
                             options=[{'label': x[1], 'value': x[0]} for x in get_clust_anno_list(ca=clust_anno)],
                             value="cluster_1")
            ], className="colm", style={"flex": "1 1 auto"}),  # actual dropdown
            html.Div([""], className="colm", style={"flex": "2 2 auto"}),  # SPACER
        ], className="rowm", style={"margin": "0.5rem 0 0.5rem 0"}),

        # the umap clustering (left colum) and 3D clusters (right) (row)
        html.Div([
            # clusters in UMAP space
            html.Div([clust_umap_card], className="colm", style={"max-width": "50%", "margin-right":"3rem"}),
            # clusters in 3D model
            html.Div([clust_3d_card], className="colm", style={"max-width": "50%", "margin-left":"3rem"})
        ], className="rowm")
    ], className="colm")
], className="rowm clus_card")


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
                      layout=go.Layout(scene=dict(bgcolor="#282828",
                                                  xaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  yaxis=dict(showgrid=False, zeroline=False, visible=False),
                                                  zaxis=dict(showgrid=False, zeroline=False, visible=False)
                                                  ),
                                       margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#282828"
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
                      layout=go.Layout(showlegend=False, plot_bgcolor="#282828",
                                       margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="#282828",
                                       xaxis=dict(visible=True, color="white", title=dict(text="UMAP1"), showline=True,
                                                  showgrid=False, zeroline=False),
                                       yaxis=dict(visible=True, color="white", title=dict(text="UMAP2"), showline=True,
                                                  showgrid=False, zeroline=False)
                                       )
                      )
    return fig_1
