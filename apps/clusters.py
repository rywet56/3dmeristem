import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
clust['x'] = ref['x'].tolist()
clust['y'] = ref['y'].tolist()
clust['z'] = ref['z'].tolist()

layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2('3D UMAP cluster assignment '),
            width={'size': 7, 'offset': 3}
        )
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='my-dropdown_4', multi=False,
                         options=[{'label': x, 'value': x} for x in cluster_names],
                         value='cluster_1'),
            width={'size': 2, 'offset': 5}
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph-output_3', figure={}),
            width={'size': 6, 'offset': 0}
        ),
        dbc.Col(
            dcc.Graph(id='graph-output_4', figure={}),
            width={'size': 6, 'offset': 0}
        )
    ])
])

@app.callback([Output('graph-output_3', 'figure'), Output('graph-output_4', 'figure')],
              [Input('my-dropdown_4', 'value')])
def update_my_graph_1(val_chosen_2):
    if len(val_chosen_2) > 0:
        cols = px.colors.qualitative.Dark24[0:13]
        cluster_cols = [cols[int(cluster_no)] for cluster_no in umap['cluster']]
        clust_focus = val_chosen_2.split("_")[1]
        umap_sub = umap[umap['cluster']==clust_focus]
        cluster_cols_sub = [cols[int(clust_focus)]] * umap_sub.shape[0]
        fig_1 = go.Figure(data=[go.Scatter(x=umap["UMAP_1"], y=umap["UMAP_2"], mode='markers',
                                         marker=dict(size=6, color=cluster_cols), opacity=0.3
                                        ),
                              go.Scatter(x=umap_sub["UMAP_1"], y=umap_sub["UMAP_2"], mode='markers',
                                         marker=dict(size=6, color=cluster_cols_sub), opacity=1
                                        )
                                ],
                          layout=go.Layout(showlegend=False
                                          )
                         )
        # fig_1 = px.scatter(umap, x="UMAP_1", y="UMAP_2", color="cluster")
        # clus_no = int(val_chosen_2.split("_")[1])
        # cluster_colors = {str(i):("red" if i == clus_no else "black") for i in range(0,13)}
        # fig_1 = px.scatter(umap, x="UMAP_1", y="UMAP_2", color="cluster",
        #                 hover_name="cluster",
        #                 color_discrete_map=cluster_colors
        #                 )
        fig_2 = px.scatter_3d(data_frame=clust, x='x', y='y', z='z',
              color=val_chosen_2, color_continuous_scale=["blue", "yellow","red"])
        fig_2.update_layout(scene=dict(
                                      xaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      yaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      zaxis=dict(showgrid=False,zeroline=False,visible=False)
                                    )
                         )
        return fig_1, fig_2
    elif len(val_chosen_2) == 0:
        raise dash.exceptions.PreventUpdate
