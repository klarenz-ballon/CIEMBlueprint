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

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        dbc.Button("Go Back", 
            id="back_btn", 
            color="primary",
            href='/members',
            style={'background-color': '#5474D5'}
            ),
        dbc.Card([
            dbc.CardHeader("MEMBER INFORMATION",
                                   style={  'background-color': '#2E4178',
                                        'color': 'white',  # White text for header
                                        'font-size': '24px',
                                        'font-weight': 'bold'}),
            dbc.CardBody([
                # First row (1 card)
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("PERSONAL", className = "flex-grow-1"),
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col(html.H6(['First Name ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width=2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_fn', disabled=False),
                                                ),width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6('Middle Name'), width = 2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_mn', disabled=False),
                                                ),width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Last Name ', 
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_ln', disabled=False),
                                                ),width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6('Suffix'), width = 2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_sf', disabled=False),
                                                ),width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                html.Hr(),
                                dbc.Row([
                                    dbc.Col(html.H6(['Student Number ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_st_num',  maxLength=9, disabled=False),
                                                ),width=4),
                                    dbc.Col(html.H6(['Degree ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col((dcc.Dropdown(id='member_degree', disabled=False),
                                                ),width=4),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Birthday ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_bd', disabled=False),
                                                ),width=4),
                                ], style={"align-items": "center"}, className="mb-2"),
                            ])
                        ]),
                        width=12,  # Full width for single card
                        className="mb-1"  # Margin below the card
                    )
                ]),
                
                # Second row (2 cards)
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("CONTACT", className = "flex-grow-1")
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                 dbc.Row([
                                    dbc.Col(html.H6(['Contact Number ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_cn',maxLength=11, disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Emergency Contact Number ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_emergency',maxLength=11 , disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Email Address ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_email', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['UP Email Address ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_up_email', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Present Address ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_pres_add', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Permanent Address ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_perma_add', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                    ])
                                ]),
                                width=6,  # Half width for each card in a row of 2
                                className="mr-2 mb-1"  # Margin between and below cards
                            ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("SCHOOL & MEMBERSHIP", className = "flex-grow-1")
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col(html.H6(['Batch Year ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_year_batch', maxLength=4, disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['App Batch ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    #dbc.Col(html.H3(dbc.Input(type="text", id='mem_app_batch', disabled=False),
                                    #            ),width=7),
                                    dbc.Col((dcc.Dropdown(id='mem_appbatch_list', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Year Standing ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_year_standing', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Membership Type ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col((dcc.Dropdown(id='memtype_name', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Other Organizations ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col(html.H3(dbc.Input(type="text", id='member_other_org', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Membership Status ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 5),
                                    dbc.Col((dcc.Dropdown(id='status_name', disabled=False),
                                                ),width=7),
                                ], style={"align-items": "center"}, className="mb-2"),
                            ])
                        ]),
                        width=6,  # Half width for each card in a row of 2
                        className="ml-2 mb-1"  # Margin between and below cards
                    )
                ]),
                # Third row (1 card)
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("REAFFILIATION & COMMITTEE ASSIGNMENT", className = "flex-grow-1")
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col(html.H6(['A.Y. ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 1),
                                    dbc.Col((dcc.Dropdown(id='reaff_edit_acad_year', disabled=False),
                                                ),width=3),
                                    dbc.Col(html.H6(['Sem ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 1),
                                    dbc.Col((dcc.Dropdown(id='reaff_edit_sem', disabled=False),
                                                ),width=3),
                                    dbc.Col(html.H6(['GWA ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 1),
                                    dbc.Col((dbc.Input(id='reaff_edit_gwa', type='number',
                                                    step='0.0001',
                                                    min=1,
                                                    max=5,
                                                    pattern=r'^\d+(\.\d{1,4})?$', disabled=False),
                                                ),width=3),
                                ], style={"align-items": "center"}, className="mb-2"),
                                html.Hr(),
                                #dbc.Row([
                                 #  dbc.Col(html.H6(['Reaffiliated ',
                                 #                   html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                #   dbc.Col((dcc.Dropdown(id='member_edit_reaffiliated', options = [{'label': "Yes", 'value': True},{'label': "No", 'value': False}], disabled=False),
                                #                ),width=10),
                               # ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Date Reaffiliated ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col((dbc.Input(type="date", id='reaff_edit_date', disabled=False),
                                            ), width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Paid:', 
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col((dcc.Dropdown(id='reaff_edit_is_paid', options = [{'label': "Yes", 'value': True},{'label': "No", 'value': False}], disabled=False),
                                                ),width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6('Date Paid ',
                                                    ), width = 2),
                                    dbc.Col((dbc.Input(type="date", id='reaff_edit_date_paid', disabled=False),
                                            ), width=10),
                                ], style={"align-items": "center"}, className="mb-2"),
                                html.Hr(),
                                html.H5('Committee Preferences'),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col(html.H6(['First Choice ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice1',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                    dbc.Col(html.H6(['Fourth Choice ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice4',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                ], justify='between', style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Second Choice ',
                                                    html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice2',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                    dbc.Col(html.H6(['Fifth Choice ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice5',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                ], justify='between', style={"align-items": "center"}, className="mb-2"),
                                dbc.Row([
                                    dbc.Col(html.H6(['Third Choice ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice3',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                    dbc.Col(html.H6(['Sixth Choice ',
                                                     html.Span("*", style={"color": "#F8B237"})]), width = 2),
                                    dbc.Col(dcc.Dropdown(
                                        id='reaff_edit_choice6',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 4),
                                ], justify='between', style={"align-items": "center"}, className="mb-2"),
                                html.Hr(),
                                dbc.Row([
                                    dbc.Col(html.H6('Committee Assignment '), width = 3),
                                    dbc.Col(dcc.Dropdown(
                                        id='edit_assigned_comm',
                                        options = comm_options,
                                        searchable=False,
                                        clearable=False
                                    ), width = 9),
                                ], justify='between', style={"align-items": "center"}, className="mb-2"),
                            ])
                        ]),
                        width=12,  # Full width for single card
                        className="mb-1"  # Margin below the card
                    )
                ]),
                # Fourth row (2 cards)
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("PERFORMANCE", className = "flex-grow-1"),
                                    #dbc.Col(
                                        #dbc.Button("Add", id="add_perf_btn", href="/performance?mode=add&id=", color="primary", style={"width":"100%",'display': 'none','font-size':'14px'}),
                                        #width = 2
                                        #    ),
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                dbc.Container(["No Performances to Display"], id="perf-table", class_name='table-wrapper p-3', style={'margin-top':'0em'})
                                
                            ])
                        ]),
                        width=12,
                        className="mr-0"  # Margin between and below cards
                    ),
                    
                ]),
                
                dbc.Row(
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader(
                                html.Div([
                                    html.H5("HEADSHIP", className = "flex-grow-1"),
                                    dbc.Col(
                                        dbc.Button("Add", id="add_head_btn", href="/headship?mode=add&mem_id=", color="primary", style={"width":"100%",'display': 'block','font-size':'14px','background-color':'#5474D5'}),
                                        width = 2
                                            ),
                                ], className = "d-flex align-items-center justify-content-between"),
                                style={'background-color': '#E8EDF7'}
                            ),
                            dbc.CardBody([
                                dbc.Container(["No Headships to Display"], id="headship-table", class_name='table-wrapper p-3', style={'margin-top':'0em'})
                                
                            ])
                        ]),
                        width=12,
                        className="ml-2"  # Margin between and below cards
                    )
                )


            ]),
            
        ], className="ml-4 mr-4 mt-4"),
            # Add margin to the main card
            dbc.Button("Save Update", 
                                    id="save_btn", 
                                    color="primary",
                                    ),
            html.Div(id='member_output_message'),
            html.Div(id='reaff_output_message')
    ], className="body"),  # Add a class to style the main content area
])


