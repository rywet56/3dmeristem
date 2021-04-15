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


def get_title(gene, use_pep, pep):
    if use_pep:
        v = pep.loc[[gene], ["tair", "symbol", "top_spear_cor"]]
        v = v.values.tolist()[0]
        v[2] = round(v[2], 4)
        # if v[1] == 'None':
        #     v = [v[0], v[2]]
        # v = ' - '.join(str(e) for e in v)

        if v[1] == 'None':
            v = str(v[0]) + ' (PEP: ' + str(v[2]) + ")"
        else:
            v = str(v[0]) + ' - ' + str(v[1]) + ' (PEP: ' + str(v[2]) + ")"
    else:
        v = pep.loc[[gene], ["tair", "symbol"]]
        v = v.values.tolist()[0]
        v = ' - '.join(str(e) for e in v)
    return v


def get_tair_symbol_list(sdge_genes, pep):
    tair_symbol = []
    for gene in sdge_genes:
        t_s = pep.loc[[gene], ["tair", "symbol"]].values[0].tolist()
        t = t_s[0]
        t_s_str = str(t_s[0]) + " - " + str(t_s[1])
        tair_symbol.append([t_s_str, t])
    return tair_symbol


PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

path = DATA_PATH.joinpath("confocal_states0-FilterWUSCLVtop100.csv")
ref = pd.read_csv(path, sep=",", index_col=0, decimal=".")
ref_genes = ref.columns.values.tolist()[5:28]

path = DATA_PATH.joinpath("dge_top_1000_genes.csv")
sdge = pd.read_csv(path, sep=",", index_col=0, decimal=".")
# sdge = sdge.T
sdge_genes = sdge.columns.values.tolist()

path = DATA_PATH.joinpath("pep.csv")
pep = pd.read_csv(path, sep=",", index_col=0, decimal=".")


# text_1 = "The 3D expression profiles of genes shown here are in binary format and were obtained by reconstructing 2D " \
#          "confocal images and manually annotating the respective expression for all cells in the model. In total " \
#          "there are 23 such reference genes that have been used in the prediction of the other ~15,000 genes (shown " \
#          "on the right)."
text_1 = 'The 3D gene expression profiles of 28 reference genes were obtained from Refahi et al [1]. They were generated by 3D reconstruction of confocal microscopy images and manually annotating the binary gene expression of 28 reference genes in this model.'


# chose_gene = "View the 3D Expression Profile of a gene of your interest by selecting this gene in the dropdown menu " \
#              "or entering its TAIR ID. The TAIR ID, the Gene Symbol (if available) and the PEP Score for that gene are " \
#              "shown in the plot, in " \
#              "this order. For example, TAIR ID: AT1G24260, Gene Symbol: WAM1, PEP: 1.0"
chose_gene = 'View the 3D expression profile of a gene of interest by selecting this gene in the dropdown menu or entering its TAIR ID. The TAIR ID, the Gene Symbol (if available) and the PEP score for this gene are shown in the plot in this order. For example, TAIR ID: AT1G24260, Gene Symbol: WAM1, PEP: 1.0'
change_color = "Change the color scheme for better visualization. "
change_range = "Change the Max and Min expression values to put emphasis on strongly or weakly expression patterns"

ref_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([
                html.Div([
                    html.H2(["Reference Expression"], className="card-title-big"),
                    html.P([text_1], className="card-text"),
                    html.P(["1) Select a gene"], className="card-title-small"),
                    html.P([chose_gene], className="card-text")
                ], className="colm"
                    # , style={"background-color": "red"}
                )
            ], className="rowm", style={"margin": "0.5rem"}),
            # dropdown menu
            html.Div([
                html.Div([
                    # dcc.Dropdown(id='ref_expr_dropdown', multi=False,
                    #              options=[{'label': x, 'value': x} for x in ref_genes],
                    #              value="AT1G62360")
                    dcc.Dropdown(id='ref_expr_dropdown', multi=False,
                                 options=[{'label': x[0], 'value': x[1]} for x in get_tair_symbol_list(ref_genes, pep)],
                                 value="AT1G24260")
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
                        html.P(["2) Select a color scheme"], className="card-title-small"),
                        html.P([change_color], className="card-text"),
                        # html.H5("Color Scheme:"),
                        dcc.RadioItems(id='color_code_ref',
                                       options=[
                                           {'label': 'blue-yellow-red', 'value': 'byr'},
                                           {'label': 'yellow-red', 'value': 'yr'},
                                           {'label': 'red-green', 'value': 'rg'}],
                                       value='byr', className="onehalfrem-up")
                    ], className="colm"),
                ], className="rowm")
            ], className="colm")
        ], className="rowm"),
    ], className="colm"),
], className="rowm expr_card", style={"margin": "1rem 0.5rem 0 1rem"}
)

