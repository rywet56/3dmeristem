import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from apps import expression, clusters
# Connect to main app.py file
from app import app
from app import server  # you need this otherwise Heroku will not work

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "22rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    # "margin-left": "22rem",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


header = html.Div([
    html.Div([], className='col-2'),
    html.Div([html.H1(children='3D Flower Meristem', style={'textAlign': 'center'})
              ], className='col-8', style={'padding-top': '1%'}),
    html.Div([html.H5(children='Kaufmann Lab', style={'textAlign': 'center', 'padding-top': '10%'})], className='col-2')
], className='row', style={'height': '4%',
                           'background-color': 'black'}
)

navbar = html.Div([
    html.Div([
        html.A(html.Button('3D expression', id='expression', className='btn btn-warning',
                           style={"border-radius": "0rem", "width": "100%", "font-size": "1.8rem",
                                  "font-weight": "bold"}),
               href="/apps/expr")
    ], className='col-3 offset-2'),
    html.Div([
        html.A(html.Button('3D cluster assignment', id='clusters', className='btn btn-primary',
                           style={"border-radius": "0rem", "width": "100%", "font-size": "1.8rem",
                                  "font-weight": "bold"}),
               href="/apps/clust")
    ], className='col-3 offset-2')
], className='row')


content = html.Div(id="page-content"
                   )

app.layout = html.Div([dcc.Location(id="url"), header, navbar, content], style={"background-color":"grey", "background-size": "cover"})


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/apps/expr':
        return expression.page_1
    if pathname == '/apps/clust':
        return clusters.page_2
        # return html.P("Oh cool, this is page 2!")
    else:
        return html.P("Welcome Page")


if __name__ == "__main__":
    app.run_server(debug=True)
