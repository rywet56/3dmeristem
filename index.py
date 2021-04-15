import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import dash_bootstrap_components as dbc
from apps import expression, clusters, welcome
# Connect to main app.py file
from app import app
from app import server  # you need this otherwise Heroku will not work

header = html.Div([
        # SPACER
        html.Div([""], className='colm', style={"flex": "1 1 20%"
                                              # ,"background-color": "red"
                                              }
                 ),
        html.Div([
            html.A([html.Div(["3D Flower Meristem"])], href="/#", className="LINK")
        ], className='colm', style={"flex": "3 0 60%",
                                    "display": "flex", "flex-direction": "column",
                                    "align-items": "center",
                                    "justify-content": "center", "font-size": "3rem"
                                     # ,"background-color": "blue"
                                    }),
        html.Div([
            html.A([html.Div(["Kaufmann Lab"])], href="https://www2.hu-berlin.de/biologie/flower/", className="LINK")
        ], className='colm', style={"flex": "1 1 20%",
                                    "display": "flex", "flex-direction": "column",
                                    "align-items": "flex-end",
                                    "justify-content": "center", "font-size": "1.5rem",
                                    "padding":"0 1.5rem 0 0"
                                    # ,"background-color": "red"
                                    })
], className='rowm', style={"height": "6rem"})

navbar = html.Div([
        # SPACER
        html.Div([""], className='colm'),
        # BUTTON
        html.Div([
            html.A([html.Button(["Visualize Gene Expression"], className="button button1")],
                   href="/apps/expr", style={"height": "100%", "width": "100%"})
        ], className='colm',
            style={"align-items": "center", "justify-content": "center", "background-color": "red"}),
        # SPACER
        html.Div([""], className='colm'),
        # BUTTON
        html.Div([
            html.A([html.Button(["Visualize Cell Cluster Location"], className="button button2")],
                   href="/apps/clust", style={"height": "100%", "width": "100%"})
        ], className='colm', style={"align-items": "center", "justify-content": "center"}),
        # SPACER
        html.Div([""], className='colm', style={"height":"100%"})
], className='rowm', style={"height": "3rem"})

content = html.Div(id="page-content", className='colm')

footer = html.Div([
    html.Div([
        html.Div([
            html.Div(["Created by Manuel Neumann using Dash Plotly and CSS Flexbox"]),
            html.P([""]),
            html.A([html.Div(["GitHub"])], href="https://github.com/rywet56", className="LINK")
        ], className='colm', style={"flex": "1 1 0", "padding": "2rem",
                                    "justify-content": "space-around", "height": "3rem"})
    ], className="rowm")
], className='colm')

app.layout = html.Div([
    dcc.Location(id="url"),

    # HEADER
    html.Div([
        html.Div([header], className="colm")
    ], className="rowm"),

    # NAV BAR
    html.Div([
        html.Div([navbar], className="colm")
    ], className="rowm"),

    # main content
    html.Div([
        content
    ], className="rowm", style={"flex": "1 1 auto"}),

    # FOOTER
    html.Div([
        html.Div([footer], className="colm")
    ], className="rowm", style={"height": "8rem", "border-top":"0.2rem solid white", "margin-top":"5rem"})
], className="main-viewport")


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/apps/expr':
        return expression.page_1
    if pathname == '/apps/clust':
        return clusters.page_2
    else:
        return welcome.page_3


if __name__ == "__main__":
    app.run_server(debug=True)
