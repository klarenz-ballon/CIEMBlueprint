import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from dash.exceptions import PreventUpdate
from app import app
from apps import commonmodule as cm
from urllib.parse import parse_qs
from apps import dbconnect as db  # Import your dbconnect module here
import urllib.parse

# Define the form layout
edit_mem_form = dbc.Form(
    [
        html.Br(),
        html.H5(html.B('Membership Type')),
        dbc.Row(
            [
                html.P('You may choose from the dropdown menu to update the membership type.'),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dcc.Dropdown(
                                id='memtype_dropdown',
                                options=[
                                    {'label': 'Regular', 'value': 'Regular'},
                                    {'label': 'Non-Regular', 'value': 'Non-Regular'},
                                    {'label': 'Honorary', 'value': 'Honorary'},
                                    {'label': 'Probationary', 'value': 'Probationary'}
                                ],
                                multi=False,
                                placeholder="Select Membership Type",
                                style={'width': '80%'}
                            )
                        ]
                    ),
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.H5(html.B('Membership Status')),
        dbc.Row(
            [
                html.P('You may choose from the dropdown menu to update the membership status.'),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dcc.Dropdown(
                                id='memstat_dropdown',
                                options=[
                                    {'label': 'Active', 'value': 'Active'},
                                    {'label': 'Inactive', 'value': 'Inactive'}
                                ],
                                multi=False,
                                placeholder="Select Membership Status",
                                style={'width': '80%'}
                            )
                        ]
                    ),
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.H5(html.B('Committee Assignment')),
        dbc.Row(
            [
                html.P('You may choose from the dropdown menu to assign the committee.'),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dcc.Dropdown(
                                id='comm_dropdown',
                                options=[
                                    {'label': 'Academic Affairs Committee', 'value': 'Academic Affairs Committee'},
                                    {'label': 'External Affairs Committee', 'value': 'External Affairs Committee'},
                                    {'label': 'Internal Affairs Committee', 'value': 'Internal Affairs Committee'},
                                    {'label': 'Finance Committee', 'value': 'Finance Committee'},
                                    {'label': 'Membership and Recruitment Committee', 'value': 'Membership and Recruitment'},
                                    {'label': 'Publication and Records Committee', 'value': 'Publication and Records Committee'}
                                ],
                                multi=False,
                                placeholder="Select Committee Assignment",
                                style={'width': '80%'}
                            )
                        ]
                    ),
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.H5(html.B('Performance')),
        dbc.Row(
            [
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dcc.Input(
                                type="text",
                                id='performance',
                                style={'width': '80%'}
                            )
                        ]
                    ),
                ),
            ],
            className="mb-2",
        ),

        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Submit", id="memsubmit-button", color="primary", className="mb-3"),
                    width={"size": 6, "offset": 3}
                )
            ],
        ),
        html.Div(id='memoutput-message'),  # For displaying output messages
        html.Br(),
        html.Br(),
    ]
)

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader("EDIT MEMBER FORM", className='flex'),
                dbc.CardBody([
                    dbc.Container(
                        [edit_mem_form],
                    )
                ]),
            ])
        ])
    ], className='body')
])

# Callback to handle form submission
@app.callback(
    Output('memoutput-message', 'children'),
    Input('memsubmit-button', 'n_clicks'),
    State('memtype_dropdown', 'value'),
    State('memstat_dropdown', 'value'),
    State('comm_dropdown', 'value'),
    State('performance', 'value'),
    State('url','search')
)
def update_member(n_clicks, memtype_values, memstat_values, comm_values, performance_value,search):
    if n_clicks is None:
        raise PreventUpdate

    upciem_member_id = parse_qs(search)['id'][0]
    try:
        if memstat_values:
            update_status(memstat_values, upciem_member_id)

        if memtype_values or comm_values:
            update_affiliation(memtype_values, comm_values, upciem_member_id)

        if performance_value:
            update_performance(performance_value, upciem_member_id)

        return html.Div([
            html.P("Member information updated successfully!", className="text-success")
        ])

    except Exception as e:
        return html.Div([
            html.P(f"Error updating member information: {str(e)}", className="text-danger")
        ])

# Functions to update database tables
def update_status(memstat_value, upciem_member_id):
    print('stat')
    sql = """
    UPDATE upciem_member
    SET active_status= %s
    WHERE valid_id= %s
    """
    db.modifydatabase(sql, (memstat_value, upciem_member_id))

def update_affiliation(memtype_values, comm_values, upciem_member_id):
    print('aff')
    sql = """
    UPDATE affiliation
    SET membership_type = %s,
        comm_firstchoice = %s
    WHERE valid_id= %s
    """
    db.modifydatabase(sql, (memtype_values, comm_values if comm_values else None, upciem_member_id))

def update_performance(performance_value, upciem_member_id):
    print('performance')
    sql="SELECT upciem_member_id from upciem_member where valid_id=%s"
    values=[upciem_member_id]
    cols=['id']
    df=db.querydatafromdatabase(sql,values,cols)
    upid=int(df['id'][0])
    sql = """
    UPDATE performance
    SET evaluation = %s
    WHERE upciem_member_id = %s
    """
    db.modifydatabase(sql, (performance_value, upid))