# text_2 = "The 3D expression profiles of genes shown here are in continuous format and were predicted using an " \
#          "Optimal-Transport (OT) based framework as implemented in novosparc+ [3], an extension of NovoSpaRc [1]. The " \
#          "predicted 3D gene expression profiles presented here are limited to the best 1,000 genes, as measured by " \
#          "the PEP score (explained on main page)."
text_2 = 'The gene expression profiles predicted by Neumann et al. [2] can be visualized in the 3D reconstructed floral meristem. The predicted expression values were standardized to mean 0 and variance 1. Only genes with a PEP score higher than 0.13 can be visualized. The PEP score is an indication of the power of the expression prediction for a particular gene (see Neumann et al. [2]).'
# "for whose we have reason to assume that they are accurate based on the PEP (Prediced ExPression) score, which expresses the " \
# "how confident were are that the predicted expression profile is biologically reasonable."

pre_card = html.Div([
    html.Div([
        # The main part of the card
        html.Div([html.Div([
            # some text
            html.Div([
                html.Div([
                    html.H2(["Predicted Expression"], className="card-title-big"),
                    html.P([text_2], className="card-text"),
                    html.P(["1) Select a gene"], className="card-title-small"),
                    html.P([chose_gene], className="card-text")
                ], className="colm"
                    # ,style={"background-color": "red"}
                )
            ], className="rowm", style={"margin": "0.5rem"}),
            # dropdown menu
            html.Div([
                html.Div([
                    # dcc.Dropdown(id='pre_expr_dropdown', multi=False,
                    #              options=[{'label': x, 'value': x} for x in sdge_genes],
                    #              value="AT1G24260")
                    dcc.Dropdown(id='pre_expr_dropdown', multi=False,
                                 options=[{'label': x[0], 'value': x[1]} for x in get_tair_symbol_list(sdge_genes, pep)],
                                 value="AT1G24260")

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
                        html.P(["2) Select a color scheme"], className="card-title-small"),
                        html.P([change_color], className="card-text"),
                        # html.H5("Color Scheme:"),
                        dcc.RadioItems(id='color_code',
                                       options=[{'label': 'blue-yellow-red', 'value': 'byr'},
                                                {'label': 'yellow-red', 'value': 'yr'},
                                                {'label': 'red-green', 'value': 'rg'}],
                                       value='byr', className="onehalfrem-up")
                    ], className="colm"),
                ], className="rowm"),
                html.Div([
                    html.Div([
                        html.P(["3) Change Min Max"], className="card-title-small"),
                        html.P([change_range], className="card-text"),
                        # html.H5("Range of Values:"),
                        dcc.RangeSlider(id='slider_pre', min=0, max=0, value=[],
                                        marks={}, step=None, allowCross=False,
                                        className="slider_expr onerem-up", verticalHeight=800),
                    ], className="colm")
                ], className="rowm")
            ], className="colm")
        ], className="rowm"),
    ], className="colm"),
], className="rowm expr_card", style={"margin": "1rem 1rem 0 0.5rem"}
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
    # get title based on gene choosen
    print(val_chosen_2)
    title = get_title(gene=val_chosen_2, use_pep=False, pep=pep)

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
                    layout=go.Layout(title=dict(text=title, font=dict(color="white", size=30), x=0.5, y=0.95),
                                     scene=dict(bgcolor="#282828",
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
    # get title based on gene choosen
    title = get_title(gene=val_chosen_2, use_pep=True, pep=pep)

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
                      layout=go.Layout(title=dict(text=title, font=dict(color="white", size=30), x=0.5, y=0.95),
                                       scene=dict(bgcolor="#282828",
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