#performance table
@app.callback(
    Output('perf-table', 'children'),
    #Output('add_perf_btn', 'href'),  # Add this output to update the href of the add button
    Input('url', 'search')
)
def perf_table(url_search):
    parsed = urlparse(url_search)
    query_mem_id = parse_qs(parsed.query)

    if 'id' in query_mem_id:
        mem_id = query_mem_id['id'][0]
        sql = '''
            SELECT
                perf_acad_year,
                CASE
                    WHEN p.perf_reaff_comm1 IS NULL THEN 'Non-Reaffiliated'
                    WHEN c1.comm_name IS NULL THEN 'Waiting for Committee'
                    ELSE c1.comm_name
                END as FirstSem,
                COALESCE(perf_comm1_score, '0') as FirstSemScore,
                CASE
                    WHEN p.perf_reaff_comm2 IS NULL THEN 'Non-Reaffiliated'
                    WHEN c2.comm_name IS NULL THEN 'Waiting for Committee'
                    ELSE c2.comm_name
                END as SecondSem,
                COALESCE(perf_comm2_score, '0') as SecondSemScore,
                COALESCE(perf_eval, '0') as perf_eval,
                perf_id
            FROM performance p
            LEFT JOIN reaffiliation r1 on r1.reaff_id = p.perf_reaff_comm1
            LEFT JOIN committee c1 on c1.comm_id = r1.reaff_assigned_comm
            LEFT JOIN reaffiliation r2 on r2.reaff_id = p.perf_reaff_comm2
            LEFT JOIN committee c2 on c2.comm_id = r2.reaff_assigned_comm
            JOIN member m ON p.mem_id = m.mem_id
            WHERE m.mem_id = %s AND (perf_delete_ind IS NULL OR perf_delete_ind = FALSE)
        '''
        values = [mem_id]
        cols = ['Academic Year', '1st Sem Committee', '1st Sem Score', '2nd Sem Committee', '2nd Sem Score', 'Performance', 'Update']
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            df.fillna('Null', inplace=True)
            df['Update'] = df['Update'].apply(lambda x: f'<div style="text-align: center;"><a href="/performance?perf_id={x}"><button class="btn btn-primary btn-sm" style="font-size: 12px; background-color: 5474D5;">Edit</button></a>')
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Graduated?' or 'Member Info' else {'name': i, 'id': i} for i in df.columns],
                markdown_options={'html': True},
                style_cell={
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '12px',
                    'color': '#000000',
                    'height': '40px',
                    'padding': '5px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                },
                style_header={
                    'background-color': '#2E4178',
                    'color': 'white',
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px',
                    'font-weight': 'bold',
                    'border-bottom': '2px solid #dee2e6',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#E8EFFF'
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#ffffff'
                    },
                ],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                page_action='native',
                page_size=10,
                style_table={'height': '200%', 'overflow': 'auto'}
            )
            #add_perf_btn_href = f"/performance?mode=add&id={mem_id}"
            #return [table], add_perf_btn_href
            return [table]
        #return ["No Performances to Display"], f"/performance?mode=add&id={mem_id}"
        return ["No Performances to Display"]
    raise PreventUpdate


