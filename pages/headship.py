import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from datetime import datetime
from app import app
from apps import commonmodule as cm
from apps import dbconnect as db
from dash_iconify import DashIconify as di
from urllib.parse import urlparse, parse_qs, urlencode
import dash_mantine_components as dmc
from dash import dash_table

# Define headship options
head_options=[
    {'label': "Committee Director", 'value': 1},
    {'label': "Project Executive Head", 'value': 2},            
    {'label': "Project Committee Head", 'value': 3},            
    {'label': "Project Member", 'value': 4},
]

# Create the headship form
headship_form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Academic Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col((dcc.Dropdown(id='headship_score_acad_year', disabled=False),
                            ),width=4),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Headship ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(id='headship_score_name', options=head_options, disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Headship Description ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='headship_score_description', value='', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Headship Score ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='headship_score_score', disabled=True),  # Set to disabled so user cannot modify directly
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.Hr(),
        dbc.Button('Submit', id="head_submit_btn", n_clicks=0, style={'backgroundColor': '#5474D5'}),
        html.Div(id='headscore_message') 
    ]
)

# Define the layout
layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        dbc.Button("Go Back",
                id="headship_back_btn",
                color="primary",
                href='', 
                style={'backgroundColor': '#5474D5'},
            ),
        dbc.Card([
            dbc.CardHeader([
                html.H3("MEMBER HEADSHIPS")
            ],  className='flex', 
                style={  'background-color': '#2E4178',
                            'color': 'white',  # White text for header
                            'font-size': '24px',
                            'font-weight': 'bold'}),
            dbc.CardBody([
                dbc.Container([
                    html.Br(),
                    headship_form,
                    html.Br(),
                ])
            ]),
        ], className="ml-4 mr-4 mt-4"),
    ], className='body')
])

# Callback to automatically update the headship score based on the selected headship name
@app.callback(
    Output('headship_score_score', 'value'),
    Input('headship_score_name', 'value'),
    State('headship_score_name', 'value'),
)
def update_headship_score(_, head_name_value):
    if head_name_value == 1:  # Committee Director
        return "10"
    elif head_name_value == 2:  # Project Executive Head
        return "8"
    elif head_name_value == 3:  # Project Committee Head
        return "5"
    elif head_name_value == 4:  # Project Member
        return "2"
    return ""

@app.callback(
    [
        Output('headship_score_acad_year', 'value'),
        Output('headship_score_name', 'value'),
        Output('headship_score_description', 'value'),

        Output('headscore_message', 'children')
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('head_submit_btn', 'n_clicks'),
    ],
    [
        State('headship_score_acad_year', 'value'),
        State('headship_score_name', 'value'),
        State('headship_score_description', 'value'),
        State('headship_score_score', 'value'),
     ],
)
def mem_form_fill_and_submit(
                url_search,
                pathname,
                submit,
                
                acad_year,
                headship,
                description,
                score):
    
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    mem_id = query_id.get('id', [None])[0]
    mode = query_id.get('mode', [None])[0]

    if pathname == '/headship':
        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'head_submit_btn' and submit:
                if not(
                    acad_year and
                    headship and
                    description
                ):
                    return[
                        dash.no_update, dash.no_update, dash.no_update, 
                        html.Div("Please fill in all required information.", style={'color': 'red'})
                    ]
                else:
                    if mode == 'edit':

                        head_id = query_id.get('head_id', [None])[0]

                        sql = """
                            UPDATE headship_score
                            SET
                                headscore_acad_year = %s,
                                headscore_description = %s,
                                headscore_score = %s
                            WHERE not headscore_delete_ind
                                AND mem_id = %s
                                AND head_id = %s
                        """
                        values = [acad_year, description, score, mem_id, head_id]

                        db.modifydatabase(sql, values)

                        return[
                            dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Headship edited successfully!", style={'color': 'green'})
                        ]

                    if mode == 'add':

                        sql = """
                            INSERT INTO headship_score(
                                mem_id,
                                head_id,
                                headscore_acad_year,
                                headscore_description,
                                headscore_score
                            )
                            VALUES(%s, %s, %s, %s, %s)
                        """
                        values = [mem_id, headship, acad_year, description, score]

                        db.modifydatabase(sql, values)
                        
                        return[
                            dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Headship added successfully!", style={'color': 'green'})
                        ]

        elif mode == 'edit':

            head_id = query_id.get('head_id', [None])[0]
            sql = """
                select
                    headscore_acad_year,
                    head_id,
                    headscore_description
                from headship_score
                where not headscore_delete_ind
                    AND mem_id = %s
                    AND head_id = %s
            """
            values = [mem_id, head_id]
            cols = [
                'headscore_acad_year',
                'head_name',
                'headscore_description',
            ]
            df = db.querydatafromdatabase(sql, values, cols)

            acad_year = df['headscore_acad_year'][0]
            name = df['head_name'][0]
            description = df['headscore_description'][0]

            return [acad_year, name, description, html.Div(style={'disply': 'none'})]
    raise PreventUpdate
        

@app.callback(  
    Output("headship_score_acad_year", "options"),
    Output('headship_back_btn', 'href'),
    Input('url','search'),
)
def add_active_acad_year(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    return_link = ""

    if 'id' in query_ids:
        mem_id = query_ids['id'][0]
        sql = """
            SELECT reaff_acad_year as label, reaff_acad_year as value
            FROM (
                SELECT DISTINCT reaff_acad_year, CAST(SUBSTRING(reaff_acad_year FROM 1 FOR 4) AS INTEGER) AS start_year
                FROM reaffiliation
                WHERE NOT reaff_delete_ind
                    AND mem_id = %s
            ) AS sorted_years
            ORDER BY start_year ASC
        """
        values = [mem_id]
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        acad_year_options = df.to_dict('records')
        return_link = f'/mem_vieweditinfo?id={mem_id}'
        
        return acad_year_options, return_link
    else:
        raise PreventUpdate
    
def set_back_button_url(url_search):
    parsed = urlparse(url_search)
    query_ids = parse_qs(parsed.query)
    
    if 'id' in query_ids:
        mem_id = query_ids['id'][0]
        return f'/mem_vieweditinfo?id={mem_id}'
    else:
        return '/'

   


        
