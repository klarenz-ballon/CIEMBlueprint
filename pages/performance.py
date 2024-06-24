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

comm_options=[
                {'label': "Academic Affairs Committee", 'value': "1"},
                {'label': "External Affairs Committee", 'value': "2"},            
                {'label': "Finance Committee", 'value': "3"},            
                {'label': "Internal Affairs Committee", 'value': "4"},            
                {'label': "Membership and Recruitment Committee", 'value': "5"},           
                {'label': "Publications and Records Committee", 'value': "6"},
                        ]

perf_form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Academic Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='performance_acad_year', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "1st Sem Committee "
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(id='performance_reaff_sem1_comm', options=comm_options, disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "1st Sem Score "
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="number", id='performance_comm1_score', min=0, max=100, step=1, disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "2nd Sem Committee "
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(id='performance_reaff_sem2_comm', options=comm_options, disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "2nd Sem Score "
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="number", id='performance_comm2_score', min=0, max=100, step=1, disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Performance ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='performance_eval', disabled=True),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Button('Submit', id="perf_submit_btn", n_clicks=0),
        html.Div(id='perf_message') 
    ]
)

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        dbc.Button("Go Back",
                id="perf_back_btn",
                color="primary",
                href=""
            ),
        dbc.Card([
            dbc.CardHeader([
                html.H3("MEMBER PERFORMANCE")
            ], className='flex', style={'background-color': '#E8EDF7'}),
            dbc.CardBody([
                dbc.Container([
                    perf_form,
                ])
            ]),
        ], className="ml-4 mr-4 mt-4"),
    ], className='body')
])

@app.callback(
    Output('performance_eval', 'value'),
    [
        Input('performance_comm1_score', 'value'),
        Input('performance_comm2_score', 'value'),
    ]
)
def eval_calc(score1, score2):
    if score1:
        score1 = int(score1)
    else:
        score1 = 0
    if score2:
        score2 = int(score2)
    else:
        score2 = 0

    perf_eval = (score1 + score2)/2
    return perf_eval

@app.callback(
    [
        Output('performance_acad_year', 'value'),
        Output('performance_reaff_sem1_comm', 'value'),
        Output('performance_comm1_score', 'value'),
        Output('performance_reaff_sem2_comm', 'value'),
        Output('performance_comm2_score', 'value'),

        Output('perf_back_btn', 'href'),
        Output('perf_message', 'children')
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('perf_submit_btn', 'n_clicks'),
    ],
    [
        State('performance_acad_year', 'value'),
        State('performance_reaff_sem1_comm', 'value'),
        State('performance_comm1_score', 'value'),
        State('performance_reaff_sem2_comm', 'value'),
        State('performance_comm2_score', 'value'),
        State('performance_eval', 'value'),
     ],
)
def performance_fill_and_edit(url_search, pathname, submit, acad_year, comm1, score1, comm2, score2, eval):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    perf_id = query_id.get('perf_id', [None])[0]
    return_link = ""

    if pathname == '/performance':
        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            message = ""

            if eventid == 'perf_submit_btn' and submit:
                if comm1 and not score1:
                    message = 'Please input a score for the 1st Sem Committee'
                    color = 'red'
                elif not comm1 and score1:
                    message = 'Please remove the 1st Sem score since member is non-reaffiliated'
                    color = 'red'
                elif comm2 and not score2:
                    message = 'Please input a score for the 2nd Sem Committee'
                    color = 'red'
                elif not comm2 and score2:
                    message = 'Please remove the 2nd Sem score since member is non-reaffiliated'
                    color = 'red'
                else:
                    sql = """
                        UPDATE performance
                        SET
                            perf_comm1_score=%s,
                            perf_comm2_score=%s,
                            perf_eval=%s
                        WHERE NOT perf_delete_ind AND perf_id = %s
                    """
                    values = [score1, score2, eval, perf_id]
                    db.modifydatabase(sql, values)
                    message = 'Performance edited succesfully!'
                    color = 'green'

                return [acad_year, comm1, score1, comm2, score2, dash.no_update, html.Div(message, style={'color': color, 'display': 'block'})]

        sql = """
            select
                perf_acad_year,
                r1.reaff_assigned_comm,
                perf_comm1_score,
                r2.reaff_assigned_comm,
                perf_comm2_score,
                p.mem_id
            from performance p
            left join reaffiliation r1 on r1.reaff_id = p.perf_reaff_comm1
            left join reaffiliation r2 on r2.reaff_id = p.perf_reaff_comm2
            where NOT perf_delete_ind AND perf_id = %s
        """
        values = [perf_id]
        cols = [
            'acad_year',
            'comm1',
            'score1',
            'comm2',
            'score2',
            'mem_id'
        ]
        df = db.querydatafromdatabase(sql, values, cols)

        acad_year = df['acad_year'][0]
        comm1 = df['comm1'][0]
        score1 = df['score1'][0]
        comm2 = df['comm2'][0]
        score2 = df['score2'][0]
        mem_id = df['mem_id'][0]

        return_link = f'/mem_vieweditinfo?id={mem_id}'

        return [acad_year, comm1, score1, comm2, score2, return_link, html.Div(style={'disply': 'none'})]
    else:
        raise PreventUpdate