#headship table
@app.callback(
    Output('headship-table', 'children'),
    Output('add_head_btn', 'href'),  # Add this output to update the href of the add button
    Input('url', 'search')
)
def headship_table(url_search):
    parsed = urlparse(url_search)
    query_mem_id = parse_qs(parsed.query)

    if 'id' in query_mem_id:
        mem_id = query_mem_id['id'][0]
        sql = '''
            SELECT 
                headscore_acad_year,
                head_name,
                headscore_description,
                headscore_score,
                s.head_id,
                m.mem_id
            FROM 
                headship_score s
            JOIN headship h
            ON s.head_id = h.head_id
            INNER JOIN member m
            ON s.mem_id = m.mem_id
            WHERE m.mem_id = %s AND (headscore_delete_ind IS NULL OR headscore_delete_ind = FALSE)
            ORDER BY headscore_score DESC
        '''
        values = [mem_id]
        cols = ['Academic Year', 'Headship', 'Headship Description', 'Score', 'head_id', 'mem_id']
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            df['Update'] = df.apply(lambda row: f'<div style="text-align: center;"><a href="/headship?mode=edit&mem_id={row["mem_id"]}&head_id={row["head_id"]}"><button class="btn btn-primary btn-sm" style="font-size: 12px;background-color: #5474D5;">Edit</button></a></div>', axis=1)
            df = df.drop(columns=['head_id', 'mem_id'])  # Drop these columns if you don't want them in the final table

            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Update' else {'name': i, 'id': i} for i in df.columns],
                markdown_options={'html': True},
                style_cell={
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '12px',
                    'color': '#000000',
                    'height': '40px',
                    'padding': '5px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                },
                style_header={
                    'background-color': '#2E4178',  # Blue background for header
                    'color': 'white',  # White text for header
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px',
                    'font-weight': 'bold',
                    'border-bottom': '2px solid #dee2e6',  # Border for separation
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#E8EFFF'  # Light grey for odd rows
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': '#ffffff'  # White for even rows
                    },
                ],
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                page_action='native',
                page_size=10,
                style_table={'height': '200%', 'overflow': 'auto'}
            )
            add_head_btn_href = f"/headship?mode=add&mem_id={mem_id}"
            return [table], add_head_btn_href
        return ["No Headships to Display"], f"/headship?mode=add&mem_id={mem_id}"
    raise PreventUpdate

