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
    html.Div([], className='colm', style={"flex": "1 1 20%"
                                          # ,"background-color": "red"
                                          }
             ),
    html.Div([
        html.A([html.Div(["3D Flower Meristem"])], href="/#")
    ], className='colm', style={"flex": "3 0 60%",
                                "display": "flex", "flex-direction": "column",
                                "align-items": "center",
                                "justify-content": "center", "font-size": "3rem"
                                # , "background-color": "blue"
                                }),
    html.Div([
        html.A([html.Div(["Kaufmann Lab"])], href="https://www2.hu-berlin.de/biologie/flower/")
    ], className='colm', style={"flex": "1 1 20%",
                                "display": "flex", "flex-direction": "column",
                                "align-items": "flex-end",
                                "justify-content": "center", "font-size": "1.5rem"
                                # , "background-color": "red"
                                }),
], className='rowm')

navbar = html.Div([
    # SPACER
    html.Div([], className='colm', style={"flex": "1 1 0"}),
    html.Div([
        html.A([html.Button(["3D Expression"], className="button button1")],
               href="/apps/expr", style={"height": "100%", "width": "100%"})
    ], className='colm',
        style={"flex": "1 1 0", "align-items": "center", "justify-content": "center", "background-color": "red"}),
    # SPACER
    html.Div([], className='colm', style={"flex": "1 1 0"}),
    html.Div([
        html.A([html.Button(["3D Clusters"], className="button button2")],
               href="/apps/clust", style={"height": "100%", "width": "100%"})
    ], className='colm', style={"flex": "1 1 0", "align-items": "center", "justify-content": "center"}),
    # SPACER
    html.Div([], className='colm', style={"flex": "1 1 0"})
], className='rowm')

content = html.Div(id="page-content")

footer = html.Div([
    html.Div([
        html.Div(["Created by Manuel Neumann using Dash Plotly and a bit of CSS"], className="footer-text"),
        html.P([""]),
        html.A([html.Div(["GitHub"], className="footer-text")], href="https://github.com/rywet56")
    ], className='colm', style={"flex": "1 1 0", "padding": "2rem",
                                "justify-content": "space-around", "height": "3rem"})
], className='rowm')

# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             dcc.Location(id="url"),
#             html.Div(header, style={"margin-bottom": "1rem"}),
#             html.Div(navbar, style={"margin-bottom": "1rem"}),
#             html.Div(expression.page_1),
#             html.Div([], style={"border-top": "0.1rem solid white", "margin-top": "6rem"}),  # for Footer
#             html.Div(footer)
#         ]
#             , style={"margin": "2rem"}  # KEEP THIS ! IMPORTANT ! without this the window gets a horizontal scrollbar
#         )
#     ], className="colm",
#         style={"max-width": "100%"}
#         # style={"display": "flex", "width":"100%", "margin":"2rem",
#         #       "flex-direction": "column", "min-height":"100vh"}
#     )
# ], className="rowm"
# )

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([header], className="container", style={
        # "background-color": "red",
        "height": "5rem", "padding": "0 0.5rem 0 0.5rem"}),
    html.Div([navbar], className="container", style={
        # "background-color": "yellow",
        "height": "3rem"}),
    html.Div([
        html.Div(  # main content
            # [expression.page_1],
            [content],
            style={"margin": "2rem"})
        # KEEP THIS ! IMPORTANT ! without this margin the window gets a horizontal scrollbar
    ], className="container", style={"flex": "1", "width": "100%"}),
    html.Div([footer], className="container", style={
        # "background-color": "red",
        "height": "4rem", "border-top": "0.2rem solid white", "color":"white"})
], className="main-viewport", style={"width": "100%"}
)


# app.layout = expression.page_1

# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             expression.page_1
#         ], style={"margin": "2rem"}
#         )
#     ], className="colm",
#         style={"max-width": "100%"}
#     )
# ], className="rowm"
# )


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
