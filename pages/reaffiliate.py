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


# Generate a list of years for the dropdown
years = list(range(1908, 2099))
# Get the current year
current_year = datetime.now().year

comm_options=[
                {'label': "Academic Affairs Committee", 'value': "1"},
                {'label': "External Affairs Committee", 'value': "2"},            
                {'label': "Finance Committee", 'value': "3"},            
                {'label': "Internal Affairs Committee", 'value': "4"},            
                {'label': "Membership and Recruitment Committee", 'value': "5"},           
                {'label': "Publications and Records Committee", 'value': "6"},
                        ]

reaffiliation_form = dbc.Form(
    [
        html.Div([
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Student Number ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id = "student_number_list",
                            placeholder = "20XXXXXXX",
                            searchable = True,
                            options = [],
                        ), width = 4),
                    dbc.Col(
                        dbc.Button("New Member", id="new_mem_btn", color="primary", className="mb-3", style={"width":"100%",'display': 'block','font-size':'14px', 'backgroundColor': '#5474D5'}),
                        width = 2
                    ),
                ],  className="mb-2",
            ),
        ], id = 'exist_mem_row', style = {'display': 'block'}),

        html.Div([
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "Student Number ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='student_number_new',
                                placeholder="20XXXXXXX", maxLength=9, disabled=False),
                        width=4),
                    dbc.Col(
                        dbc.Button("Existing Member", id="exist_mem_btn", color="primary", className="mb-3", style={"width":"100%",'display': 'block','font-size':'14px'}),
                        width = 2
                    ),
                ], className="mb-2",
            ),
        ], id = 'new_mem_row', style = {'display': 'none'}),
        html.Br(),
        
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
                    dbc.Input(type="text", id='mem_fn', value='', placeholder = "Enter First Name", disabled=False),
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
                    dbc.Input(type="text", id='mem_mn', placeholder = "Enter Middle Name", disabled=False),
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
                    dbc.Input(type="text", id='mem_ln', placeholder = "Enter Surname", disabled=False),
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
                    dbc.Input(type="text", id='mem_sf', maxLength=5, placeholder = "Enter Suffix", disabled=False),
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
                    dbc.Input(type="date", id='mem_bd', disabled=False),
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
                    dbc.Input(type="text", id='mem_cn',
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
                    dbc.Input(type="text", id='mem_emergency',
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
                    dbc.Input(type="email", id='mem_email', placeholder = "example@gmail.com", disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "UP Email Address ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dbc.Input(type="email", id='mem_up_email', placeholder = "example@up.edu.ph", disabled=False),
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
                    dbc.Input(type="text", id='mem_pres_add', placeholder = "Street, City, Region", disabled=False),
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
                    dbc.Input(type="text", id='mem_perma_add', placeholder = "Street, City, Region", disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),

        html.Br(),
        html.H5(html.B('School and Membership Information')),
        
        html.Div([
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "App Batch ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id = "app_batch_list",
                            placeholder = "Eg. 20A",
                            searchable = True,
                            options = [],
                        ), width = 4)
                ],  className="mb-2",
            ),
        ], id = 'exist_batch_row', style = {'display': 'block'}),

        html.Div([
            dbc.Row(
                [
                    dbc.Label(
                        [
                            "App Batch ",
                            html.Span("*", style={"color": "#F8B237"})
                        ],
                        width=3),
                    dbc.Col(
                        dbc.Input(type="text", id='app_batch_new',
                                placeholder="Eg. 20A", maxLength=9, disabled=False),
                        width=4)
                ], className="mb-2",
            ),
        ], id = 'new_batch_row', style = {'display': 'none'}),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Batch Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='mem_year_batch',
                        options=[{'label': str(year), 'value': year} for year in years],
                        placeholder="Select a year",
                        clearable=False,
                        value=current_year  # default value can be set if needed
                    ),
                    width=4
                ),
            ],
            className="mb-2",
        ),

        dbc.Row(
            [
                dbc.Label(
                    [
                        "Year Standing ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='mem_year_standing',
                        options=[{'label': str(i), 'value': i} for i in range(1, 6)],
                        value=1,
                        searchable=False,
                        clearable=False
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Degree ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='mem_degree',
                        placeholder="Select Degree",
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Membership Type ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='memtype_id',
                        placeholder="Select Membership Type",
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Current Semester ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_sem',
                        options=(
                            {'label': "1st Semester", 'value': "1st"},
                            {'label': "2nd Semester", 'value': "2nd"}),
                        placeholder="Select Semester"
                    ),
                    width=4
                ),
            ],
            className="mb-2"
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Current Academic Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_acad_year',
                        options=(
                            {'label': "2020-2021", 'value': "2020-2021"},
                            {'label': "2021-2022", 'value': "2021-2022"},
                            {'label': "2022-2023", 'value': "2022-2023"},
                            {'label': "2023-2024", 'value': "2023-2024"},
                            {'label': "2024-2025", 'value': "2024-2025"},
                            {'label': "2025-2026", 'value': "2025-2026"}),
                        placeholder="Select Academic Year"
                    ),
                    width=4
                ),
            ],
            className="mb-2"
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Semester GWA ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                dbc.Input(
                    id='reaff_gwa',
                    type='number',
                    step='0.0001',
                    min=1,
                    max=5,
                    pattern=r'^\d+(\.\d{1,4})?$',  # Regex pattern for up to 4 decimals
                    placeholder='Enter GWA (up to 4 decimals)',
                ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Other Organization Affiliation ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='mem_other_org', value='', disabled=False, placeholder='Eg. UP ERG, UP CSA, CAPWA UP or put NA if none'),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        
        html.Br(),
        html.H5(html.B('Committee Preference')),
        dbc.Row(
            [
                html.P('This is a multi-select dropdown. Select with first choice being most preferred and sixth choice being least preferred. Note that no duplications of committees per choice.'),
            ]),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "First Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice1',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                )
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Second Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice2',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Third Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice3',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Fourth Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice4',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Fifth Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice5',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Sixth Choice: ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_choice6',
                        options=comm_options,
                        value='',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
                
            ],
            className="mb-2",
        ),
        
        html.Br(),
        html.H5(html.B('Reaffiliation Fee')),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "The Finance Committee has decided to set the reaffiliation fee to Php 150."
                        ),
                        html.Br(),
                        html.P(
                            "Payment of the reaffiliation fee upon submission of reaffiliation form is highly encouraged (but not required) as you will get a committee choice priority! "
                        ),
                        html.Br(),
                        html.P("You can pay your reaffiliation fee through:"),
                        html.P("GCash/Paymaya: 0995 973 6273 (Johann Daniel Alvarez)"),
                        html.P("PNB: 6334 1001 2523 (Johann Daniel Alvarez)"),
                        html.Br(),
                        html.P(
                            "For other concerns, you may message Johann Daniel Alvarez or any of the Finance Committee Core Team through Facebook Messenger."
                        ),
                    ],
                    width={"size": 8, "offset": 1},
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "When will you pay the Reaff Fee? ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='reaff_is_paid',
                        options=[
                            {'label': "Pay as I Submit the Reaff Form", 'value': "True"},
                            {'label': "Pay at a later date", 'value': "False"}
                        ],
                        value='Pay as I Submit the Reaff Form',
                        searchable=False,
                        clearable=False
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        #dbc.Row(
        #    [
        #        dbc.Col(
        #            dbc.Button("Submit", id="reaf-submit", color="primary", className="mb-3", style={'display': 'none'}),
        #            width={"size": 6, "offset": 3}
        #        )
        #    ]
        #),
        
        dbc.Button('Submit', id="submit_form_btn", n_clicks=0, style={'backgroundColor': '#5474D5'}),
        html.Div(id='output-message')  # For displaying output messages
    ],
)