# DROPDOWN CALLBACK
@app.callback(
    [
        Output('memtype_name', 'options'),
        Output('status_name', 'options'),
        Output('member_degree', 'options'),
        Output('mem_appbatch_list', 'options'),
        Output('reaff_edit_acad_year', 'options'),
        Output('reaff_edit_sem', 'options'),
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('reaff_edit_acad_year', 'options'),
        Input('reaff_edit_sem', 'options'),
    ],
)
def populate_dropdowns(url_search, pathname, acad_year, acad_sem):
    parsed = urlparse(url_search)
    query_mem_id = parse_qs(parsed.query)
    mem_id = query_mem_id['id'][0]

    if pathname == '/mem_vieweditinfo':
        
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
        SELECT status_name as label, status_id  as value
        FROM status
        WHERE NOT status_delete_ind
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        status = df.to_dict('records')

        sql = """
        SELECT degree_name as label, degree_id  as value
        FROM Degree
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        mem_degree = df.to_dict('records')

        sql = """
        SELECT appbatch_name as label, appbatch_id  as value
        FROM appbatch
        WHERE NOT appbatch_delete_ind
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        
        appbatch = df.to_dict('records')

        academic_year = []
        academic_sem = []
        if acad_sem:

            sql = """
                SELECT reaff_acad_year as label, reaff_acad_year as value
                FROM (
                    SELECT DISTINCT reaff_acad_year, CAST(SUBSTRING(reaff_acad_year FROM 1 FOR 4) AS INTEGER) AS start_year
                    FROM reaffiliation
                    WHERE NOT reaff_delete_ind AND mem_id = %s AND reaff_sem = %s
                ) AS sorted_years
                ORDER BY start_year ASC;
                """
            values = [mem_id, acad_sem]

            cols = ['label', 'value']
            df = db.querydatafromdatabase(sql, values, cols)
            
            academic_year = df.to_dict('records')
        
        else: 
            sql = """
                SELECT reaff_acad_year as label, reaff_acad_year as value
                FROM (
                    SELECT DISTINCT reaff_acad_year, CAST(SUBSTRING(reaff_acad_year FROM 1 FOR 4) AS INTEGER) AS start_year
                    FROM reaffiliation
                    WHERE NOT reaff_delete_ind AND mem_id = %s
                ) AS sorted_years
                ORDER BY start_year ASC;
                """
            values = [mem_id]

            cols = ['label', 'value']
            df = db.querydatafromdatabase(sql, values, cols)
            
            academic_year = df.to_dict('records')

        if acad_year:
            sql = """
                SELECT reaff_sem as label, reaff_sem as value
                FROM (
                    SELECT DISTINCT reaff_sem, CAST(SUBSTRING(reaff_sem FROM 1 FOR 1) AS INTEGER) AS start_num
                    FROM reaffiliation
                    WHERE NOT reaff_delete_ind AND mem_id = %s and reaff_acad_year = %s
                ) AS sorted_sem
                ORDER BY start_num ASC;
                """
            values = [mem_id, acad_year]

            cols = ['label', 'value']
            df = db.querydatafromdatabase(sql, values, cols)
            
            academic_sem = df.to_dict('records')

        else:
            sql = """
                SELECT reaff_sem as label, reaff_sem as value
                FROM (
                    SELECT DISTINCT reaff_sem, CAST(SUBSTRING(reaff_sem FROM 1 FOR 1) AS INTEGER) AS start_num
                    FROM reaffiliation
                    WHERE NOT reaff_delete_ind AND mem_id = %s
                ) AS sorted_sem
                ORDER BY start_num ASC;
                """
            values = [mem_id]

            cols = ['label', 'value']
            df = db.querydatafromdatabase(sql, values, cols)
            
            academic_sem = df.to_dict('records')
            
        return [memtype, status, mem_degree, appbatch, academic_year, academic_sem]
    
