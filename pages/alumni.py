from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
from apps import dbconnect as db
from app import app
import dash_table



layout = html.Div([
    cm.navigation,
    cm.top,
    html.Div([ 
        dbc.Card(
            [
                dbc.Container([
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.FormFloating([
                                    dbc.Input(type="text", placeholder="Enter Name", id="alum-name"),
                                    dbc.Label("Search Name", style={"font-size": "14px"}),
                                ]),
                                width=5,
                            ),
                            dbc.Col(
                                dbc.FormFloating([
                                    dbc.Input(type="text", placeholder="Specialization", id="prof-filter"),
                                    dbc.Label("Filter by Specialization", style={"font-size": "14px"}),
                                ]),
                                width=5,
                            ),
                            dbc.Col(
                                dbc.Button("Add Alumni", 
                                    id="add_alum_btn", 
                                    color="primary", 
                                    href = '/add_alumni?mode=add', 
                                    style={"height": "100%", "display": "flex", "align-items": "center", "justify-content": "center", "padding": "0 15px", 'backgroundColor': '#5474D5'}),
                                width=2,
                            ),
                        ],
                        className="g-7",
                        style={"width": "100%"},
                        justify='between'
                    ),
                ], class_name='flex '),

                dbc.Container(["No Alumni to Display"], id="alum-table", class_name='table-wrapper'),
                dbc.Container(id="alumrow-count", class_name='table-wrapper p-3')
            ],
            class_name="custom-card"
        )
    ], className='body')
])


# Callback to update alumni table based on inputs
@app.callback(
    Output("alum-table", "children"),
    Output('alumrow-count', 'children'),
    [Input("url", "pathname"), 
     Input("prof-filter", "value"), 
     Input("alum-name", "value")]
)
def show_alumni(pathname, filter, name):
    if pathname == "/alumni":
        sql = """
            SELECT 
                CONCAT(alumni.alum_fn, ' ', COALESCE(alumni.alum_mn, ''), ' ', alumni.alum_ln, ' ', COALESCE(alumni.alum_sf, '')) AS "Full Name",
                alumni.alum_st_num, alumni.alum_cn, alumni.alum_email,
                appbatch.appbatch_name, alumni.alum_year_batch, alumni.alum_year_grad,
                degree.degree_name AS "Degree",
                specialization.spec_name AS "Specialization",
                alumni.alum_ID
            FROM alumni
            LEFT JOIN degree ON alumni.degree_id = degree.degree_id
            LEFT JOIN specialization ON alumni.spec_id = specialization.spec_id
            LEFT JOIN appbatch ON alumni.appbatch_id=appbatch.appbatch_id
            WHERE TRUE
            """
        values = []
        cols = [ "Full Name", 
                "Student Number", "Contact Number", "Email",
                "App Batch", "Batch year", "Year Graduated", "Degree", 
                "Specialization", "Action"]

        if name:
            sql += """ AND CONCAT(alumni.alum_fn, ' ', COALESCE(alumni.alum_mn, ''), ' ', alumni.alum_ln, ' ', COALESCE(alumni.alum_sf, '')) ILIKE %s """
            values.append(f"%{name}%")

        if filter:
            sql += """ AND specialization.spec_name ILIKE %s """
            values.append(f"{filter}%")

        # Fetch data from database using the dbconnect module
        df = db.querydatafromdatabase(sql, tuple(values), cols)


        if not df.empty:
            df['Action'] = df['Action'].apply(lambda x: f'<div style="text-align: center;"><a href="/add_alumni?mode=edit&id={x}"><button class="btn btn-primary btn-sm" style="font-size: 12px; background-color: #5474D5;">Edit</button></a>')
            # Build DataTable with data
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Action' else {'name': i, 'id': i} for i in df.columns],
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
                    'width': 'auto',  # Adjust width dynamically
                    'maxWidth': '600px',  # Maximum column width
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
                page_action='none',
                style_table={'height': '400%', 'overflowY': 'auto'}
            )
            alumrow_count = f"No. of Alumni: {len(df)}"
            return table, alumrow_count
        return html.Div("No Alumni to Display", className="no-data-message")

    raise PreventUpdate
