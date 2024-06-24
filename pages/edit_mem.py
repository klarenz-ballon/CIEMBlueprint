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
import urllib.parse

# Define the form layout

edit_mem_form = dbc.Form(
    [
        html.H5(html.B('Personal Information')),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Name ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memfirst_name', value='', disabled=False),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Middle Name ",
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memmiddle_name', disabled=False),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Surname ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memlast_name', disabled=False),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Suffix ",
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memsuffix', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "ID Number ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memvalid_id', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Birthday ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="date", id='membirthdate', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        html.Br(),
        html.H5(html.B('Contact Information')),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Contact Number ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='memcontact_number',
                              placeholder="09XXXXXXXXX", maxLength=11, disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Emergency Contact Number ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='emergency_memcontact_number',
                              placeholder="09XXXXXXXXX", maxLength=11, disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Email Address ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dbc.Input(type="email", id='mememail', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Present Address ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dbc.Input(type="text", id='mempresent_address', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Permanent Address ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dbc.Input(type="text", id='mempermanent_address', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

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
                                multi=True,
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
                                multi=True,
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
                                multi=True,
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
        html.H5(html.B('Accountabilities')),
        dbc.Row(
            [
                html.P('You may choose from the dropdown menu to clear accountabilities.'),
                dbc.Col(
                    dbc.InputGroup(
                        [
                            dcc.Dropdown(
                                id='comm_dropdown',
                                options=[
                                    {'label': 'Pay as I Submit the Reaff Form', 'value': 'Pay as I Submit the Reaff Form'},
                                    {'label': 'Pay at a later date', 'value': 'Pay at a later date'},
                                    {'label': 'Paid', 'value': 'Paid'}
                                ],
                                multi=True,
                                placeholder="Edit Accountabilities",
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
                    dbc.Button("Submit", id="memsubmit-button", color="primary", className="mb-3", style={'display': 'none'}),
                    width={"size": 6, "offset": 3}
                )
            ],
        ),
        dbc.Button('Submit',id='memsubmit-button'),
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
                    [
                        edit_mem_form,
                    ]
                )
                  ]),
                ])
                ]) 
    ], className='body')
        ])