#MEMBER PERSONAL INFORMATION
@app.callback(
    [
        Output('member_fn', 'value'),
        Output('member_mn', 'value'),
        Output('member_ln', 'value'),
        Output('member_sf', 'value'),
        Output('member_st_num', 'value'),
        Output('member_bd', 'value'),
        Output('member_degree', 'value'),

        Output('member_cn', 'value'),
        Output('member_emergency', 'value'),
        Output('member_email', 'value'),
        Output('member_up_email','value'),
        Output('member_pres_add', 'value'),
        Output('member_perma_add', 'value'),

        Output('member_year_batch', 'value'),
        Output('mem_appbatch_list', 'value'),
        Output('member_year_standing', 'value'),
        Output('memtype_name', 'value'),
        Output('member_other_org', 'value'),
        Output('status_name','value'),

        Output('member_output_message', 'children')
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('save_btn', 'n_clicks'),
    ],
    [
        State('member_fn', 'value'),
        State('member_mn', 'value'),
        State('member_ln', 'value'),
        State('member_sf', 'value'),
        State('member_st_num', 'value'),
        State('member_bd', 'value'),
        State('member_degree', 'value'),

        State('member_cn', 'value'),
        State('member_emergency', 'value'),
        State('member_email', 'value'),
        State('member_up_email','value'),
        State('member_pres_add', 'value'),
        State('member_perma_add', 'value'),

        State('member_year_batch', 'value'),
        State('mem_appbatch_list', 'value'),
        State('member_year_standing', 'value'),
        State('memtype_name', 'value'),
        State('member_other_org', 'value'),
        State('status_name','value'),
     ],
)
def mem_form_fill_and_submit(
                url_search,
                pathname,
                submit,
                
                fn,
                mn,
                ln,
                sf,
                st_num,
                bd,
                degree,
                
                cn,
                emergency,
                email,
                up_email,
                pres_add,
                perma_add,
                
                batch_year,
                app_batch,
                year_standing,
                memtype,
                other_org,
                status):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    mem_id = query_id.get('id', [None])[0]

    if pathname == '/mem_vieweditinfo':
        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'save_btn' and submit:
                if not(
                    fn and
                    ln and
                    st_num and
                    bd and
                    degree and

                    cn and
                    emergency and
                    email and
                    up_email and
                    pres_add and
                    perma_add and

                    batch_year and
                    app_batch and
                    year_standing and
                    memtype and
                    other_org and
                    status
                ):
                    return [
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                        html.Div("Please fill in all required member information", style={'color': 'red'})
                    ]
                else:
                    sql = """
                        UPDATE member
                        SET
                            mem_fn=%s,
                            mem_mn=%s,
                            mem_ln=%s,
                            mem_sf=%s,
                            mem_st_num=%s,
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
                            appbatch_id=%s
                        WHERE 
                            NOT mem_delete_ind
                            AND mem_id=%s
                    """
                    values = [fn, mn, ln, sf, st_num, bd, 
                              cn, emergency, email, up_email, pres_add, perma_add, 
                              batch_year, year_standing, degree, other_org, status, memtype, app_batch,
                              mem_id]
                    db.modifydatabase(sql, values)

                    return [
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                        html.Div("Member information updated succesfully!", style={'color': 'green'})
                    ]
        
        sql = """
            select
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
                appbatch_id
            from member
            where
                NOT mem_delete_ind AND
                mem_id = %s
            """
            
        values = [mem_id]
        cols = [
            'mem_fn',
            'mem_mn',
            'mem_ln',
            'mem_sf',
            'mem_st_num',
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
            'status_id',
            'memtype_id',
            'appbatch_id'
        ]

        df = db.querydatafromdatabase(sql, values, cols)

        fn = df['mem_fn'][0]
        mn = df['mem_mn'][0]
        ln = df['mem_ln'][0]
        sf = df['mem_sf'][0]
        st_num = df['mem_st_num'][0]
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
        status = df['status_id'][0]
        memtype = df['memtype_id'][0]
        app_batch = df['appbatch_id'][0]

        return [
            fn, mn, ln, sf, st_num, bd, degree,
            cn, emergency, email, upmail, pres_add, perma_add,
            year_batch, app_batch, year_standing, memtype, other_org, status,
            html.Div(style={'style': 'none'})
        ]
    else:
        raise PreventUpdate

