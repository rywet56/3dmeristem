import dash
import dash_bootstrap_components as dbc

# meta_tags are required for the app layout to be mobile responsive
my_styles = "/Users/manuel/OneDrive/git_hub_repos/3dmeristem/assets/my_styles.css"
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                # external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server
