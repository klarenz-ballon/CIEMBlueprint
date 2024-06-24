import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import dash_table
from app import app
from apps import commonmodule as cm
from apps import dbconnect as db
import pandas as pd

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
                                dbc.FormFloating(
                                    [
                                        dbc.Input(type="text", placeholder="Enter Name", id="mem-name"),
                                        dbc.Label("Search Name"),
                                    ]
                                ),
                                width=6,
                            ),
                        ],
                        className="g-3",
                        style={"width": "100%"}
                    ),
                ], class_name='py-3'),

                dbc.Container(["No Members to Display"], id="comm-table", class_name='table-wrapper p-3')
            ],
            class_name="custom-card"
        )
    ], className='body')
])

@app.callback(
    Output('comm-table', 'children'),
    [Input('url', 'pathname'),
     Input('mem-name', 'value'),
    # Input('filter-select', 'value'),
     #Input('prof-filter', 'value')
     ]
)
def mem_pop(pathname, mem_name):
    if pathname == "/updatecomm":
        sql = """ 
            SELECT 
                person.valid_id,
                CONCAT(first_name, ' ', middle_name, ' ', last_name, ' ', suffix) AS full_name,
                membership_type,
                app_batch
            FROM person 
            LEFT JOIN upciem_member ON person.valid_id = upciem_member.valid_id 
            LEFT JOIN affiliation ON person.valid_id = affiliation.valid_id 
            WHERE (upciem_member_id IS NOT NULL AND upciem_member_delete IS NULL OR upciem_member_delete = FALSE)
        """
        values = []
        if mem_name:
            sql += " AND CONCAT(first_name, ' ', middle_name, ' ', last_name, ' ', suffix) ILIKE %s"
            values.append(f"%{mem_name}%")

        print(sql, mem_name)
        cols = ["Select Committee", "Name", "Membership", "App Batch"]
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            df['Select Committee'] = df['Select Committee'].apply(lambda x: f'<a href="/add_alumni?mode=toalum&id={x}"><button class="btn btn-primary btn-sm">Committee</button></a>')
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Select Committee' else {'name': i, 'id': i} for i in df.columns],
                markdown_options={'html': True},
                style_cell={
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px',
                    'color': '#000000',
                    'height': '40px',
                    'padding': '10px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'maxWidth': 0
                },
                style_header={
                    'background-color': '#000097',  # Blue background for header
                    'color': 'white',  # White text for header
                    'text-align': 'center',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '16px',
                    'font-weight': 'bold',
                    'border-bottom': '2px solid #dee2e6',  # Border for separation
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8f9fa'  # Light grey for odd rows
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
                style_table={'height': '80%', 'overflow': 'auto'}
            )
            return [table]
        return ["No Members to Display"]
    raise PreventUpdate

