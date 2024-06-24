import dash
from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm

# Modal for displaying password change result
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4("Modal Header", style={"font-weight": "bold"}), id='modal-header'),
                dbc.ModalBody(id='modal-body'),
                dbc.ModalFooter(
                    dbc.Button("Proceed", id="close-modal", className="ml-auto", href="/home", external_link=True)
                ),
            ],
            id="modal",
            centered=True,
            size="md",  # Adjust the size here (sm, md, lg)
        ),
    ]
)


# Form for changing password
newpass_form = dbc.Form(
    [
        html.Br(),
        dbc.Row(
            [
                dbc.Label(
                    [
                        "Current Password: ",
                        html.Span("*", style={"color": "#F8B237"}),
                    ],
                    width=5,
                ),
                dbc.Col(
                    dbc.Input(
                        type="password",
                        id="cpw",
                        value="",
                        disabled=False,
                        placeholder="Type Current Password",
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
                        "New Password: ",
                        html.Span("*", style={"color": "#F8B237"}),
                    ],
                    width=5,
                ),
                dbc.Col(
                    dbc.Input(
                        type="password",
                        id="npw",
                        value="",
                        disabled=False,
                        placeholder="Type New Password",
                    ),
                    width=6,
                ),
            ],
            className="mb-2",
        ),
        html.Br(),
    ]
)

# Layout of the application
layout = html.Div(
    [
        cm.navigation,
        cm.top,
        html.Div(
            [
                html.Div(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("CHANGE PASSWORD", className="flex",
                                    style={  'background-color': '#2E4178',
                                        'color': 'white',  # White text for header
                                        'font-size': '24px',
                                        'font-weight': 'bold'}),
                                dbc.CardBody(
                                    [
                                        dbc.Container(
                                            [
                                                modal,
                                                html.Div(
                                                    [
                                                        newpass_form,
                                                        html.Br(),
                                                        dbc.Button(
                                                            "Change Password",
                                                            id="change-pw",
                                                            className="choice",
                                                            n_clicks=0,
                                                            style={'backgroundColor': '#5474D5'},
                                                        ),
                                                    ],
                                                    className="flex row",
                                                ),
                                            ],
                                            className="flex homeshow",
                                        )
                                    ]
                                ),
                            ]
                        ),
                    ],
                    className="body",
                )
            ],
            className="flex body-container",
        ),
    ]
)

# Callback to change password and update modal based on result
@app.callback(
    [
        Output("modal-header", "children"),
        Output("modal-body", "children"),
        Output("modal", "is_open"),
    ],
    [
        Input("change-pw", "n_clicks"),
        Input("close-modal", "n_clicks"),
    ],
    [
        State("cpw", "value"),
        State("npw", "value"),
        State("auth", "data"),
    ],
)
def change_pass(click, close_click, cur_pw, new_pw, accdata):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if trigger_id == "change-pw" and click and click > 0:
        # Check if current password matches the stored password
        sql = "SELECT admin_pass FROM admin WHERE admin_name=%s"
        values = [accdata["acc"]]
        cols = ["pw"]
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0 and df["pw"][0] == cur_pw:
            # Update password in the database
            sql_update = "UPDATE admin SET admin_pass=%s WHERE admin_name=%s"
            values_update = [new_pw, accdata["acc"]]
            db.modifydatabase(sql_update, values_update)

            # Return modal messages for success
            return (
                html.H3("SUCCESS"),
                "Password Changed Successfully",
                True,
            )
        else:
            # Return modal messages for current password mismatch
            return (
                html.H3("ERROR"),
                "Current Password is Incorrect",
                True,
            )

    if trigger_id == "close-modal" and close_click and close_click > 0:
        return "", "", False

    raise PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
