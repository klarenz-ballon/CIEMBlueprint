from dash_iconify import DashIconify as di
from dash import html,dash_table
import math
import dash
import pandas as pd
from apps import commonmodule as cm
from apps import dbconnect as db
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc
from app import app

layout=html.Div([
        dcc.Store(id='pref-mem',data=[]),
        cm.navigation,
        cm.top,
    html.Div([
        dbc.Card(
            [dbc.CardHeader([
                dcc.Dropdown(id='graph-selector',options=[
                    {"label":"Reaffiliated Members","value":0},
                    {"label":"New Members","value":1},
                    {"label":"Current Active and Inactive Members","value":5},
                    {"label":"Alumni Added","value":6},
                    {"label":"Committee Performance","value":2},
                    {"label":"Accountabilities","value":3},
                    {"label":"14 White Stripes","value":4}
                    ],searchable=False, value=0,style={'width':'100%'},clearable=False),
                dcc.Dropdown(id='by-grouping',options=[
                    {'label':'by Sem','value':0},
                    {'label':'by Year','value':1}
                    ],value=0,style={'width':'100%'},clearable=False,disabled=False)
            ],class_name='flex'),
            dbc.CardBody("No Graph Loaded",id='report-body')]
        )
    ],className='body')
])
@app.callback(Output('com-table','children'),Input('com-selector','value'),State('com-selector','options'))
def fill_another_table(com,lab):
    label=[x['label'] for x in lab if x['value']==com][0]
    if com==-1:
        print('here')
        sql="""
            SELECT
                p.perf_acad_year,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 1 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com1,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 2 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com2,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 3 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com3,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 4 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com4,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 5 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com5,
                ROUND(COALESCE(AVG(CASE WHEN r.reaff_assigned_comm = 6 THEN COALESCE(p.perf_comm1_score, p.perf_comm2_score) END), 0), 2) as com6
            FROM 
                performance p
            JOIN 
                reaffiliation r ON p.perf_acad_year = r.reaff_acad_year AND p.mem_id = r.mem_id
            GROUP BY 
                p.perf_acad_year;
    """
        cols=['perf_acad_year','1','2','3','4','5','6']   
        labs={'wide_variable_'+str(i['value']-1):i['label'] for i in lab}
        print(labs)
        df=db.querydatafromdatabase(sql,[],cols)
        gf=px.line(x=df['perf_acad_year'],y=[df[str(i)] for i in range(1,7)],title="Average Committee Performances per Year",labels={'variable','Committee'})
        gf.for_each_trace(lambda t:t.update(name=labs[t.name]))
        return [dcc.Graph(figure=gf)]
    sql="SELECT perf_acad_year,ROUND(AVG(perf_eval),2) FROM performance p JOIN reaffiliation r  ON p.perf_acad_year=r.reaff_acad_year AND p.mem_id=r.mem_id WHERE reaff_assigned_comm="+str(com)+" GROUP BY perf_acad_year "
    cols=['acad','avg_eval']
    df=db.querydatafromdatabase(sql,[],cols)
    new_cols=[]
    datetod=datetime.date.today()
    myear=datetod.year
    for i in range(2018,myear+int(datetod.month>7)):
        acad_year=str(i)+'-'+str(i+1)
        if not acad_year in df['acad']:
            new_cols.append({'acad':acad_year,'avg_eval':0})
    if len(new_cols)>0:
        df=df._append(new_cols,ignore_index=True)
    df=df.sort_values(by='acad')
    gf=px.bar(x=df['acad'],y=df['avg_eval'],title=label+" per Acad year")
    gf.update_layout(yaxis=dict(title='# of Members'))
    print('processed')
    return [dcc.Graph(figure=gf)]

#14 WS
@app.callback(Output('ws-table','children'),Input('ws-selector','value'))

