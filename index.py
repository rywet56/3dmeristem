import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app
from app import server  # you need this otherwise Heroku will not work

# Connect to your app pages
from apps import clusters, expression

sidebar = dbc.Card([
    dbc.CardBody([
        html.H2("3D Meristem", className="display-4"),
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
                        "width":"16rem",
                        "position":"fixed"}
)

content = html.Div(id="page-content", children=[], style={"padding":"2rem"})

app.layout = dbc.Container([
    dcc.Location(id="url"),  # sets what pathname is. If we click sth. in the side bar this changes. This is fed into the callback
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(content, width=9, style={"margin-left": "16rem"})
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