#student number dropdown
@app.callback(
    [
        Output('student_number_list', 'options'),
    ],
    [
        Input('url', 'pathname'),
    ],
    State('student_number_list', 'value'),
)
def populate_mem_st_num_dropdown(pathname, searchterm):
    if pathname == '/reaffiliate' and not searchterm:
        sql = """
            select
                mem_id,
                mem_st_num
            from member
            where not mem_delete_ind
        """
        values = []

        if searchterm:
            sql += """
                AND mem_st_num ILIKE %s
                """
            values.append(f"%{searchterm}%")
            
        sql += " ORDER BY mem_st_num;"

        cols = ['mem_id', 'mem_st_num']
        result = db.querydatafromdatabase(sql, values, cols)
        options = [{'label': row['mem_st_num'], 'value': row['mem_id']} for _, row in result.iterrows()]

        return options,
    else:
        raise PreventUpdate

#student number row
        
# Degree dropdown
@app.callback(
    [
        Output('mem_degree', 'options'),
        Output('memtype_id', 'options'),
        Output('app_batch_list', 'options'),
    ],
    Input('url', 'pathname')
)
def populate_memdegree_dropdown(pathname):
    if pathname == '/reaffiliate':
        sql = """
        SELECT degree_name as label, degree_id  as value
        FROM Degree
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        mem_degree = df.to_dict('records')

        sql = """
        SELECT memtype_name as label, memtype_id  as value
        FROM memtype
        WHERE NOT memtype_delete_ind
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        memtype = df.to_dict('records')

        sql = """
        SELECT appbatch_name as label, appbatch_id  as value
        FROM appbatch
        WHERE NOT appbatch_delete_ind
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        appbatch = df.to_dict('records')

        return [mem_degree, memtype, appbatch]
    raise PreventUpdate

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        html.Div([
        dbc.Card([
            dbc.CardHeader("REAFFILIATION FORM", class_name='flex',
                           style={  'background-color': '#2E4178',
                                        'color': 'white',  # White text for header
                                        'font-size': '24px',
                                        'font-weight': 'bold'}),
            dbc.CardBody([
                dbc.Container(
                    [
                        reaffiliation_form,
                        html.Br(),
                    ], class_name=' flex homeshow'
                )
            ]),
    ]),],className='body') 
], className='flex body-container')
        ])


# FILLING THE FORM FOR EXISTING MEMBERS AND CLEARING IT AFTER SAVING

@app.callback(
    [
        Output('exist_mem_row', 'style'),
        Output('exist_batch_row', 'style'),
        Output('new_mem_row', 'style'),
        Output('new_batch_row', 'style'),

        Output('mem_fn', 'value'),
        Output('mem_mn', 'value'),
        Output('mem_ln', 'value'),
        Output('mem_sf', 'value'),
        Output('mem_bd', 'value'),

        Output('mem_cn', 'value'),
        Output('mem_emergency', 'value'),
        Output('mem_email', 'value'),
        Output('mem_up_email','value'),
        Output('mem_pres_add', 'value'),
        Output('mem_perma_add', 'value'),

        Output('mem_year_batch', 'value'),
        Output('mem_year_standing', 'value'),
        Output('mem_degree', 'value'),
        Output('memtype_id', 'value'),
        Output('reaff_sem','value'),
        Output('reaff_acad_year','value'),
        Output('mem_other_org', 'value'),

        Output('student_number_list', 'value'),
        Output('student_number_new', 'value'),
        Output('app_batch_list','value'),
        Output('app_batch_new','value'),
        Output('reaff_gwa', 'value'),

        Output('reaff_choice1','value'),
        Output('reaff_choice2','value'),
        Output('reaff_choice3','value'),
        Output('reaff_choice4','value'),
        Output('reaff_choice5','value'),
        Output('reaff_choice6','value'),
        Output('reaff_is_paid', 'value'),

        Output('output-message', 'children')
    ],
    [
        Input('exist_mem_btn', 'n_clicks'),
        Input('new_mem_btn', 'n_clicks'),
        Input('submit_form_btn', 'n_clicks'),
        Input('url', 'pathname'),
        Input('student_number_list', 'value'),
        Input('student_number_new', 'value')
    ],
    [
        State('mem_fn', 'value'),
        State('mem_mn', 'value'),
        State('mem_ln', 'value'),
        State('mem_sf', 'value'),
        State('mem_bd', 'value'),

        State('mem_cn', 'value'),
        State('mem_emergency', 'value'),
        State('mem_email', 'value'),
        State('mem_up_email','value'),
        State('mem_pres_add', 'value'),
        State('mem_perma_add', 'value'),

        State('mem_year_batch', 'value'),
        State('mem_year_standing', 'value'),
        State('mem_degree', 'value'),
        State('memtype_id', 'value'),
        State('reaff_sem','value'),
        State('reaff_acad_year','value'),
        State('mem_other_org', 'value'),

        State('app_batch_list','value'),
        State('app_batch_new','value'),
        State('reaff_gwa', 'value'),

        State('reaff_choice1','value'),
        State('reaff_choice2','value'),
        State('reaff_choice3','value'),
        State('reaff_choice4','value'),
        State('reaff_choice5','value'),
        State('reaff_choice6','value'),
        State('reaff_is_paid', 'value'),
     ],
)
def reaff_form_fill_and_submit(
                exist_btn,
                new_btn,
                submit,
                pathname,
                exist_mem,
                new_mem,
                
                mem_fn, 
                mem_mn,
                mem_ln, 
                mem_sf, 
                mem_bd, 
                
                mem_cn,
                mem_emergency, 
                mem_email, 
                mem_up_email,
                mem_pres_add, 
                mem_perma_add, 
                
                mem_year_batch,
                mem_year_standing, 
                mem_degree,
                memtype_id,
                reaff_sem,
                reaff_acad_year,
                mem_other_org, 

                mem_app_batch_exist,
                mem_app_batch_new,
                reaff_gwa,
                
                reaff_choice1,
                reaff_choice2,
                reaff_choice3,
                reaff_choice4,
                reaff_choice5,
                reaff_choice6,
                reaff_is_paid):

    current_datetime = datetime.today()
    current_date = current_datetime.date()

    if not reaff_is_paid:
        current_date = None

    if pathname == '/reaffiliate':
        ctx = dash.callback_context

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == "submit_form_btn" and submit:
                if exist_mem:

                    variable = [reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6]

                    seen = set()
                    duplicate = False

                    for comm in variable:
                        if comm in seen:
                            duplicate = True
                            break
                        seen.add(comm)

                    if not(
                        mem_fn and 
                        mem_ln and 
                        mem_bd and 

                        mem_cn and 
                        mem_emergency and 
                        mem_email and 
                        mem_up_email and 
                        mem_pres_add and 
                        mem_perma_add and 

                        mem_year_batch and
                        mem_year_standing and 
                        mem_degree and 
                        memtype_id and 
                        reaff_sem and 
                        reaff_acad_year and 
                        mem_other_org and

                        mem_app_batch_exist and
                        reaff_gwa and
                        
                        reaff_choice1 and
                        reaff_choice2 and
                        reaff_choice3 and
                        reaff_choice4 and 
                        reaff_choice5 and
                        reaff_choice6 and 
                        reaff_is_paid             
                    ):
                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Please fill in all required fields.", style={'color': 'red'})]
                    elif duplicate:
                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Please choose different committees per rank preference", style={'color': 'red'})]

                    else:
                        sql = """
                            UPDATE member
                            SET
                                mem_fn=%s,
                                mem_mn=%s,
                                mem_ln=%s,
                                mem_sf=%s,
                                mem_bd=%s,
                                mem_cn=%s,
                                mem_emergency=%s,
                                mem_email=%s,
                                mem_up_email=%s,
                                mem_pres_add=%s,
                                mem_perma_add=%s,
                                mem_year_batch=%s,
                                mem_year_standing=%s,
                                degree_id=%s,
                                mem_other_org=%s,
                                status_id=%s,
                                memtype_id=%s,
                                mem_reaffiliated=%s,
                                mem_is_new=%s,
                                appbatch_id=%s
                            WHERE 
                                NOT mem_delete_ind
                                AND mem_id=%s
                        """
                        values = [mem_fn, mem_mn, mem_ln, mem_sf, mem_bd, mem_cn, 
                                  mem_emergency, mem_email, mem_up_email, mem_pres_add, mem_perma_add, mem_year_batch, mem_year_standing, 
                                  mem_degree, mem_other_org, '1', memtype_id, True, False, mem_app_batch_exist, exist_mem]
                        db.modifydatabase(sql, values)

                        sql ="""
                            INSERT INTO reaffiliation(
                                    reaff_sem,
                                    reaff_gwa,
                                    reaff_acad_year,
                                    reaff_choice1,
                                    reaff_choice2,
                                    reaff_choice3,
                                    reaff_choice4,
                                    reaff_choice5,
                                    reaff_choice6,
                                    reaff_is_new,
                                    reaff_is_paid,
                                    reaff_date_paid,
                                    mem_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                        values = (reaff_sem, reaff_gwa, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, False, reaff_is_paid, current_date, exist_mem)
                        db.modifydatabase(sql, values)

                        sql ="""
                            SELECT max(reaff_id)
                            FROM reaffiliation
                        """                       
                        values = []
                        df = db.querydatafromdatabase(sql,values)
                        reaff_id = int(df.loc[0,0])

                        sql = """
                            SELECT reaff_sem
                            FROM reaffiliation
                            WHERE not reaff_delete_ind
                                AND reaff_acad_year = %s
                                AND mem_id = %s
                        """
                        values = [reaff_acad_year, exist_mem]
                        df = db.querydatafromdatabase(sql,values)

                        if df.empty:
                            if reaff_sem == '1st':
                                sql = """
                                INSERT INTO performance(
                                    perf_acad_year,
                                    perf_reaff_comm1,
                                    perf_reaff_comm2,
                                    mem_id
                                )
                                VALUES(%s, %s, %s, %s)
                                """
                            values = (reaff_acad_year, reaff_id, None, exist_mem)
                            db.modifydatabase(sql, values)

                            if reaff_sem == '2nd':
                                sql = """
                                INSERT INTO performance(
                                    perf_acad_year,
                                    perf_reaff_comm1,
                                    perf_reaff_comm2,
                                    mem_id
                                )
                                VALUES(%s, %s, %s, %s)
                                """
                            values = (reaff_acad_year, None, reaff_id, exist_mem)
                            db.modifydatabase(sql, values)


                        if not df.empty:
                            prev_sem = df.loc[0,0]
                            if prev_sem == '2nd':
                                sql = """
                                INSERT INTO performance(
                                    perf_acad_year,
                                    perf_reaff_comm1,
                                    perf_reaff_comm2,
                                    mem_id
                                )
                                VALUES(%s, %s, %s, %s)
                                """
                            values = (reaff_acad_year, reaff_id, None, exist_mem)
                            db.modifydatabase(sql, values)

                            if prev_sem == '1st':
                                sql = """
                                INSERT INTO performance(
                                    perf_acad_year,
                                    perf_reaff_comm1,
                                    perf_reaff_comm2,
                                    mem_id
                                )
                                VALUES(%s, %s, %s, %s)
                                """
                            values = (reaff_acad_year, None, reaff_id, exist_mem)
                            db.modifydatabase(sql, values)
                        
                        message = "Existing Member Reaffiliated Successfully"

                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                            html.Div(message, style={'color': 'green'})]

                if new_mem:

                    variable = [reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6]

                    seen = set()
                    duplicate = False

                    for comm in variable:
                        if comm in seen:
                            duplicate = True
                            break
                        seen.add(comm)

                    if not(
                        mem_fn and 
                        mem_ln and 
                        mem_bd and 

                        mem_cn and 
                        mem_emergency and 
                        mem_email and 
                        mem_up_email and 
                        mem_pres_add and 
                        mem_perma_add and 

                        mem_year_batch and
                        mem_year_standing and 
                        mem_degree and 
                        memtype_id and 
                        reaff_sem and 
                        reaff_acad_year and 
                        mem_other_org and

                        mem_app_batch_new and
                        reaff_gwa and
                        
                        reaff_choice1 and
                        reaff_choice2 and
                        reaff_choice3 and
                        reaff_choice4 and 
                        reaff_choice5 and
                        reaff_choice6 and 
                        reaff_is_paid             
                    ):
                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Please fill in all required fields.", style={'color': 'red'})]
                    elif duplicate:
                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            html.Div("Please choose different committees per rank preference", style={'color': 'red'})]

                    else:
                        sql = """
                            SELECT appbatch_id
                            FROM appbatch
                            WHERE appbatch_name=%s
                        """
                        value = [mem_app_batch_new]
                        df = db.querydatafromdatabase(sql,value)

                        if df.empty:
                            sql = """
                                INSERT INTO appbatch(
                                    appbatch_name
                                )
                                VALUES(%s)
                            """
                            value = (mem_app_batch_new)
                            db.modifydatabase(sql, value)

                            sql = """
                                SELECT appbatch_id
                                FROM appbatch
                                WHERE appbatch_name=%s
                            """
                            value = [mem_app_batch_new]
                            df = db.querydatafromdatabase(sql,value)
                            mem_app_batch_new = int(df.loc[0,0])
                        else:
                            mem_app_batch_new = int(df.loc[0,0])
                            

                        sql = """
                            INSERT INTO member(
                                mem_fn,
                                mem_mn,
                                mem_ln,
                                mem_sf,
                                mem_st_num,
                                mem_bd,
                                mem_cn,
                                mem_emergency,
                                mem_email,
                                mem_up_email,
                                mem_pres_add,
                                mem_perma_add,
                                mem_year_batch,
                                mem_year_standing,
                                degree_id,
                                mem_other_org,
                                status_id,
                                memtype_id,
                                mem_reaffiliated,
                                mem_is_new,
                                appbatch_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        values = (mem_fn, mem_mn, mem_ln, mem_sf, new_mem, mem_bd, mem_cn, mem_emergency, mem_email, mem_up_email, 
                                mem_pres_add, mem_perma_add, mem_year_batch, mem_year_standing, mem_degree, mem_other_org, '1', memtype_id, True, True, mem_app_batch_new)
                        db.modifydatabase(sql, values)

                        sql ="""
                            SELECT max(mem_id)
                            FROM member
                        """
                        values = []
                        df = db.querydatafromdatabase(sql,values)
                        mem_id = int(df.loc[0,0])

                        sql ="""
                            INSERT INTO reaffiliation(
                                    reaff_sem,
                                    reaff_gwa,
                                    reaff_acad_year,
                                    reaff_choice1,
                                    reaff_choice2,
                                    reaff_choice3,
                                    reaff_choice4,
                                    reaff_choice5,
                                    reaff_choice6,
                                    reaff_is_new,
                                    reaff_is_paid,
                                    reaff_date_paid,
                                    mem_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                        values = (reaff_sem, reaff_gwa, reaff_acad_year, reaff_choice1, reaff_choice2, reaff_choice3, reaff_choice4, reaff_choice5, reaff_choice6, True, reaff_is_paid, current_date, mem_id)
                        db.modifydatabase(sql, values)

                        sql ="""
                            SELECT max(reaff_id)
                            FROM reaffiliation
                        """                       
                        values = []
                        df = db.querydatafromdatabase(sql,values)
                        reaff_id = int(df.loc[0,0])

                        print(reaff_sem)

                        if reaff_sem == '1st':
                            print("activated1")
                            sql = """
                            INSERT INTO performance(
                                perf_acad_year,
                                perf_reaff_comm1,
                                perf_reaff_comm2,
                                mem_id
                            )
                            VALUES(%s, %s, %s, %s)
                            """
                        values = (reaff_acad_year, reaff_id, None, mem_id)
                        db.modifydatabase(sql, values)

                        if reaff_sem == '2nd':
                            print("activated2")
                            sql = """
                            INSERT INTO performance(
                                perf_acad_year,
                                perf_reaff_comm1,
                                perf_reaff_comm2,
                                mem_id
                            )
                            VALUES(%s, %s, %s, %s)
                            """
                        values = (reaff_acad_year, None, reaff_id, mem_id)
                        db.modifydatabase(sql, values)

                        message = "New Member Affiliated Successfully"

                        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                            html.Div(message, style={'color': 'green'})]

            if pathname == '/reaffiliate' and eventid == "new_mem_btn" and new_btn:
                return [{'display': 'none'}, {'display': 'none'}, {'display': 'block'}, {'display': 'block'},
                                None, None, None, None, None, 
                                None, None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                            html.Div(style={'display': 'none'})]
            
            if pathname == '/reaffiliate' and eventid == "exist_mem_btn" and exist_btn:
                return [{'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'},
                                None, None, None, None, None, 
                                None, None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                                None, None, None, None, None, 
                                None, None, None, None, None, None, None, 
                            html.Div(style={'display': 'none'})]

    if pathname == '/reaffiliate' and exist_mem:
        sql = """
            select
                mem_fn,
                mem_mn,
                mem_ln,
                mem_sf,
                mem_bd,
                mem_cn,
                mem_emergency,
                mem_email,
                mem_up_email,
                mem_pres_add,
                mem_perma_add,
                mem_year_batch,
                mem_year_standing,
                degree_id,
                mem_other_org,
                appbatch_id
            from member
            where
                NOT mem_delete_ind AND
                mem_id = %s
            """
            
        values = [exist_mem]
        cols = [
            'mem_fn',
            'mem_mn',
            'mem_ln',
            'mem_sf',
            'mem_bd',
            'mem_cn',
            'mem_emergency',
            'mem_email',
            'mem_up_email',
            'mem_pres_add',
            'mem_perma_add',
            'mem_year_batch',
            'mem_year_standing',
            'degree_id',
            'mem_other_org',
            'appbatch_id'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        fn = df['mem_fn'][0]
        mn = df['mem_mn'][0]
        ln = df['mem_ln'][0]
        sf = df['mem_sf'][0]
        bd = df['mem_bd'][0]
        cn = df['mem_cn'][0]
        emergency = df['mem_emergency'][0]
        email = df['mem_email'][0]
        upmail = df['mem_up_email'][0]
        pres_add = df['mem_pres_add'][0]
        perma_add = df['mem_perma_add'][0]
        year_batch = df['mem_year_batch'][0]
        year_standing = df['mem_year_standing'][0]
        degree = df['degree_id'][0]
        other_org = df['mem_other_org'][0]
        app_batch = df['appbatch_id'][0]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update,
            fn, mn, ln, sf, bd, 
            cn, emergency, email, upmail, pres_add, perma_add, 
            year_batch, year_standing, degree, dash.no_update, dash.no_update, dash.no_update, other_org, 
            exist_mem, None, app_batch, None, None,
            dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
            html.Div(style={'disply': 'none'})]    

    else:
        raise PreventUpdate
    
        """
        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                 None, None, None, None, None, 
                 None, None, None, None, None, None, 
                 None, None, None, None, None, None, None, 
                 None, None, None, None, None, 
                 None, None, None, None, None, None, None, 
                 html.Div(style={'disply': 'none'})] """
