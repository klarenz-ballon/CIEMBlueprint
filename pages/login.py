import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db  # Assuming dbconnect is correctly imported

layout = html.Div(
    [
        dcc.Store(id='account_id_store', storage_type='session', data=0),  # Store user ID
        dcc.Store(id='currentuserid', storage_type='session', data=-1),  # Store user ID
        dcc.Store(id='currentrole', storage_type='session', data=-1),  # Store user role
        dcc.Store(id='sessionlogout', storage_type='session', data=0),  # Store for logout session management
        html.Video(
            src='/assets/login_bg.mp4',
            autoPlay=True,
            loop=True,
            muted=True,
            style={
                'position': 'fixed',
                'width': '100%',
                'height': '100%',
                'object-fit': 'cover',
                'z-index': '-1',
            }
        ),
        html.Div(
            [
                html.Img(
                    src='/assets/login_title.png',
                    style={
                        'max-width': '28vw',
                        'display': 'block',
                    },
                ),
            ],
            style={
                'position': 'fixed',
                'left': '8rem',  # Position the title image to the left of the screen
                'top': '8rem',  # Position the title image above the login card
                'z-index': '1',
            }
        ),
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("LOG IN", className="card-title fw-bolder"),
                            html.Br(),

                            dbc.Alert(id='login_alert', is_open=False),
                            dbc.Input(id='uname', type='text', className='input', placeholder='Username'),
                            html.Br(),

                            dbc.Input(type='password', id='pword', className='input', placeholder='Password'),
                            html.Br(),

                            dbc.Checklist(
                                options=[{"label": "Show Password", "value": 1}],
                                value=[],
                                id="show_pword",
                                inline=True,
                            ),
                            html.Br(),
                            dbc.Row(
                                dbc.Col(
                                    dbc.Button("Log in", color="primary", className="loginbutton", id='login_loginbtn'),
                                    width={'size': 4, 'offset': 8},
                                    className="d-flex justify-content-end"
                                )
                            ),
                        ],
                        className='half left',
                        style={
                            'background-color': 'rgba(255, 255, 255, 0.0)',  # 50% transparent background color
                        }
                    ),
                    className='flex small',
                    style={
                        'width': '35%',
                        'position': 'fixed',
                        'left': '8rem',  # Position the card to the left of the screen
                        'top': '16rem',  # Position the card below the title image
                        'padding': '3rem',
                        'border-radius': '20px',
                        'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.2)',
                        'background-color': 'rgba(255, 255, 255, 0.3)',  # 50% transparent background color
                    }
                ),
            ],
        ),
    ],
    style={
        'position': 'fixed',
        'width': '100%',
        'height': '100%',
        'overflow': 'hidden',  # Ensure the content does not overflow the background
    }
)

@app.callback(
    Output('pword', 'type'),
    [Input('show_pword', 'value')]
)
def toggle_password_visibility(show_pword):
    if show_pword:
        return 'text'
    else:
        return 'password'

@app.callback(
    [
        Output('login_alert', 'color'),
        Output('login_alert', 'children'),
        Output('login_alert', 'is_open'),
        Output('auth', 'data'),  # Update auth data upon successful login
        Output('url', 'pathname')
    ],
    [
        Input('login_loginbtn', 'n_clicks'),
    ],
    [
        State('uname', 'value'),
        State('pword', 'value'),
    ],
)
def loginprocess(loginbtn, username, password):
    auth_data = {}
    ctx = callback_context
    if ctx.triggered:
        alert_open = False
        alert_color = ""
        alert_text = ""

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'login_loginbtn':
            pn = '/login'
            if loginbtn and username and password:
                sql = """
                SELECT admin_pass
                FROM admin
                WHERE admin_name = %s 
                """
                
                values = [username]
                cols = ['admin_pass']

                df = db.querydatafromdatabase(sql, values, cols)
                print(f"Query result: {df}")  # Debug: Check the query result
                if df.shape[0]:
                    stored_password = df.at[0, 'admin_pass']
                    print(f"Stored password: {stored_password}")  # Debug: Check stored password
                    print(f"Input password: {password}")  # Debug: Check input password

                    if stored_password == password:
                        auth_data['isAuthenticated'] = True  # Set isAuthenticated to True upon successful login
                        auth_data['acc'] = username
                        alert_color = 'success'
                        alert_text = 'Successfully logged in.'
                        alert_open = True
                        pn = '/home'
                    else:
                        alert_color = 'danger'
                        alert_text = 'Incorrect username or password.'
                        alert_open = True
                        pn = "/login"
                else:
                    alert_color = 'danger'
                    alert_text = 'Incorrect username or password.'
                    alert_open = True
                    pn = "/login"
            
        return [alert_color, alert_text, alert_open, auth_data, pn]
    else:
        raise PreventUpdate