def fill_table(year):
        sql="""
            SELECT 
                (SELECT TRIM(CONCAT(mem_fn,' ',mem_ln,' ',mem_sf)) FROM member m WHERE r.mem_id=m.mem_id) as name,
                CAST(AVG(CAST(reaff_gwa AS float)) AS numeric(10,4)) AS avg_gwa,
                CAST((SELECT COALESCE(SUM(headscore_score),0) FROM headship_score hs WHERE hs.mem_id=r.mem_id AND hs.headscore_acad_year=r.reaff_acad_year) as float) as headship,
                CAST(COALESCE((SELECT AVG(perf_eval) FROM performance p where p.mem_id=r.mem_id and p.perf_acad_year=r.reaff_acad_year),0) as float) as performance
            FROM 
                reaffiliation r 
            WHERE 
                reaff_acad_year = %s
            GROUP BY 
                r.reaff_acad_year, r.mem_id;
            """ 
        col=['Name','GWA','Headship Score','Performance Score']
        df=db.querydatafromdatabase(sql,[year],col)
        
        df['GWA'] = df['GWA'].astype(float)
        df['Headship Score'] = df['Headship Score'].astype(float)
        df['Performance Score'] = df['Performance Score'].astype(float)

        df["Score"]=round((40/df['GWA'])+(30*df['Headship Score']/25)+df['Performance Score']/100*30,2)
        df['Ranking']=df['Score'].rank(ascending=False).astype(int)
        df=df[['Ranking','Name','Headship Score','GWA','Performance Score','Score']]
        table = dash_table.DataTable(
            data=df[df['Ranking']<=14].sort_values(by='Ranking').to_dict('records'),
            style_table={'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': '600px',
                    'textOverflow': 'ellipsis'
                },
                style_header={
                    'backgroundColor': '#2E4178',
                    'color': 'white',
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'borderBottom': '2px solid #dee2e6',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#E8EFFF'},
                    {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'}
                ],
                page_action='none',
                style_header_conditional=[
                    {'if': {'column_id': c}, 'textAlign': 'center'} for c in df.columns
                ]
        )
        return [table]
        raise PreventUpdate

@app.callback(
    [
        Output('report-body','children'),
        Output('by-grouping','disabled'),
        Output('by-grouping','value')
    ],
    [   
        Input('graph-selector','value'),
        Input('by-grouping','value')
    ]
)
def generate(graph,sub):
    children='No graphs Selected'
    ttle=''
    
    if graph==4:
        nsql="SELECT DISTINCT reaff_acad_year FROM reaffiliation ORDER BY  reaff_acad_year"
        col=['Year']
        df=db.querydatafromdatabase(nsql,[],col)
        df['semyear']=df['Year']
        out=dcc.Dropdown(options=[{'label':i,'value':i} for i in df['semyear']],value=df['semyear'][0],id='ws-selector',clearable=False)

        return [out,
                html.Br(),
                html.Div(id='ws-table')],True,0
    elif graph==5:
        sql='''SELECT
                    (SELECT COUNT(DISTINCT m.mem_id)
                    FROM member m
                    JOIN reaffiliation r ON m.mem_id = r.mem_id
                    WHERE r.reaff_acad_year = (SELECT MAX(reaff_acad_year) FROM reaffiliation)
                    AND (m.mem_delete_ind IS NULL OR m.mem_delete_ind = FALSE)
                    AND m.status_id = 1) AS active,
                    ((SELECT COUNT(DISTINCT m.mem_id)
                    FROM member m
                    WHERE m.mem_delete_ind IS NULL OR m.mem_delete_ind = FALSE) -
                    (SELECT COUNT(DISTINCT m.mem_id)
                    FROM member m
                    JOIN reaffiliation r ON m.mem_id = r.mem_id
                    WHERE r.reaff_acad_year = (SELECT MAX(reaff_acad_year) FROM reaffiliation)
                        AND (m.mem_delete_ind IS NULL OR m.mem_delete_ind = FALSE)
                        AND m.status_id = 1)) AS inactive;'''
        cols=['Active','Inactive']
        df=db.querydatafromdatabase(sql,[],cols)
        fg=px.pie(values=[df['Active'][0],df['Inactive'][0]],names=cols, title="Active and Inactive Members")
        return [dcc.Graph(figure=fg),html.H5(["Total Current Active Members: ",df['Active'][0]]),html.H5(["Total Current Inactive Members: ",df['Inactive'][0]])],True,1
    
    elif graph==6:
        sql="SELECT EXTRACT(YEAR FROM alum_date_add),count(*) FROM alumni GROUP BY EXTRACT(YEAR FROM alum_date_add) ORDER BY EXTRACT(YEAR FROM alum_date_add)"
        cols=['Year','Count']
        df=db.querydatafromdatabase(sql,[],cols)
        gf=px.bar(x=df['Year'],y=df['Count'],title=ttle)
        gf.update_yaxes(dtick=1)
        gf.update_layout(yaxis=dict(title='# of Members'),xaxis=dict(title='Year Added'))
        return [dcc.Graph(figure=gf),
                html.Br(),
                  html.Br(),
                  html.H6('List of Alumni Added per Year', style={'text-align': 'center'}),
                  
                  dbc.Container(["No Alumni Added to Display"], id="alumadd-table")],True,1
        
        
    elif graph==0:
        mid_sql='''COUNT(DISTINCT r.mem_id) as reaffiliated
                FROM 
                    reaffiliation r
                JOIN 
                    member m ON r.mem_id = m.mem_id'''
        ttle="Reaffiliated Members per "
    elif graph==1:
        mid_sql="COUNT(CASE WHEN reaff_is_new=true THEN 1 END) as reaffiliated FROM reaffiliation r JOIN member m ON r.mem_id = m.mem_id"
        ttle="New Members per "
    elif graph==2:
        nsql="SELECT * FROM committee"
        col=['id','desc','extra']
        df=db.querydatafromdatabase(nsql,[],col)
        df=df._append({'id':-1,'desc':'All Committee','extra':'false'},ignore_index=True)
        print(df)
        out=dcc.Dropdown(options=[
            {
                'label':i['desc'],
                'value':int(i['id'])
                } for _,i in df.sort_values(by='id').iterrows()]
                ,id='com-selector',clearable=False,value=-1)
        return [out,html.Div(id='com-table')],True,1
        
    elif graph==3:
        ttle="Accountabilities per "
        mid_sql="COUNT(CASE WHEN reaff_is_paid THEN 1 END) as paid,COUNT(CASE WHEN NOT reaff_is_paid THEN 1 END) as not_paid FROM reaffiliation r JOIN member m ON r.mem_id = m.mem_id"
    if sub==1:#by Year
        start_sql="SELECT reaff_acad_year,"
        end_sql=" WHERE NOT mem_delete_ind GROUP BY reaff_acad_year ORDER BY reaff_acad_year"
        ttle+="Year"
    else:
        ttle+="Semester"
        start_sql="SELECT CONCAT(reaff_sem,' Sem ',reaff_acad_year) as sem,"
        end_sql=" WHERE NOT mem_delete_ind GROUP BY reaff_acad_year, reaff_sem ORDER BY reaff_acad_year, reaff_sem"
    sql=start_sql+mid_sql+end_sql
    if graph ==0:
        cols=['Year','Count']
        df=db.querydatafromdatabase(sql,[],cols)
        gf=px.bar(x=df['Year'],y=df['Count'],title=ttle)
        gf.update_yaxes(dtick=1)
        gf.update_layout(yaxis=dict(title='# of Members'))
        if sub==1:
            gf.update_layout(xaxis=dict(title='Years'))
        else:
            gf.update_layout(xaxis=dict(title='Sem'))
        children=[dcc.Graph(figure=gf)]
    if graph ==1:
        cols=['Year','Count']
        df=db.querydatafromdatabase(sql,[],cols)
        gf=px.bar(x=df['Year'],y=df['Count'],title=ttle)
        gf.update_yaxes(dtick=1)
        gf.update_layout(yaxis=dict(title='# of Members'))
        if sub==1:
            gf.update_layout(xaxis=dict(title='Years'))
        else:
            gf.update_layout(xaxis=dict(title='Sem'))
        children=[dcc.Graph(figure=gf)]
    if graph==3:
        cols=['Year','paid','notpaid']
        df=db.querydatafromdatabase(sql,[],cols)
        gf=px.line(x=df['Year'],y=[df['paid'],df['notpaid']],title=ttle,labels=[])
        newnames={'wide_variable_0':'Paid Members','wide_variable_1':'Not Paid Members'}
        gf.for_each_trace(lambda t:t.update(name=newnames[t.name]))
        gf.update_yaxes(dtick=1)
        gf.update_layout(yaxis=dict(title='# of Members'))
        
        if sub==1:
            gf.update_layout(xaxis=dict(title='Years'))
        else:
            gf.update_layout(xaxis=dict(title='Sem'))
        children=[dcc.Graph(figure=gf),
                  html.H5(["Total Paid(PHP): ", df['paid'].sum()*150], style={'text-align': 'right'}),
                  html.H5(["Total to be Collected(PHP): ",df['notpaid'].sum()*150], style={'text-align': 'right'}),
                  html.Br(),
                  html.Br(),
                  html.H6('List of Members with Existing Accountabilities', style={'text-align': 'center'}),
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
                                width=6,
                            ),
                            dbc.Col(
                                dbc.FormFloating(
                                    [
                                        dbc.Select(
                                            id="reaff-sem",
                                            options=[
                                                {'label': "1st Semester", 'value': "1st"},
                                                {'label': "2nd Semester", 'value': "2nd"}
                                            ],
                                            placeholder="Semester",
                                        ),
                                        dbc.Label("Semester", style={"font-size": "14px"}),
                                    ]
                                ),
                                width=3,
                                
                            ),
                            dbc.Col(
                                dbc.FormFloating(
                                    [
                                        dbc.Input(type="text", placeholder="Enter Academic Year", id="reaff-acad-year"),
                                        dbc.Label("Academic Year", style={"font-size": "14px"}),
                                    ]
                                ),
                                width=3,
                                
                            ),
                            
                        ],
                        class_name='d-flex align-items-center justify-content-end',
                        style={"width": "100%"}
                    ),
                ], class_name='py-3'),
                  dbc.Container(["No Accountabilities to Display"], id="account-table")
                  ]
    
    return children,False,dash.no_update