#REAFF INFORMATION
@app.callback(
    [
        Output('reaff_edit_gwa', 'value'),

        Output('reaff_edit_date', 'value'),
        Output('reaff_edit_is_paid', 'value'),
        Output('reaff_edit_date_paid', 'value'),

        Output('reaff_edit_choice1', 'value'),
        Output('reaff_edit_choice2', 'value'),
        Output('reaff_edit_choice3', 'value'),
        Output('reaff_edit_choice4','value'),
        Output('reaff_edit_choice5', 'value'),
        Output('reaff_edit_choice6', 'value'),

        Output('edit_assigned_comm','value'),

        Output('reaff_output_message', 'children')
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('save_btn', 'n_clicks'),
        Input('reaff_edit_acad_year', 'value'),
        Input('reaff_edit_sem', 'value'),
    ],
    [
        State('reaff_edit_gwa', 'value'),

        State('reaff_edit_date', 'value'),
        State('reaff_edit_is_paid', 'value'),
        State('reaff_edit_date_paid', 'value'),

        State('reaff_edit_choice1', 'value'),
        State('reaff_edit_choice2', 'value'),
        State('reaff_edit_choice3', 'value'),
        State('reaff_edit_choice4','value'),
        State('reaff_edit_choice5', 'value'),
        State('reaff_edit_choice6', 'value'),

        State('edit_assigned_comm','value'),
     ],
)
def reaff_form_fill_and_submit(
                url_search,
                pathname,
                submit,
                acad_year,
                acad_sem,

                acad_gwa,

                reaff_date,
                is_paid,
                date_paid,

                choice1,
                choice2,
                choice3,
                choice4,
                choice5,
                choice6,
                
                assigned_comm,
                ):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    mem_id = query_id.get('id', [None])[0]

    if pathname == '/mem_vieweditinfo':
        ctx = dash.callback_context
        
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'save_btn' and submit:
                    variable = [choice1, choice2, choice3, choice4, choice5, choice6]

                    seen = set()
                    duplicate = False
                    
                    for comm in variable:
                        if comm in seen:
                            duplicate = True
                            break
                        seen.add(comm)

                    if not(
                        acad_year and
                        acad_sem and
                        acad_gwa and

                        reaff_date and
                        is_paid and

                        choice1 and
                        choice2 and
                        choice3 and
                        choice4 and
                        choice5 and
                        choice6
                    ):
                        return[
                            dash.no_update,
                            dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update,
                            html.Div("Please fill in all required member reaffiliation information.", style={'color': 'red'})
                        ]
                    elif duplicate:
                        return[
                            dash.no_update,
                            dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update,
                            html.Div("Please choose different committees per rank preference", style={'color': 'red'})
                        ]
                    else:
                        sql = """
                            select
                                reaff_id
                            from reaffiliation
                            where 
                                NOT reaff_delete_ind
                                AND mem_id = %s
                                AND reaff_acad_year = %s
                                AND reaff_sem = %s
                            """
                        values = [mem_id, acad_year, acad_sem]
                        df = db.querydatafromdatabase(sql,values)

                        reaff_id = int(df.loc[0,0])

                        sql = """
                            UPDATE reaffiliation
                            SET
                                reaff_date=%s,
                                reaff_sem=%s,
                                reaff_gwa=%s,
                                reaff_acad_year=%s,
                                reaff_choice1=%s,
                                reaff_choice2=%s,
                                reaff_choice3=%s,
                                reaff_choice4=%s,
                                reaff_choice5=%s,
                                reaff_choice6=%s,
                                reaff_assigned_comm=%s,
                                reaff_is_paid=%s,
                                reaff_date_paid=%s
                            WHERE
                                NOT reaff_delete_ind
                                AND reaff_id=%s
                        """
                        values = [reaff_date, acad_sem, acad_gwa, acad_year, choice1, choice2, choice3, choice4, choice5, choice6, assigned_comm, is_paid, date_paid, reaff_id]
                        db.modifydatabase(sql, values)
                        
                        return[
                            dash.no_update,
                            dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
                            dash.no_update,
                            html.Div("Member reaffiliation information updated successfully!", style={'color': 'green'})
                        ]

        if acad_year and acad_sem:
            sql = """
                select
                    reaff_id
                from reaffiliation
                where 
                    NOT reaff_delete_ind
                    AND mem_id = %s
                    AND reaff_acad_year = %s
                    AND reaff_sem = %s
                """
            values = [mem_id, acad_year, acad_sem]
            df = db.querydatafromdatabase(sql,values)
            reaff_id = int(df.loc[0,0])
                
            sql = """
                select
                    reaff_date,
                    reaff_gwa,
                    reaff_is_paid,
                    reaff_date_paid,
                    reaff_choice1,
                    reaff_choice2,
                    reaff_choice3,
                    reaff_choice4,
                    reaff_choice5,
                    reaff_choice6,
                    reaff_assigned_comm
                from reaffiliation
                where 
                    NOT reaff_delete_ind
                    AND reaff_id = %s
            """
            values = [reaff_id]
            cols = [
                'date',
                'gwa',
                'is_paid',
                'date_paid',
                'choice1',
                'choice2',
                'choice3',
                'choice4',
                'choice5',
                'choice6',
                'assigned_comm'
            ]
            df = db.querydatafromdatabase(sql,values,cols)

            date = df['date'][0]
            gwa = df['gwa'][0]
            is_paid = df['is_paid'][0]
            date_paid = df['date_paid'][0]
            choice1 = df['choice1'][0]
            choice2 = df['choice2'][0]
            choice3 = df['choice3'][0]
            choice4 = df['choice4'][0]
            choice5 = df['choice5'][0]
            choice6 = df['choice6'][0]
            assigned_comm = df['assigned_comm'][0]

            return [gwa, date, is_paid, date_paid, choice1, choice2, choice3, choice4, choice5, choice6, assigned_comm, html.Div(style={'disply': 'none'})]
        
        else:
            return [None, None, None, None, None, None, None, None, None, None, None, html.Div(style={'disply': 'none'})]

    else:
        raise PreventUpdate
