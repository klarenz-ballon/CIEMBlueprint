from dash_iconify import DashIconify as di
from dash import html
from apps import commonmodule as cm
from apps import dbconnect as db
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_bootstrap_components as dbc
from app import app


layout=html.Div([
    
        cm.navigation,
        cm.top,
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader([
                    html.H3("Hello, "), 
                    html.H3(" User", id='session-user')
                ], className='flex',
                               style={  'background-color': '#2E4178',
                                        'color': 'white',  # White text for header
                                        'font-size': '24px',
                                        'font-weight': 'bold'}),
                dbc.CardBody([
                    dbc.Container([
                        dbc.Card([
                            dbc.CardHeader("Members", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem', 'background-color': '#5676D9'}),
                            dbc.CardBody("Total here", id='total-mem-home'),
                            dbc.CardFooter(dbc.NavLink("Check Members>", href="/members"), style={'background-color': '#E8EDF7'})
                        ]),
                        dbc.Card([
                            dbc.CardHeader("Alumni", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem', 'background-color': '#5676D9'}),
                            dbc.CardBody("Total here", id='total-alum-home'),
                            dbc.CardFooter(dbc.NavLink("Check Alumni>", href="/alumni"), style={'background-color': '#E8EDF7'})
                        ]),
                        dbc.Card([
                            dbc.CardHeader("Reports", style={'color': 'white', 'font-weight': 'bold', 'font-size': '1.5rem', 'background-color': '#5676D9'}),
                            dbc.CardBody("Total here", id='home-user'),
                            dbc.CardFooter(dbc.NavLink("Check Full Reports>", href="/view-reports"), style={'background-color': '#E8EDF7'})
                        ]),
                    ], className='flex homeshow')
                ])
            ]),
            dbc.Card([
                html.Video(
                    src="/assets/home_vid.mp4",
                    autoPlay=True,
                    loop=True,
                    muted=True,
                    style={'width': '100%'}
                )
            ]),
            dbc.Card([
                dbc.CardBody([
                    
                html.H2("One Circle, One Family",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"3rem",
                    "margin-top": "0",
                    "margin-bottom": "0",
                    "color": "#273250",
                    "font-weight":"bolder"
                    }
                    ),
            html.H2("Expanding the Circle Since 1976",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.5em",
                    "margin-top": "0",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            dbc.Container([
            dbc.Carousel(
                    items=[
                        {"key": "1", "src": "/static/c1.jpg"},
                        {"key": "2", "src": "/static/c2.jpg"},
                        {"key": "3", "src": "/static/c3.jpg"},
                        {"key": "4", "src": "/static/c4.jpg"},
                        {"key": "5", "src": "/static/c5.jpg"},
                        {"key": "6", "src": "/static/c6.jpg"},
                        {"key": "7", "src": "/static/c7.jpg"},
                    ],
                    controls=False,
                    indicators=False,
                    interval=1000,
                    ride="carousel",
                    style={'aspect-ratio':'16/9','height':'450px','overflow-y':'hidden'},
                ),
            dbc.Container([
                html.H2("About UP CIEM",
                    style={
                    "text-align": "left",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.3em",
                    "margin-top": "0.5em",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            html.H4("The University of the Philippines Circle of Industrial Engineering Majors (UP CIEM) was established on November 23, 1976 by a group of students from the Department of Industrial Engineering and Operations Research, College of Engineering at the University of the Philippines, Diliman. Over the years, UP CIEM has grown from a fledging organization to a force to be reckoned with, not only in academics but in sports, social activities, and leadership as well. The business of UP CIEM never falls short of the foundations of Industrial Engineering – effectiveness, efficiency, and productivity. UP CIEM is a duly recognized college-wide, socio-academic organization. UP CIEM consistently makes its mark through rendering service to the college, the university, and the country by upholding its core values: academic excellence, leadership in service, and social relevance through numerous projects that cater to the needs of Industrial Engineering students. More than being an organization, UP CIEM continues to be the family of camaraderie and trust for the IE student body and the sanctuary of excellent Industrial Engineers for the nation’s future.",
                    style={
                    "font-family": "Arial",
                    "font-weight":"normal",
                    "font-size":"1.25em",
                    "text-align":"justify",
                    "margin":"0"}
                    ),]      
            ),
            ], class_name='flex')
            ])
            ,
            dbc.CardFooter(
                [
                    dbc.Button([di(icon='mingcute:facebook-line',inline=True),dbc.Label("Facebook Page",style={'padding-left':'0.5em'})],href="https://www.facebook.com/upciem",external_link=True),
                    dbc.Button([di(icon='bi:instagram',inline=True),dbc.Label("Instagram",style={'padding-left':'0.5em'})],href="https://www.instagram.com/upciem/",external_link=True),
                    dbc.Button([di(icon='iconoir:twitter',inline=True),dbc.Label("Twitter",style={'padding-left':'0.5em'})],href="https://twitter.com/upciem",external_link=True),
                    dbc.Button([di(icon='lucide:linkedin',inline=True),dbc.Label("LinkedIn",style={'padding-left':'0.5em'})],href="https://ph.linkedin.com/company/upciem1976",external_link=True), 
                ]
                ,style={'display':'flex','justify-content':'space-evenly'}
            )
            ])
            ], 
                className="body"),
    ],className='flex body-container')
])


@app.callback(
    [
        Output('total-mem-home','children'),
        Output('total-alum-home','children'),
        Output('home-user','children'),
        Output('session-user','children')
    ],
    Input('url','pathname'),
    State('auth','data')
)
def total(pathname,data):
    #childrens to be called back
    memchildren=[]
    alumchildren=[]
    profchildren=[]
    if pathname=="/home":
        #This is for the members
        sql="SELECT COUNT(*) FROM member WHERE mem_delete_ind is NULL or mem_delete_ind=False"
        cols=['count']
        df=db.querydatafromdatabase(sql,[],cols)
        #will always return some count but can be 0
        memchildren+=[html.H1(df['count'][0])]
        memchildren+=[html.P("Total Members in the Database")]
        #info for the alumni
        sql="SELECT COUNT(*) FROM alumni"
        cols=['count']
        df=db.querydatafromdatabase(sql,[],cols)
        alumchildren+=[html.H1(df['count'][0])]
        alumchildren+=[html.P("Total Alumni in the Database")]
        
        sql = '''SELECT
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
              AND m.status_id = 1)) AS inactive'''

        cols = ['active', 'inactive']
        df = db.querydatafromdatabase(sql, [], cols)

        # Assuming memchildren, alumchildren, profchildren, and data['acc'] are defined elsewhere
        profchildren += [
            html.H3(['Active Members: ', df['active'][0]]),
            html.H3(['Inactive Members: ', df['inactive'][0]])
        ]

        return memchildren, alumchildren, profchildren, data['acc']
    raise PreventUpdate