@app.callback(
    [Output('memoutput-message', 'children'),
     Output('memfirst_name', 'value'),
     Output('memmiddle_name', 'value'),
     Output('memlast_name', 'value'),
     Output('memsuffix', 'value'),
     Output('memvalid_id', 'value'),
     Output('membirthdate', 'value'),
     Output('memcontact_number', 'value'),  # Fixing the ID here
     Output('emergency_memcontact_number', 'value'),
     Output('mememail', 'value'),
     Output('mempresent_address', 'value'),
     Output('mempermanent_address', 'value'),
     ],
    [Input('memsubmit-button', 'n_clicks'),Input('url','pathname'),Input('url','search')],
    [State('memfirst_name', 'value'),
     State('memmiddle_name', 'value'),
     State('memlast_name', 'value'),
     State('memsuffix', 'value'),
     State('memvalid_id', 'value'),
     State('membirthdate', 'value'),
     State('memcontact_number', 'value'),  # Fixing the ID here
     State('emergency_memcontact_number', 'value'),
     State('mememail', 'value'),
     State('mempresent_address', 'value'),
     State('mempermanent_address', 'value'),
     State('memtype_dropdown', 'value'),
    State('memstat_dropdown', 'value'),
    State('comm_dropdown', 'value'),
    State('performance', 'value')
    
     ]
)
def submit_form(n_clicks,pathname,search, memfirst_name, memmiddle_name, memlast_name, memsuffix, memvalid_id, membirthdate, memcontact_number,
                emergency_memcontact_number, mememail, mempresent_address, mempermanent_address, memtype_dropdown, memstat_dropdown, comm_dropdown,performance):
    
    if n_clicks is None:
        if pathname.startswith('/edit_mem') and len(search)>4:
            parsed = urllib.parse.urlparse(search)
            parsed_dict = urllib.parse.parse_qs(parsed.query)
            print(parsed_dict)
            sql="SELECT * FROM person WHERE valid_id=%s"
            values=[parsed_dict['id'][0]]
            columns=['id','fname','mname','lname','sfx','bday','cn','ecn','email','pra','pea','acctid','persondel']
            df=db.querydatafromdatabase(sql,values,columns)
            #always assume meron
            return dash.no_update, df['fname'][0],df['mname'][0],df['lname'][0],df['sfx'][0],parsed_dict['id'][0],df['bday'][0],df['cn'][0],df['ecn'][0],df['email'][0],df['pra'][0],df['pea'][0]
        else:
            raise PreventUpdate

    if not (memfirst_name and memlast_name and memvalid_id and membirthdate and memcontact_number and emergency_memcontact_number and mememail and mempresent_address and mempermanent_address and memtype_dropdown and memstat_dropdown and comm_dropdown and performance):
        return html.Div("Please fill in all required fields.", style={'color': 'red'}),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update

    try:
        # Check if the person already exists
        sql = "SELECT valid_id FROM person WHERE valid_id=%s"
        df = db.querydatafromdatabase(sql, [memvalid_id], ['valid_id'])

        if df.shape[0]:
            print(df)  # Check the DataFrame returned by the query
            print(df.shape)  # Check the shape of the DataFrame
            # Update existing person's information
            sql = """
                UPDATE person
                SET
                    first_name=%s,
                    middle_name=%s,
                    last_name=%s,
                    suffix=%s,
                    birthdate=%s,
                    contact_number=%s,
                    emergency_contact_number=%s,
                    email=%s,
                    present_address=%s,
                    permanent_address=%s

            """
            if memmiddle_name is None:
                memmiddle_name=''
            if memsuffix is None:
                memsuffix=''
            values = [memfirst_name, memmiddle_name, memlast_name, memsuffix, membirthdate, memcontact_number, emergency_memcontact_number, mememail, mempresent_address, mempermanent_address]
            sql+=" WHERE valid_id='{memvalid_id}';"
            db.modifydatabase(sql, values)
            sql='UPDATE upciem_member WHERE valid_id=%s'
            values=[memvalid_id]
            db.modifydatabase(sql,values)
            # Update SPECIALIZATION information
            sql = """
                INSERT INTO affiliation(membership_type,valid_id) 
                VALUES(%s,%s)
            """
            values = [','.join(memtype_dropdown),memvalid_id]
            db.modifydatabase(sql, values)
            
            sql = """
                INSERT INTO upciem_member(active_status,valid_id) 
                VALUES(%s,%s)
            """
            values = [','.join(memstat_dropdown),memvalid_id]
            db.modifydatabase(sql, values)

            sql = """
                INSERT INTO committee(committee_name,valid_id) 
                VALUES(%s,%s)
            """
            values = [','.join(comm_dropdown),memvalid_id]
            db.modifydatabase(sql, values)

            sql = """
                INSERT INTO performance(evaluation,valid_id) 
                VALUES(%s,%s)
            """
            values = [','.join(performance),memvalid_id]
            db.modifydatabase(sql, values)



            message = "Existing upciem member information updated successfully."
        else:
            # Insert new person
            sql = """
            INSERT INTO person(valid_id, first_name, middle_name, last_name, suffix, birthdate, contact_number, emergency_contact_number, email, present_address, permanent_address)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = [memvalid_id, memfirst_name, memmiddle_name, memlast_name, memsuffix, membirthdate, memcontact_number, emergency_memcontact_number, mememail, mempresent_address, mempermanent_address]
            db.modifydatabase(sql, values)
            sql="INSERT INTO alumni(valid_id,specialization) VALUES (%s,%s)"
            values=[memvalid_id,dropdown]
            db.modifydatabase(sql, values)
            #Adding to upciem_member
            message = "New alumni successfully added."

        return html.Div(message, style={'color': 'green'}),'','','','','','','','','','',''

    except Exception as e:
        return html.Div(f"An error occurred: {str(e)}", style={'color': 'red'})
