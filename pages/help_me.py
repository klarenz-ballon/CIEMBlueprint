from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
from app import app

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader("Access the User Manual",
                            className='flex',
                            style={'background-color': '#2E4178',
                                    'color': 'white',
                                    'font-size': '24px',
                                    'font-weight': 'bold',
                                    'margin-bottom': '0',  # Remove bottom margin
                                    'padding-bottom': '0'}),  # Remove bottom padding
                dbc.CardBody([
                dbc.Container([
                    dbc.Row(
                        dbc.Col(
                            html.A(
                                href="https://drive.google.com/file/d/16n-Ks5AjTx_BPvb96VR1--h5KQ9Ltdt_/view",
                                target="_blank",
                                children=[
                                    html.Img(
                                        src='/assets/user_manual.png',
                                        style={'height': 'auto', 'max-height': '500px', 'cursor': 'pointer'}
                                    )
                                ]
                            ),
                            className='d-flex justify-content-center'
                        )
                    )
                ], className='flex homeshow', style={'background-color': 'white', 'padding': '20px', 'border-radius': '5px', 'margin-top': '0'}),  # Remove top margin
            ]),
            dbc.CardFooter(
                [
                    html.Br(),
                    dbc.Row(dbc.Label("For any concerns, please contact the developers at:")),
                    html.Br(),
                    dbc.Row("Klarenz Ballon - knballon@up.edu.ph"),
                    dbc.Row("Andre Genesis Cabasag - abcabasag@up.edu.ph"),
                    dbc.Row("Ma. Roxette Rojas - mmrojas@up.edu.ph")
                ], className='flex homeshow', style={'padding-top': '0', 'background-color': '#E8EFFF'})  # Set background color to #E8EFFF
        ], className='body', style={'margin-bottom': '0'})  # Remove bottom margin
    ], className='flex body-container')
])
])