@app.callback(
    Output('account-table', 'children'),
    [Input('graph-selector', 'value'),
     Input('mem-name', 'value'),
     Input('reaff-sem', 'value'),
     Input('reaff-acad-year', 'value')]
)
def account_pop(graph, mem_name, reaff_sem, reaff_acad_year):
    if graph == 3:
        sql = """ 
            SELECT
                CONCAT(m.mem_fn, ' ', m.mem_mn, ' ', m.mem_ln, ' ', m.mem_sf) AS full_name,
                r.reaff_acad_year,
                r.reaff_sem,
                CASE WHEN r.reaff_is_paid = False THEN 150 ELSE 0 END AS reaff_is_paid_number
            FROM
                member m
            JOIN
                reaffiliation r ON m.mem_id = r.mem_id
            WHERE
                r.reaff_is_paid = False
        """
        values = []

        if mem_name:
            sql += " AND CONCAT(m.mem_fn, ' ', m.mem_mn, ' ', m.mem_ln, ' ', m.mem_sf) ILIKE %s"
            values.append(f"%{mem_name}%")
        
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

        sql += " ORDER BY r.reaff_acad_year ASC"

        # Assuming db.querydatafromdatabase executes the query and fetches data
        cols=['Name', 'Academic Year', 'Semester', 'Unpaid (PHP)']
        df = db.querydatafromdatabase(sql, values, cols )

        if not df.empty:
            table = dash_table.DataTable(
                id='account-data-table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': '600px',
                    'textOverflow': 'ellipsis'
                },
                style_header={
                    'backgroundColor': '#2E4178',
                    'color': 'white',
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'borderBottom': '2px solid #dee2e6',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#E8EFFF'},
                    {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'}
                ],
                page_action='none',
                style_header_conditional=[
                    {'if': {'column_id': c}, 'textAlign': 'center'} for c in df.columns
                ]
            )
            return [table]
        return ["No Accountabilities to Display"]
    raise PreventUpdate

