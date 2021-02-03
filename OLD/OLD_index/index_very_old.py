import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server  # you need this otherwise Heroku will not work

# Connect to your app pages
from apps import clusters, expression

# styling the sidebar
# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "20rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

# padding for the page content
# CONTENT_STYLE = {
#     "margin-left": "18rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
# }

# sidebar = html.Div(
#     [
#         html.H2("3D Meristem", className="display-4"),
#         html.Hr(),
#         html.P("3D clusters or gene expression profiles", className="lead"),
#         dbc.Nav([
#                 dbc.NavLink("3D gene expression", href="/apps/expr", active="exact"),
#                 dbc.NavLink("3D cluster assignment", href="/apps/clust", active="exact"),
#                 ], vertical=True, pills=True,
#                 ),
#     ],
#     style=SIDEBAR_STYLE,
# )

# content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

sidebar = dbc.Card([
    dbc.CardBody([
        html.H2("3D Flower Meristem", className="display-4"),
        html.Hr(),
        html.P("3D clusters or gene expression profiles", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("3D gene expression", href="/apps/expr", active="exact"),
                dbc.NavLink("3D cluster assignment", href="/apps/clust", active="exact"),
            ],
            vertical=True, pills=True,
        ),
    ]),
], color="light", style={"height":"100vh",
                        "width":"22rem",
                        "position":"fixed"}
)


content = html.Div(id="page-content", children=[], style={"padding":"2rem"})

# app.layout = html.Div([
#     dcc.Location(id="url"),
#     sidebar,
#     content
# ])

app.layout = dbc.Container([
    dcc.Location(id="url"),  # sets what pathname is. If we click sth. in the side bar this changes. This is fed into the callback
    dbc.Row([
        dbc.Col(sidebar, width=3),
        dbc.Col(content, width=9
                ,style={"margin-left": "22rem"}
                )
    ])
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/expr':
        return expression.layout
    if pathname == '/apps/clust':
        return clusters.layout
    else:
        return expression.layout


if __name__ == '__main__':
    app.run_server(debug=False)
