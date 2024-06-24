import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import datetime
from app import app
from apps import commonmodule as cm
from apps import dbconnect as db
from dash_iconify import DashIconify as di
from apps.dbconnect import get_latest_alum_id
from urllib.parse import urlparse, parse_qs

# Generate a list of years for the dropdown
years = list(range(1908, 2099))
# Get the current year
current_year = datetime.now().year

# Define the form layout
add_alumni_form = dbc.Form(
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
                    dbc.Input(type="text", id='alum_fn', placeholder = "Enter First Name", value='', disabled=False),
                    width=4,
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
                    dbc.Input(type="text", id='alum_mn', placeholder = "Enter Middle Name", disabled=False),
                    width=4,
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
                    dbc.Input(type="text", id='alum_ln', placeholder = "Enter Surname", disabled=False),
                    width=4,
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
                    dbc.Input(type="text", id='alum_sf', disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Student Number ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='alum_st_num', placeholder="20XXXXXXX", maxLength=9, disabled=False),
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
                    dbc.Input(type="text", id='alum_cn',
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
                    dbc.Input(type="email", id='alum_email', placeholder = "example@gmail.com", disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.H5(html.B('Past Student Information')),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "App Batch ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dcc.Dropdown(id='appbatch_id', placeholder = "Select App Batch", clearable=False,searchable=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Batch Year ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(id='alum_year_batch',maxLength=4, placeholder="Enter a year", disabled=False),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Year Graduated ",
                        html.Span("*", style={"color": "#F8B237"})
                    ],
                    width=3),
                dbc.Col(
                    dbc.Input(type="text", id='alum_year_grad', maxLength=4, placeholder="Enter a year", disabled=False),
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
                        id='alumdegree_id',
                        placeholder="Select Degree",
                    ),
                    width=4,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.H5(html.B('Specialization')),
        dbc.Row(
            [
                html.P('Select the field of specialization of the Alumni in their career after graduating'),
                dbc.Col(
                    dcc.Dropdown(
                        id='spec_id',
                        placeholder="Select Specialization",
                        multi=False
                    ),
                    width=7,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
        html.Br(),
        dbc.Button('Submit', id='alumsubmit_button', style={'backgroundColor': '#5474D5'}),
        html.Div(id='alumoutput-message'),  #_For displaying output messages
        html.Br(),
        html.Br(),
    ]
)

# Degree dropdown
@app.callback(
    Output('alumdegree_id', 'options'),
    Input('url', 'pathname')
)
def populate_alumdegree_dropdown(pathname):
    # Check if the pathname matches if necessary
    if pathname == '/add_alumni':
        sql = """
        SELECT degree_name as label, degree_id as value
        FROM Degree
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        alumdegree = df.to_dict('records')
        return alumdegree
    else:
        raise PreventUpdate

# Specialization dropdown
@app.callback(
    Output('spec_id', 'options'),
    Input('url', 'pathname')
)
def populate_specialization_dropdown(pathname):

    # Check if the pathname matches if necessary
    if pathname == '/add_alumni':
        sql = """
        SELECT spec_name as label, spec_id as value
        FROM specialization
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(sql, values, cols)
        specialization_name = df.to_dict('records')
        return specialization_name
    else:
        raise PreventUpdate
#appbatch dropdown

# Callback to fill the alumni form
@app.callback(
        Output('appbatch_id','options'),
        Input('url','pathname')
)
def pop_batch(pathname):
    if pathname=='/add_alumni':
        sql='SELECT appbatch_id,appbatch_name FROM appbatch'
        cols=['value','label']
        df=db.querydatafromdatabase(sql,[],cols)
        print(df)
        return df[['label','value']].to_dict('records')
    raise PreventUpdate
@app.callback(
    [
        Output('alumoutput-message', 'children'),
        Output('alum_fn', 'value'),
        Output('alum_mn', 'value'),
        Output('alum_ln', 'value'),
        Output('alum_sf', 'value'),
        Output('alum_st_num', 'value'),
        Output('alum_cn', 'value'),
        Output('alum_email', 'value'),
        Output('appbatch_id', 'value'),
        Output('alum_year_batch', 'value'),
        Output('alum_year_grad', 'value'),
        Output('alumdegree_id', 'value'),
        Output('spec_id', 'value'),
        Output('alumsubmit_button', 'n_clicks') 
    ],
    [
        Input('url', 'search'),
        Input('url', 'pathname'),
        Input('alumsubmit_button', 'n_clicks'),
    ],
    [   
        State('alum_fn', 'value'),
        State('alum_mn', 'value'),
        State('alum_ln', 'value'),
        State('alum_sf', 'value'),
        State('alum_st_num', 'value'),
        State('alum_cn', 'value'),
        State('alum_email', 'value'),
        State('appbatch_id', 'value'),
        State('alum_year_batch', 'value'),
        State('alum_year_grad', 'value'),
        State('alumdegree_id', 'value'),
        State('spec_id', 'value')
    ]
)


def fill_form(url_search, pathname, submit, alum_fn, alum_mn, alum_ln, alum_sf, alum_st_num, alum_cn, alum_email, appbatch_id, alum_year_batch, alum_year_grad, alumdegree_id, spec_id):
    parsed = urlparse(url_search)
    query_id = parse_qs(parsed.query)
    identity = query_id.get('id', [None])[0]
    mode = query_id.get('mode', [None])[0]

    if pathname == '/add_alumni':
        ctx = dash.callback_context
        if ctx.triggered:
            nclicks = ctx.triggered[0]['prop_id'].split('.')[0]
            if submit >0:
                if not(
                    alum_fn,
                    alum_ln,
                    alum_st_num,
                    alum_cn,
                    alum_email,
                    appbatch_id,
                    alum_year_batch,
                    alum_year_grad,
                    alumdegree_id
                ):
                    return html.Div("Please fill in all required fields", style={'color': 'red'}), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,0
                else:
                    sql = """
                        INSERT INTO alumni(
                                alum_fn, 
                                alum_mn, 
                                alum_ln, 
                                alum_sf, 
                                alum_st_num, 
                                alum_cn, 
                                alum_email, 
                                appbatch_id, 
                                alum_year_batch, 
                                alum_year_grad, 
                                degree_id,
                                spec_id        
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    values = [alum_fn, alum_mn, alum_ln, alum_sf, alum_st_num, alum_cn, alum_email, appbatch_id, alum_year_batch, alum_year_grad, alumdegree_id, spec_id]
                    db.modifydatabase(sql, values)
                    
                    sql = """
                        UPDATE member
                        SET
                            mem_delete_ind=%s
                        WHERE
                            mem_id=%s
                    """
                    values = [True, identity]
                    db.modifydatabase(sql, values)
                    return html.Div("Member successfully moved to Alumni", style={'color': 'green'}), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,0

            if nclicks == 'alumsubmit_button' and submit and mode == 'edit':
                if not(
                    alum_fn,
                    alum_ln,
                    alum_st_num,
                    alum_cn,
                    alum_email,
                    appbatch_id,
                    alum_year_batch,
                    alum_year_grad,
                    alumdegree_id
                ):
                    return html.Div("Please fill in all required fields", style={'color': 'red'}), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,0
                else:
                    sql = """
                        UPDATE alumni
                        SET
                            alum_fn=%s, 
                            alum_mn=%s, 
                            alum_ln=%s, 
                            alum_sf=%s, 
                            alum_st_num=%s, 
                            alum_cn=%s, 
                            alum_email=%s, 
                            appbatch_id=%s, 
                            alum_year_batch=%s, 
                            alum_year_grad=%s, 
                            degree_id=%s,
                            spec_id=%s        
                        WHERE
                            NOT alum_delete_ind
                            AND alum_id=%s
                    """
                    values = [alum_fn, alum_mn, alum_ln, alum_sf, alum_st_num, alum_cn, alum_email, appbatch_id, alum_year_batch, alum_year_grad, alumdegree_id, spec_id, identity]
                    db.modifydatabase(sql, values)

                    return html.Div("Alumni Information Updated successfully!", style={'color': 'green'}), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,0

        elif mode == 'move':
            sql = """
                select
                    mem_fn,
                    mem_mn,
                    mem_ln,
                    mem_sf,
                    mem_st_num,
                    mem_cn,
                    mem_email,
                    appbatch_id,
                    mem_year_batch,
                    degree_id
                from member
                where
                    NOT mem_delete_ind
                    AND mem_id = %s
            """
            values = [identity]
            cols = [
                'fn',
                'mn',
                'ln',
                'sf',
                'st_num',
                'cn',
                'email',
                'app_batch',
                'year_batch',
                'degree_id',
            ]

            df = db.querydatafromdatabase(sql, values, cols)

            fn = df['fn'][0]
            mn = df['mn'][0]
            ln = df['ln'][0]
            sf = df['sf'][0]
            st_num = df['st_num'][0]
            cn = df['cn'][0]
            email = df['email'][0]
            app_batch = df['app_batch'][0]
            year_batch = df['year_batch'][0]
            degree = df['degree_id'][0]

            return html.Div(style={'disply': 'none'}), fn, mn, ln, sf, st_num, cn, email, app_batch, year_batch, dash.no_update, degree, dash.no_update,0

        elif mode == 'edit':
            sql = """
                select
                    alum_fn,
                    alum_mn,
                    alum_ln,
                    alum_sf,
                    alum_st_num,
                    alum_cn,
                    alum_email,
                    appbatch_id,
                    alum_year_batch,
                    alum_year_grad,
                    degree_id,
                    spec_id
                from alumni 
                where 
                    NOT alum_delete_ind
                    AND alum_id = %s
            """
            values = [identity]
            cols = [
                'fn',
                'mn',
                'ln',
                'sf',
                'st_num',
                'cn',
                'email',
                'app_batch',
                'year_batch',
                'year_grad',
                'degree_id',
                'spec_id'
            ]

            df = db.querydatafromdatabase(sql, values, cols)
            print(df)
            fn = df['fn'][0]
            mn = df['mn'][0]
            ln = df['ln'][0]
            sf = df['sf'][0]
            st_num = df['st_num'][0]
            cn = df['cn'][0]
            email = df['email'][0]
            app_batch = df['app_batch'][0]
            year_batch = df['year_batch'][0]
            year_grad = df['year_grad'][0]
            degree = df['degree_id'][0]
            spec = df['spec_id'][0]

            return html.Div(style={'disply': 'none'}), fn, mn, ln, sf, st_num, cn, email, app_batch, year_batch, year_grad, degree, spec,0
        else:
            return html.Div(style={'disply': 'none'}), dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,0
    raise PreventUpdate

layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader("ALUMNI FORM", className='flex', 
                               style={  'background-color': '#2E4178',
                                        'color': 'white',  # White text for header
                                        'font-size': '24px',
                                        'font-weight': 'bold'}),
                dbc.CardBody([
                    dbc.Container(
                        [
                            add_alumni_form,
                        ]
                    )
                ]),
            ])
        ])
    ], className='body')
])