@app.callback(
    Output('alumadd-table', 'children'),
    Input('graph-selector', 'value')
)
def alumadd_pop(graph):
    if graph == 6:
        sql = """ 
            SELECT
                CONCAT(a.alum_fn, ' ', a.alum_mn, ' ', a.alum_ln, ' ', a.alum_sf) AS full_name,
                EXTRACT(YEAR FROM a.alum_date_add) AS year_added
            FROM
                alumni a
            WHERE
                a.alum_delete_ind = False
        """
        values = []

        sql += " ORDER BY a.alum_date_add ASC"

        # Assuming db.querydatafromdatabase executes the query and fetches data
        cols=['Name', 'Year Added']
        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            table = dash_table.DataTable(
                id='alumadded-data-table',
                columns=[{'name': i, 'id': i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'padding': '5px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'maxWidth': '600px',
                    'textOverflow': 'ellipsis'
                },
                style_header={
                    'backgroundColor': '#2E4178',
                    'color': 'white',
                    'textAlign': 'center',
                    'font_family': 'Arial, sans-serif',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'borderBottom': '2px solid #dee2e6',
                    'whiteSpace': 'normal',
                    'height': 'auto'
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#E8EFFF'},
                    {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'}
                ],
                page_action='none',
                style_header_conditional=[
                    {'if': {'column_id': c}, 'textAlign': 'center'} for c in df.columns
                ]
            )
            return [table]
        return ["No Alumni Added to Display"]
    
    raise PreventUpdate
