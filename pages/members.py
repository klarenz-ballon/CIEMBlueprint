import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash import dash_table
from app import app
from apps import commonmodule as cm
from apps import dbconnect as db
import pandas as pd
from datetime import datetime

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
                                        dbc.Label("Search Name", style={"font-size":"14px"}),
                                    ]
                                ),
                                width=4,
                                style={'height': '60px'}  # Apply height style here
                            ),
                            dbc.Col(
                                dbc.FormFloating(
                                    [
                                        dbc.Input(type="text", placeholder="Semester", id="reaff-sem"),
                                        dbc.Label("Semester", style={"font-size": "14px"}),
                                    ]
                                ),
                                width=2,
                                style={'height': '60px'}  # Apply height and alignment style here
                            ),
                            dbc.Col(
                                dbc.FormFloating(
                                    [
                                        dbc.Input(type="text", placeholder="Enter Academic Year", id="reaff-acad-year"),
                                        dbc.Label("Academic Year", style={"font-size": "14px"}),
                                    ]
                                ),
                                width=2,
                                style={'height': '60px'}  # Apply height style here
                            ),
                            dbc.Col(
                                [
                                    dbc.Label("Filter by: ", style={"padding-right": "1em", "font-size": "14px"}),
                                    dbc.Select(
                                        id="filter-select",
                                        options=[
                                            {"label": "Member Type", "value": "memtype_name"},
                                            {"label": "Year Standing", "value": "mem_year_standing"},
                                            {"label": "App Batch", "value": "appbatch_name"},
                                            {"label": "Status", "value": "status_name"},
                                        ],
                                    ),
                                    dbc.Input(type="text", placeholder="Filter", id="prof-filter", style={"font-size":"14px"}),
                                ],
                                width=4,
                                style={'height': '60px', 'display': 'flex', 'align-items': 'center'}  # Apply height and alignment style here
                            ),
                        ],
                        className="g-3",
                        style={"width": "100%"}
                    ),
                ], class_name='py-3'),

                dbc.Container(["No Members to Display"], id="mem-table", class_name='table-wrapper p-3'),
                dbc.Container(id="row-count", class_name='table-wrapper p-3')
            ],
            class_name="custom-card", 
        )
    ], className='body',)
])

@app.callback(
    Output('reaff-sem', 'value'),
    Output('reaff-acad-year', 'value'),
    Input('url', 'pathname')
)
def set_default_filters(pathname):
    if pathname == "/members":
        current_date = datetime.now()
        current_year = current_date.year
        if current_date.month >= 8:
            semester = "1st"
            academic_year = f"{current_year}-{current_year + 1}"
        else:
            semester = "2nd"
            academic_year = f"{current_year - 1}-{current_year}"
        return semester, academic_year
    raise PreventUpdate

@app.callback(
    Output('mem-table', 'children'),
    Output('row-count', 'children'),
    Input('url', 'pathname'),
    Input('mem-name', 'value'),
    Input('filter-select', 'value'),
    Input('prof-filter', 'value'),
    Input('reaff-sem', 'value'),
    Input('reaff-acad-year', 'value')
)
def mem_pop(pathname, mem_name, filter_select, prof_filter, reaff_sem, reaff_acad_year):
    if pathname == "/members":
        sql = """ 
            SELECT 
                CONCAT(m.mem_fn,' ', m.mem_mn,' ', m.mem_ln,' ', m.mem_sf) AS full_name,
                m.mem_st_num,
                m.mem_year_standing,
                t.memtype_name,
                a.appbatch_name,
                s.status_name,
                m.mem_id,
                m.mem_id
            FROM member m
            JOIN memtype t ON m.memtype_id = t.memtype_id
            JOIN status s ON m.status_id = s.status_id
            JOIN appbatch a ON m.appbatch_id = a.appbatch_id
            LEFT JOIN reaffiliation r ON m.mem_id = r.mem_id
            WHERE (m.mem_delete_ind IS NULL OR m.mem_delete_ind = FALSE)
        """
        values = []
        if mem_name:
            sql += " AND CONCAT(m.mem_fn, ' ', m.mem_mn, ' ', m.mem_ln, ' ', m.mem_sf) ILIKE %s"
            values.append(f"%{mem_name}%")

        if filter_select and prof_filter:
            if filter_select == "mem_year_standing":
                sql += " AND m.mem_year_standing = %s"
                values.append(prof_filter)
            else:
                sql += f" AND {filter_select} ILIKE %s"
                values.append(f"%{prof_filter}%")
        
        if reaff_sem:
            sql += " AND r.reaff_sem = %s"
            values.append(reaff_sem)
        
        if reaff_acad_year:
            # Check if the input is in the format YYYY-YYYY
            if '-' in reaff_acad_year:
                start_year, end_year = reaff_acad_year.split('-')
                sql += " AND (LEFT(r.reaff_acad_year, 4) = %s OR RIGHT(r.reaff_acad_year, 4) = %s)"
                values.extend([start_year.strip(), end_year.strip()])
            else:
                # Assume single year input (e.g., 2018)
                sql += " AND (LEFT(r.reaff_acad_year, 4) = %s OR RIGHT(r.reaff_acad_year, 4) = %s)"
                values.extend([reaff_acad_year.strip(), reaff_acad_year.strip()])

        print("Final SQL Query:", sql)
        print("Values for SQL Query:", values)
        
        cols = ["Name", "Student Number", "Year Standing", "Membership Type", "App Batch", "Status", "Member Info", "Graduated?"]
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            df['Graduated?'] = df['Graduated?'].apply(lambda x: f'<div style="text-align: center;"><a href="/add_alumni?mode=move&id={x}"><button class="btn btn-primary btn-sm" style="font-size: 12px; background-color: #5474D5;">Move to Alumni</button></a>')
            df['Member Info'] = df['Member Info'].apply(lambda x: f'<div style="text-align: center;"><a href="/mem_vieweditinfo?id={x}"><button class="btn btn-primary btn-sm" style="font-size: 12px; background-color: #5474D5;">View or Modify</button></a>')
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i in ['Graduated?', 'Member Info'] else {'name': i, 'id': i} for i in df.columns],
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
            row_count = f"No. of Reaffiliated Members: {len(df)}"
            return [table], row_count
        return ["No Members to Display"], "Total Rows: 0"
    raise PreventUpdate
