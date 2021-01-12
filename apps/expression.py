import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
from app import app
import dash_bootstrap_components as dbc


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

path = DATA_PATH.joinpath("confocal_states0-FilterWUSCLVtop100.csv")
ref = pd.read_csv(path, sep=",", index_col=0, decimal=".")
ref_genes = ref.columns.values.tolist()[5:28]

path = DATA_PATH.joinpath("ALLGENES_ns_2_nt_5_alpha_0.1_epsilon_0.05_top_sccells_50_top_hvg_100_1000genes.txt")
sdge = pd.read_csv(path, sep=",", index_col=0, decimal=".")
sdge = sdge.T
sdge_genes = sdge.columns.values.tolist()
sdge['x'] = ref['x'].tolist()
sdge['y'] = ref['y'].tolist()
sdge['z'] = ref['z'].tolist()


layout = html.Div([
    dbc.Row(
        dbc.Col(
            html.H2('3D expression profiles'),
            width={'size': 7, 'offset': 3}
        )
    ),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='my-dropdown_1', multi=False,
                         options=[{'label': x, 'value': x} for x in ref_genes],
                         value="AT1G62360"),
            width={'size': 6, 'offset': 0}
        ),
        dbc.Col(
            dcc.Dropdown(id='my-dropdown_2', multi=False,
                         options=[{'label': x, 'value': x} for x in sdge_genes],
                         value="AT1G01010"),
            width={'size': 6, 'offset': 0}
        )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph-output_1', figure={}),
            width={'size': 6, 'offset': 0}
        ),
        dbc.Col(
            dcc.Graph(id='graph-output_2', figure={}),
            width={'size': 6, 'offset': 0}
        )
    ])
])

@app.callback([Output('graph-output_1', 'figure'), Output('graph-output_2', 'figure')],
              [Input('my-dropdown_1', 'value'), Input('my-dropdown_2', 'value')])
def update_my_graph_1(val_chosen_1, val_chosen_2):
    if len(val_chosen_1) > 0 or len(val_chosen_2) > 0:
        fig_1 = px.scatter_3d(ref, x='x', y='y', z='z', color=val_chosen_1)
        fig_1.update_layout(scene=dict(
                                      xaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      yaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      zaxis=dict(showgrid=False,zeroline=False,visible=False)
                                    )
                         )
        fig_2 = px.scatter_3d(data_frame=sdge, x='x', y='y', z='z',
                              color=val_chosen_2,
                              color_continuous_scale=["blue", "yellow","red"])
        fig_2.update_layout(scene=dict(
                                      xaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      yaxis=dict(showgrid=False,zeroline=False,visible=False),
                                      zaxis=dict(showgrid=False,zeroline=False,visible=False)
                                    )
                         )
        return fig_1, fig_2
    elif len(val_chosen_1) == 0 or len(val_chosen_2) == 0:
        raise dash.exceptions.PreventUpdate
