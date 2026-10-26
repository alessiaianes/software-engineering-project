import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_table
from pony import orm
import datetime as dt
from tabelledb import (paziente_entity, utente_entity, medico_entity, infermiere_entity, ambulatorio_entity,
sala_entity, visita_entity, prestazione_entity, data_entity, controllo_entity,
cura_entity, servizio_entity, sostituzione_entity)
from query import (seleziona_date_prestazione, check_riempimento, fill_segreteria, fill_date, fill_sale,
fill_ambulatori, fill_visite, fill_prestazioni, check_credentials, check_user, seleziona_medico, insert_med,
elimina_med, seleziona_paziente, insert_paz, elimina_paz, seleziona_infermiere, insert_inf, elimina_inf, checkMail,
checkRes, seleziona_data, orari_visita, orari_prestazione, find_medico, show_visite, show_prestazioni,
seleziona_paziente_minore, seleziona_responsabile, find_paziente, show_servizi, seleziona_sostituti, plan, sel_orario,
aggiungi_controllo, sel_orario_cura, aggiungi_cura, sel_date_visita, sel_date_prestazione, aggiungi_esito,
aggiungi_esito_pres, sel_date_seg, conferma_visita, sel_date_seg_pres, conferma_prestazione, show_visite_medici,
show_prestazioni_infermiere, tipo_visita, find_medico_conv)


db = orm.Database()
db.bind(provider = 'sqlite', filename='casaSalute.db', create_db=True)


utenti = utente_entity(db, orm)
date = data_entity(db, orm)
medici = medico_entity(db, orm, utenti, date)
infermieri = infermiere_entity(db, orm, utenti)
pazienti = paziente_entity(db, orm, medici, utenti)
ambulatori = ambulatorio_entity(db, orm)
sale = sala_entity(db, orm)
visite = visita_entity(db, orm, date)
prestazioni = prestazione_entity(db, orm, date)
controlli = controllo_entity(db, orm, pazienti, visite, medici, ambulatori)
cure = cura_entity(db, orm, pazienti, prestazioni, infermieri, sale)
servizi = servizio_entity(db, orm, infermieri, date, sale)
sostituzioni = sostituzione_entity(db, orm, medici, date)


db.generate_mapping(create_tables=True)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

if check_riempimento(utenti, date, sale, prestazioni, ambulatori, visite) == False:
    fill_segreteria(utenti)
    fill_date(date)
    fill_sale(sale)
    fill_ambulatori(ambulatori)
    fill_visite(visite, date)
    fill_prestazioni(prestazioni, date)


login_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Login"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Nome utente", html_for="username"),
                                        dbc.Input(type="text", id="username", placeholder="Inserisci il tuo nome utente"),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Password", html_for="password"),
                                        dbc.Input(type="password", id="password", placeholder="Inserisci la tua password"),
                                    ],
                                    className="mt-3",
                                ),
                                dbc.Button("Accedi", color="primary", className="mt-3 mb-3 w-100", id='login-button', n_clicks=0),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True
)

#Implementazione NAVBAR
navbarPaz = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Casa della Salute")),
                ],
                align="center",
                className="g-0",
            ),
            href="/"
        ),
        dbc.Nav(
            [
            dbc.NavItem(dbc.NavLink("Prenotazione visita", id='prenotaV', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Prenotazione prestazione", id='prenotaP', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Visualizzazione visite passate", id='visualizzaVP', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Visualizzazione prestazioni passate", id='visualizzaPP', n_clicks=0))
            ],
            navbar=True
            
        ),
    ],
    color="dark",
    dark=True,
)


navbarMed = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Casa della Salute")),
                ],
                align="center",
                className="g-0",
            ),
            href="/",
        ),
        dbc.Nav(
            [
            dbc.NavItem(dbc.NavLink("Gestione visita", id='gestisciV', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Visualizzazione visite passate", id='visualizzaVM', n_clicks=0))],
            navbar=True
            
        ),
    ],
    color="dark",
    dark=True,
)


navbarInf = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Casa della salute")),
                ],
                align="center",
                className="g-0",
            ),
            href="/",
        ),
        dbc.Nav(
            [
            dbc.NavItem(dbc.NavLink("Gestione prestazione", id='gestisciP', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Visualizzazione prestazioni passate", id='visualizzaPI', n_clicks=0)),
            dbc.NavItem(dbc.NavLink("Visualizzazione piano di servizio", id='visualizzaPS', n_clicks=0))],
            navbar=True
            
        ),
    ],
    color="dark",
    dark=True,
)

navbarSeg = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Casa della Salute")),
                ],
                align="center",
                className="g-0",
            ),
            href="/",
        ),
        dbc.Nav(
            [
             dbc.NavItem(dbc.NavLink("Gestione visita", id='gestisciVS', n_clicks=0)),
             dbc.NavItem(dbc.NavLink("Gestione prestazione", id='gestisciPS', n_clicks=0)),
             dbc.NavItem(dbc.NavLink("Gestione pazienti", id='inserisciPaz', n_clicks=0)),
             dbc.NavItem(dbc.NavLink("Gestione medici", id='inserisciMed', n_clicks=0)),
             dbc.NavItem(dbc.NavLink("Gestione infermieri", id='inserisciInf', n_clicks=0))],
            navbar=True
            
        ),
    ],
    color="dark",
    dark=True,
)

#Layout PRENOTAZIONI
prenota_visita = dbc.Container(
    [
        dbc.Row([
            dbc.Col(
                html.Div(
                    [
                        html.H2("Prenotazione Visita"),
                        dbc.Label("Medico"),
                        dbc.Input(type="text", id="medico-prenotazione", placeholder="Medico", disabled=True),
            
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Tipo"),
                                        dcc.Dropdown(
                                            id="tipo-visita-dropdown",
                                            options=['Adulti', 'Pediatrica'],
                                            disabled = True
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Paziente minorenne"),
                                        dcc.Dropdown(
                                            id="paziente-minore-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3", style={'display':'none'}, id = "paziente-minore-stile"
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Data della Visita"),
                                        dcc.Dropdown(
                                            id="dateV-dropdown",
                                            options=[],
                                        )
                                ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Ora della Visita"),
                                        dcc.Dropdown(
                                            id="timeV-dropdown",
                                            options=[]
                                )],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Regime della Visita"),
                                        dcc.Dropdown(
                                            id="regime-dropdown",
                                            options=['Visita sportiva', 'Vista di controllo', 'Visita cardiaca', 'Visita oculistica'],
                                            
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                 
                                dbc.Button("Prenota Visita", id='prenotazione-visita', color="primary", className="mt-3 w-100"),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            ),
            
    ])
    ],
    className="h-100",
    fluid=True,
    id = "output-prenotazione"
)


@app.callback(
    Output('prenotazione-visita', 'disabled'),
    [Input('paziente-minore-dropdown', 'value'), Input('dateV-dropdown', 'value'), Input('timeV-dropdown', 'value'), Input('regime-dropdown', 'value'), Input('tipo-visita-dropdown', 'value'), Input('paziente-minore-stile', 'style')]
)
def enable_button(minore, data, ora, regime, tipo, stilemin):
    if tipo == 'Pediatrica' and minore == None and stilemin=={'display':'block'}:
        return True
    elif tipo == None or data == None or ora == None or regime == None:
        return True
    else:
        return False


@app.callback(
    [Output('tipo-visita-dropdown', 'value'), Output('tipo-visita-dropdown', 'disabled')],
    [Input('tipo-visita-dropdown', 'value'), Input('user-store', 'data'), Input('paziente-minore-dropdown', 'value')]
)
def update(tipov, cred, minore):
    user = cred['username']
    psw = cred['password']
    if checkRes(user, psw, pazienti, utenti):
        return tipov, False
    else:
        return tipo_visita(user, psw, utenti, pazienti, minore), True



prenota_prestazione = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Prenotazione prestazione"),
                        dbc.Form(
                            [
                                
                                html.Div(
                                    [
                                        dbc.Label("Tipo di prestazione"),
                                        dcc.Dropdown(
                                            id="tipoP-dropdown",
                                            options=['Prelievo', 'Medicazione'],
                                        ),
                                    ],
                                    className="mt-3", 
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Data della prestazione"),
                                        dcc.Dropdown(
                                            id="dateP-dropdown",
                                            options=[]
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Ora della prestazione"),
                                        dcc.Dropdown(
                                            id="timeP-dropdown",
                                            options=[]
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                
                                dbc.Button("Prenota prestazione", id='prenota-prestazione', color="primary", className="mt-3 w-100"),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id='output-prestazione'
)

@app.callback(
    Output('prenota-prestazione', 'disabled'),
    [Input('dateP-dropdown', 'value'), Input('timeP-dropdown', 'value'), Input('tipoP-dropdown', 'value')]
)
def enable_button(data, ora, tipo):
    if data != None and ora != None and tipo != None:
        return False
    else:
        return True


prenota_pres_minore = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Prenotazione prestazione"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Paziente"),
                                        dcc.Dropdown(
                                            id="paziente-prestazione-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Tipo di prestazione"),
                                        dcc.Dropdown(
                                            id="tipoPmin-dropdown",
                                            options=['Prelievo', 'Medicazione'],
                                        ),
                                    ],
                                    className="mt-3", 
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Data della prestazione"),
                                        dcc.Dropdown(
                                            id="datePmin-dropdown",
                                            options=[]
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Ora della prestazione"),
                                        dcc.Dropdown(
                                            id="timePmin-dropdown",
                                            options=[]
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                
                                dbc.Button("Prenota prestazione", id='prenota-prestazione-minore', color="primary", className="mt-3 w-100"),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id='output-prestazione-min'
)



@app.callback(
    Output('datePmin-dropdown', 'options'),
    Input('tipoPmin-dropdown', 'value')
)
def update_date(tipoP):
    return seleziona_date_prestazione(sale, servizi, date, tipoP)

#Aggiornamento menu a tendina orario per prenotazione prestazione
@app.callback(
    Output('timePmin-dropdown', 'options'),
    [Input('datePmin-dropdown', 'value'), Input('tipoPmin-dropdown', 'value')], 
)
def update_date(dataP, tipoP):
    if dataP == None:
        return []
    else:
        orari = sel_orario_cura(date, prestazioni, cure, sale, dataP, tipoP)
        return orari


#Aggiornamento menu a tendina paziente per prenotazione prestazione
@app.callback(
    [Output("paziente-prestazione-dropdown", 'options')],
    [Input('user-store', 'data')]
)
def update(cred):
    user = cred['username']
    psw = cred['password']
    return [seleziona_paziente_minore(utenti, pazienti, user, psw)]


@app.callback(
    Output('prenota-prestazione-minore', 'disabled'),
    [Input('paziente-prestazione-dropdown', 'value'), Input('datePmin-dropdown', 'value'), Input('timePmin-dropdown', 'value'), Input('tipoPmin-dropdown', 'value')]
)
def enable_button(paz, data, ora, tipo):
    if paz != None and data != None and ora != None and tipo != None:
        return False
    else:
        return True

#Prenotazione della prestazione minori
@app.callback(
    Output('output-prestazione-min', 'children'),
    Input('prenota-prestazione-minore', 'n_clicks'),
    [State('paziente-prestazione-dropdown', 'value'), State('datePmin-dropdown', 'value'), State('timePmin-dropdown', 'value'), State('tipoPmin-dropdown', 'value')]
)
def update_prenotazione(n_clicks, npaz, data_pres, ora_pres, tipoP):
    if n_clicks != None:
        result = aggiungi_cura(cure, prestazioni, sale, servizi, pazienti, date, npaz, data_pres, ora_pres, tipoP)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return prenota_pres_minore




prenotazione_prestazione_adulti_minori = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Prenota una prestazione per il tuo minore", id="lay-pren-pres-min-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Prenota una prestazione per te", id="lay-pren-pres-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], className="d-flex justify-content-end"), 
                ], style={'marginTop':'10px'}),
                html.Div(id="contenuto-prenotazione-prestazioni", className="mt-3") 
        ])
    ])

@app.callback(
    Output('contenuto-prenotazione-prestazioni', 'children'),
    [Input('lay-pren-pres-min-button', 'n_clicks'), Input('lay-pren-pres-button', 'n_clicks')]
)
def update_pag(n_clicksINS, n_clicksDEL):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'lay-pren-pres-min-button':
        return prenota_pres_minore
    elif button_id == 'lay-pren-pres-button':
        return prenota_prestazione





#Layout VISUALIZZAZIONI
visualizza_visite = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                
                html.Div(
                    [
                        html.H2("Tabella Informazioni Visite"),
                        dash_table.DataTable(
                            id='table-visite-passate',
                            columns=[],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=10,  # Numero di righe per pagina
                        ), 
                        html.Div(id='ricerca-visite')
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "1000px", "margin": "auto", "marginTop": "20vh"},
                    
                    
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
   )

#Visualizzazione tabella di servizio
@app.callback(
    [Output('table-visite-passate', 'columns'), Output('table-visite-passate', 'data'), Output('ricerca-visite', 'children')],
    Input('user-store', 'data')
)
def update(cred):
    user = cred['username']
    psw = cred['password']
    utente_log = check_user(user, psw, medici, infermieri, pazienti, utenti)

    if utente_log == 'PAZIENTE':
        paz = find_paziente(user, psw, utenti, pazienti)[0]
        visite_passate = show_visite(controlli, visite, pazienti, medici, date, ambulatori, paz)
        if [] not in visite_passate:
       
            visite_eff = {'Cognome e Nome Medico': visite_passate[0], 'Esito':visite_passate[1], 'Data': visite_passate[2], 'Ora': visite_passate[3], 'Regime': visite_passate[4], 'Tipo': visite_passate[5], 'Ambulatorio': visite_passate[6], 'Urgenza': visite_passate[7], 'Note':visite_passate[8]}       
       
            df = pd.DataFrame(visite_eff)
       
            colonne = [{"name": i, "id": i} for i in df.columns]
            dati = df.to_dict('records')
            return colonne, dati, []
        else:
            return [], [], "Non sono ancora state effettuate visite per questo paziente"

    elif utente_log == 'MEDICO':
        visite_passate = show_visite_medici(controlli, visite, pazienti, medici, utenti, date, ambulatori, user, psw)
       
        if [] not in visite_passate:
      
            visite_eff = {'Cognome e Nome Paziente': visite_passate[0], 'Esito':visite_passate[1], 'Data': visite_passate[2], 'Ora': visite_passate[3], 'Regime': visite_passate[4], 'Tipo': visite_passate[5], 'Ambulatorio': visite_passate[6], 'Urgenza': visite_passate[7], 'Note':visite_passate[8]}       
       
            df = pd.DataFrame(visite_eff)
     
            colonne = [{"name": i, "id": i} for i in df.columns]
            dati = df.to_dict('records')
            return colonne, dati, []
        else:
          
            return [], [], "Non sono ancora state effettuate visite per questo paziente"




mostra_servizio =  dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                dbc.Form(
                        html.Div(
                                    [
                                        dbc.Label("Data di servizio"),
                                        dcc.Dropdown(
                                            id="date-servizio-dropdown",
                                            options=seleziona_data(date),
                                        ),
                                    ],
                                    className="mt-3",
                                )
                                ),
                html.Div(
                    [
                        
                        html.H2("Piano di Servizio"),
                        dash_table.DataTable(
                            id='table-servizio',
                            columns=[],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=10, 
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "800px", "margin": "auto", "marginTop": "40px"},
                    id='output-serivizio'
                )
    ])
        )
    ],
    className="h-100",
    fluid=True)


visualizza_visite_minori = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Paziente"),
                                        dcc.Dropdown(
                                            id="paziente-minore-visua-visite-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3"
                                ),]),
                html.Div(
                    [
                        html.H2("Tabella Informazioni Visite"),
                        dash_table.DataTable(
                            id='table-visite-minori',
                            columns=[],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=10,  # Numero di righe per pagina
                        ),
                        html.Div(id='ricerca-visite-minori')
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "1000px", "margin": "auto", "marginTop": "20vh"},
                    id='outputVVPM'
                )
    ])
        )
    ],
    className="h-100",
    fluid=True,
)

#Visualizzazione tabella di servizio
@app.callback(
    [Output('table-visite-minori', 'columns'), Output('table-visite-minori', 'data'), Output('ricerca-visite-minori', 'children')],
    Input('paziente-minore-visua-visite-dropdown', 'value')
)
def update(paz):
    visite_passate = show_visite(controlli, visite, pazienti, medici, date, ambulatori, paz)
    if paz == None:
        return [], [], []
    if [] not in visite_passate:
        visite_eff = {'Cognome e Nome Medico': visite_passate[0], 'Esito':visite_passate[1], 'Data': visite_passate[2], 'Ora': visite_passate[3], 'Regime': visite_passate[4], 'Tipo': visite_passate[5], 'Ambulatorio': visite_passate[6], 'Urgenza': visite_passate[7], 'Note':visite_passate[8]}       
       
        df = pd.DataFrame(visite_eff)
        colonne = [{"name": i, "id": i} for i in df.columns]
        dati = df.to_dict('records')
        return colonne, dati, []
    else:
        return [], [], 'Non sono ancora state effettuate visite per questo paziente'



visualizza_prestazioni = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Tabella Informazioni Prestazioni"),
                        dash_table.DataTable(
                            id='table-prestazioni-passate',
                            columns=[],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=10,  # Numero di righe per pagina
                        ),
                        html.Div(id='ricerca-prestazioni')
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "800px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
)

#Visualizzazione tabella di servizio
@app.callback(
    [Output('table-prestazioni-passate', 'columns'), Output('table-prestazioni-passate', 'data'), Output('ricerca-prestazioni', 'children')],
    Input('user-store', 'data')
)
def update(cred):
    user = cred['username']
    psw = cred['password']
    utente_log = check_user(user, psw, medici, infermieri, pazienti, utenti)
   
    if utente_log == 'PAZIENTE':
        paz = find_paziente(user, psw, utenti, pazienti)[0]
        prestazioni_passate = show_prestazioni(cure, prestazioni, pazienti, infermieri, date, sale, paz)
        if [] not in prestazioni_passate:
            prestazioni_eff = {'Cognome e Nome Infermiere': prestazioni_passate[0], 'Esito':prestazioni_passate[1], 'Data': prestazioni_passate[2], 'Ora': prestazioni_passate[3], 'Tipo': prestazioni_passate[4], 'Sala': prestazioni_passate[5], 'Note': prestazioni_passate[6]}       
      
            df = pd.DataFrame(prestazioni_eff)
            colonne = [{"name": i, "id": i} for i in df.columns]
            dati = df.to_dict('records')
            return colonne, dati, []
        else:
            return [], [], "Non sono ancora state effettuate prestazioni per questo paziente"
    elif utente_log == 'INFERMIERE':
        prestazioni_passate = show_prestazioni_infermiere(cure, prestazioni, pazienti, infermieri, utenti, date, sale, user, psw)
        if [] not in prestazioni_passate:
       
            prestazioni_eff = {'Cognome e Nome Paziente': prestazioni_passate[0], 'Esito':prestazioni_passate[1], 'Data': prestazioni_passate[2], 'Ora': prestazioni_passate[3], 'Tipo': prestazioni_passate[4], 'Sala': prestazioni_passate[5], 'Note': prestazioni_passate[6]} 
       
            df = pd.DataFrame(prestazioni_eff)
            colonne = [{"name": i, "id": i} for i in df.columns]
            dati = df.to_dict('records')
            return colonne, dati, []
        else:
            return [], [], "Non sono ancora state effettuate prestazioni"
        
   


visualizza_prestazioni_minori = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Paziente"),
                                        dcc.Dropdown(
                                            id="paziente-minore-visua-prestazioni-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3"
                                ),]),
                html.Div(
                    [
                        html.H2("Tabella Informazioni Prestazioni"),
                        dash_table.DataTable(
                            id='table-prestazioni-minori',
                            columns=[],
                            data=[],
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_cell={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white',
                                'textAlign': 'left'
                            },
                            page_size=10,  # Numero di righe per pagina
                        ),
                        html.Div(id='ricerca-prestazioni-minori')
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "800px", "margin": "auto", "marginTop": "20vh"},
                    id = 'outputVPPM'
                )
    ])
        )
    ],
    className="h-100",
    fluid=True,
)
#Visualizzazione tabella di servizio
@app.callback(
    [Output('table-prestazioni-minori', 'columns'), Output('table-prestazioni-minori', 'data'), Output('ricerca-prestazioni-minori', 'children')],
    Input('paziente-minore-visua-prestazioni-dropdown', 'value')
)
def update(paz):
    prestazioni_passate = show_prestazioni(cure, prestazioni, pazienti, infermieri, date, sale, paz)
    if paz == None:
        return [],[],[]
    if [] not in prestazioni_passate:
        prestazioni_eff = {'Cognome e Nome Infermiere': prestazioni_passate[0], 'Esito':prestazioni_passate[1], 'Data': prestazioni_passate[2], 'Ora': prestazioni_passate[3], 'Tipo': prestazioni_passate[4], 'Sala': prestazioni_passate[5], 'Note': prestazioni_passate[6]}       
        
        df = pd.DataFrame(prestazioni_eff)
        colonne = [{"name": i, "id": i} for i in df.columns]
        dati = df.to_dict('records')
        return colonne, dati, []
    else:
        return [], [], 'Non sono ancora state effettuate prestazioni per questo paziente'


#Layout GESTIONI
gestisci_visita = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Gestisci Visita"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Data della visita"),
                                        dcc.Dropdown(
                                            id="dateGV-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                    dbc.Label("Esito"),
                                    dcc.Textarea(id='input-codice', placeholder="Inserisci l'esito",
                                    style={'width': '100%', 'height': '100px', 'fontSize': '16px'}),
                                    html.Label('Urgente', style={'padding-right': '10px', 'margin-top':'10px'}),
                                    dcc.Checklist(
                                        id='urgenza-checkbox',
                                        options=[{'label': '', 'value': 'urgent'}],
                                        value=[],
                                        style={'display': 'inline-block'}
                                    ),   
                               
                                dbc.Button("Aggiungi esito", color="primary", className="mt-3 w-100", id='aggiungi-esito', disabled=True),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id = 'output-aggiunta-esitoV'
)


@app.callback(
    Output('aggiungi-esito', 'disabled'),
    [Input('input-codice', 'value'), Input('dateGV-dropdown', 'value')]
)
def enable_button(esito, datav):
    if esito and datav != None:
        return False
    else:
        return True

@app.callback(
    [Output('dateGV-dropdown', 'options')],
    Input('user-store', 'data')
)
def update(cred):
    user = cred['username']
    psw = cred['password']
    datasel = sel_date_visita(date, controlli, visite, utenti, medici, pazienti, user, psw)
   
    return datasel 

@app.callback(
    Output('output-aggiunta-esitoV', 'children'),
    Input('aggiungi-esito', 'n_clicks'),
    [State('dateGV-dropdown', 'value'), State('input-codice', 'value'), State('user-store', 'data'), State('urgenza-checkbox', 'value')]
)
def update_esito(n_clicks, dataV, esito, cred, urgenza):
    user = cred['username']
    psw = cred['password']
    res = aggiungi_esito(controlli, date, visite, pazienti, medici, utenti, dataV, esito, user, psw, urgenza)
    if res == []:
        return gestisci_visita
    else:
        return html.Div(res, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")

gestisci_prestazione = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Gestisci prestazione"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Data della prestazione"),
                                        dcc.Dropdown(
                                            id="dateGP-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                    dbc.Label("Esito"),
                                    dcc.Textarea(id='input-codice-pres', placeholder="Inserisci l'esito",
                                    style={'width': '100%', 'height': '100px', 'fontSize': '16px'}),   
                               
                                dbc.Button("Aggiungi esito", color="primary", className="mt-3 w-100", id='aggiungi-esito-pres', disabled=True),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "400px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id = 'output-aggiunta-esitoP'
)
@app.callback(
    Output('aggiungi-esito-pres', 'disabled'),
    [Input('input-codice-pres', 'value'), Input('dateGP-dropdown', 'value')]
)
def enable_button(esito, datap):
    if esito and datap != None:
        return False
    else:
        return True


@app.callback(
    [Output('dateGP-dropdown', 'options')],
    Input('user-store', 'data')
)
def update(cred):
    user = cred['username']
    psw = cred['password']
    datasel = sel_date_prestazione(date, cure, prestazioni, utenti, infermieri, pazienti, user, psw)
    return datasel

@app.callback(
    Output('output-aggiunta-esitoP', 'children'),
    Input('aggiungi-esito-pres', 'n_clicks'),
    [State('dateGP-dropdown', 'value'), State('input-codice-pres', 'value'), State('user-store', 'data')]
)
def update_esito(n_clicks, datap, esito, cred):
    user = cred['username']
    psw = cred['password']
    res = aggiungi_esito_pres(cure, date, prestazioni, pazienti, infermieri, utenti, datap, esito, user, psw)
    if res == []:
        return gestisci_prestazione
    else:
        return html.Div(res, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")


gestisci_visita_seg = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Conferma visita"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Data della visita"),
                                        dcc.Dropdown(
                                            id="dateGVS-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                    dbc.Label("Aggiungi eventuali note"),
                                    dcc.Textarea(id='input-note', placeholder="Inserisci note",
                                    style={'width': '100%', 'height': '100px', 'fontSize': '16px'}),   
                               
                                dbc.Button("Conferma visita", color="primary", className="mt-3 w-100", id='conferma-visita', disabled=True),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "700px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id = 'output-conferma-visita'
)

@app.callback(
    Output('conferma-visita', 'disabled'),
    [Input('dateGVS-dropdown', 'value')]
)
def enable_button(datav):
    if datav != None:
        return False
    else:
        return True

@app.callback(
    [Output('dateGVS-dropdown', 'options')],
    Input('user-store', 'data')
)
def update(trigger):
    datasel =  sel_date_seg(visite, pazienti, medici, date, controlli)
    
    return datasel 

@app.callback(
    Output('output-conferma-visita', 'children'),
    Input('conferma-visita', 'n_clicks'),
    [State('dateGVS-dropdown', 'value'), State('input-note', 'value')]
)
def update_esito(n_clicks, dataV, note):
    res = conferma_visita(controlli, date, visite, pazienti, medici, dataV, note)
    if res == []:
        return gestisci_visita_seg
    else:
        return html.Div(res, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    

gestisci_prestazione_seg = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Conferma prestazione"),
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Data della prestazione"),
                                        dcc.Dropdown(
                                            id="dateGPS-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                    dbc.Label("Aggiungi eventuali note"),
                                    dcc.Textarea(id='input-note-prestazione', placeholder="Inserisci note",
                                    style={'width': '100%', 'height': '100px', 'fontSize': '16px'}),   
                               
                                dbc.Button("Conferma prestazione", color="primary", className="mt-3 w-100", id='conferma-prestazione', disabled=True),
                            ]
                        ),
                    ],
                    className="p-4 shadow-lg rounded",
                    style={"max-width": "700px", "margin": "auto", "marginTop": "20vh"},
                )
            )
        )
    ],
    className="h-100",
    fluid=True,
    id = 'output-conferma-prestazione'
)

@app.callback(
    Output('conferma-prestazione', 'disabled'),
    [Input('dateGPS-dropdown', 'value')]
)
def enable_button(datap):
    if datap != None:
        return False
    else:
        return True

@app.callback(
    [Output('dateGPS-dropdown', 'options')],
    Input('user-store', 'data')
)
def update(trigger):
   
    datasel =  sel_date_seg_pres(prestazioni, pazienti, infermieri, date, cure)
    
    return datasel 

@app.callback(
    Output('output-conferma-prestazione', 'children'),
    Input('conferma-prestazione', 'n_clicks'),
    [State('dateGPS-dropdown', 'value'), State('input-note-prestazione', 'value')]
)
def update_esito(n_clicks, dataP, note):
    res = conferma_prestazione(cure, date, prestazioni, pazienti, infermieri, dataP, note)
    if res == []:
        return gestisci_prestazione_seg
    else:
        return html.Div(res, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")

gestione_medici = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Inserisci Medico", id="inserisci-medico-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Elimina Medico", id="elimina-medico-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], className="d-flex justify-content-end"),
            dbc.Col(
                html.Button("Gestisci sostituzioni", id="sostituzione-medico-button", className="btn btn-primary btn-block", n_clicks=0)
                ), 
                ]),
                html.Div(id="contenuto-gestione-medico", className="mt-3") 
        ], style={'marginTop':'10px'})
    ])

gestione_pazienti = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Inserisci Paziente", id="inserisci-paziente-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Elimina Paziente", id="elimina-paziente-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], className="d-flex justify-content-end"), 
                ], style={'marginTop':'10px'}),
                html.Div(id="contenuto-gestione-paziente", className="mt-3") 
        ])
    ])


gestione_visita_adulti_minori = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Visualizza le tue visite", id="visua-visite-passate-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Visualizza le visite dei tuoi minori", id="visua-visite-minori-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], id='allineamento-contenuto', className="d-flex justify-content-end"), 
                ], style={'marginTop':'10px'}),
                html.Div(id="contenuto-gestione-visite-passate", className="mt-3") 
        ])
    ])


gestione_prestazione_adulti_minori = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Visualizza le tue prestazioni", id="visua-prestazioni-passate-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Visualizza le prestazioni dei tuoi minori", id="visua-prestazioni-minori-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], className="d-flex justify-content-end"), 
                ], style={'marginTop':'10px'}),
                html.Div(id="contenuto-gestione-prestazioni-passate", className="mt-3") 
        ])
    ])

gestione_infermieri = html.Div([
    dbc.Container([
        
            dbc.Row([
                dbc.Col(
                html.Button("Inserisci Infermiere/a", id="inserisci-infermiere-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                dbc.Col([
                    html.Button("Elimina Infermiere/a", id="elimina-infermiere-button", className="btn btn-primary btn-block", n_clicks=0),
                   
            ], className="d-flex justify-content-end"), 
            dbc.Col(
                html.Button("Visualizza giornate di servizio", id="servizio-infermiere-button", className="btn btn-primary btn-block", n_clicks=0)
                ),
                ]),
                html.Div(id="contenuto-gestione-infermiere", className="mt-3") 
        ], style={'marginTop':'10px'})
    ])




#Layout INSERIMENTI
inserisci_paziente = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Inserisci le Informazioni del Paziente", className="text-center")),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Input(id="nome", type="text", placeholder="Nome *", className="form-control mb-3"),
                dcc.Input(id="cognome", type="text", placeholder="Cognome *", className="form-control mb-3"),
                dcc.DatePickerSingle(
                    id="data-nascita",
                    placeholder="Data di Nascita *",
                    display_format='DD/MM/YYYY',
                    className="form-control mb-3"
                ),
                dcc.Input(id="luogo-nascita", type="text", placeholder="Luogo di Nascita *", className="form-control mb-3"),
                dcc.Input(id="email", type="email", placeholder="Email *", className="form-control mb-3", style={'display': 'none'}),
                html.Div([
                                dbc.Label("Responsabile *"),
                                dcc.Dropdown(
                                                id="responsabile",
                                                options=[],
                                                placeholder="Seleziona responsabile",
                                            )
                                    ], id='stileResp', className="mb-3", style={'display': 'none'}),
                
                dcc.Input(id="email-responsabile", type="text", placeholder="Email Responsabile *", value=' ', disabled=True, className="form-control mb-3", style={'display': 'none'}),
                html.Div([
                                dbc.Label("Medico convenzionato *"),
                                dcc.Dropdown(
                                                id="medico-convenzionato",
                                                options=[],
                                                placeholder="Seleziona medico"
                                            )
                                    ], className="mt-3")
                                    ])
            ]),
                html.Button("Inserisci Paziente", id="inserisciP-button", className="btn btn-primary btn-block", n_clicks=0),
         ])
    ], id="outputP", className="mt-3")

@app.callback(
    Output('inserisciP-button', 'disabled'),
    [Input('nome', 'value'), Input('cognome', 'value'), Input('data-nascita', 'date'), Input('luogo-nascita', 'value'), Input('email', 'value'), Input('responsabile', 'value'), Input('medico-convenzionato', 'value')]
)
def enable_button(n, c, dn, ln, em, r, med):
    if n != None and c != None and dn != None and ln != None and med != None:
        date_obj = dt.datetime.strptime(dn, '%Y-%m-%d')
        threshold_date = dt.datetime(2010, 1, 1)
        if date_obj < threshold_date:
            if em == None:
                return True
            else:
                return False
        else:
            if r == None:
                return True
            else:
                return False
    else:
        return True

inserisci_medico = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Inserisci le Informazioni del Medico", className="text-center")),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Input(id="codice-fiscale", type="text", placeholder="Codice Fiscale *", className="form-control mb-3"),
                dcc.Input(id="nomeM", type="text", placeholder="Nome *", className="form-control mb-3"),
                dcc.Input(id="cognomeM", type="text", placeholder="Cognome *", className="form-control mb-3"),
                
                dcc.Input(id="specialita", type="text", placeholder="Specialità", className="form-control mb-3"),
         
                html.Button("Inserisci", id="inserisciM-button", className="btn btn-primary btn-block", n_clicks=0),
                
                
            ]),
        ]),
    ])
], id="outputM", className="mt-3")

@app.callback(
    Output('inserisciM-button', 'disabled'),
    [Input('codice-fiscale', 'value'), Input('nomeM', 'value'), Input('cognomeM', 'value')]
)
def enable_button(cf, n, c):
    if cf == None or n == None or c == None:
        return True
    else:
        return False


inserisci_infermiere = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Inserisci le Informazioni dell'Infermiere", className="text-center")),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Input(id="codice-fiscale-inf", type="text", placeholder="Codice Fiscale *", className="form-control mb-3"),
                dcc.Input(id="nomeI", type="text", placeholder="Nome *", className="form-control mb-3"),
                dcc.Input(id="cognomeI", type="text", placeholder="Cognome *", className="form-control mb-3"),
                html.Button("Inserisci Infermiere", id="inserisciI-button", className="btn btn-primary btn-block", n_clicks = 0),
            ])
        ])
    ])
], id="outputI", className="mt-3")

@app.callback(
    Output('inserisciI-button', 'disabled'),
    [Input('codice-fiscale-inf', 'value'), Input('nomeI', 'value'), Input('cognomeI', 'value')]
)
def enable_button(cf, n, c):
    if cf == None or n == None or c == None:
        return True
    else:
        return False


#Layout ASSENZA
assenza_medico = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Pianifica Assenza", className="text-center")),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Medico da sostituire"),
                                        dcc.Dropdown(
                                            id="med-sostituire-dropdown",
                                            options=seleziona_medico(medici),
                                            
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Medico sostituto"),
                                        dcc.Dropdown(
                                            id="med-sostituto-dropdown",
                                            options=[],
                                        ),
                                    ],
                                    className="mt-3",
                                ),
                            ]),
                dcc.DatePickerRange(
                    id='date-picker-range',
                    min_date_allowed=dt.datetime.today(),
                    max_date_allowed=dt.datetime(2030, 12, 31),
                    start_date=dt.datetime.now().date(),
                    end_date=dt.datetime.now().date(),
                    display_format='DD/MM/YYYY',
                    className="form-control mb-3"
                ),
                html.Button("Pianifica Assenza", id="plan-absence-button", className="btn btn-primary btn-block"),
                #html.Div(id="absence-output", className="mt-3")
            ])
        ]),
    ])
], id="absence-output")




#Layout ELIMINAZIONI
elimina_medici = html.Div([
    dbc.Container([
        dbc.Form([
                    html.Div([
                                    dbc.Label("Seleziona il medico da eliminare"),
                                    dcc.Dropdown(
                                                    id="medici-dropdown",
                                                    options=[],
                                                    placeholder="Seleziona medico"
                                                )
                                    ], className="mt-3")
                ]),
               
                html.Button("Elimina", id="eliminaM-button", className="btn btn-primary btn-block", n_clicks=0),
            ])
], id="outputEliminazione", className="mt-3")

@app.callback(
    Output('eliminaM-button', 'disabled'),
    [Input('medici-dropdown', 'value')]
)
def enable_button(med):
    if med == None:
        return True
    else:
        return False

elimina_pazienti = html.Div([
    dbc.Container([
        dbc.Form([
                    html.Div([
                                    dbc.Label("Seleziona il paziente da eliminare"),
                                    dcc.Dropdown(
                                                    id="pazienti-dropdown",
                                                    options=[],
                                                    placeholder="Seleziona paziente"
                                                )
                                    ], className="mt-3")
                ]),
               
                html.Button("Elimina", id="eliminaP-button", className="btn btn-primary btn-block", n_clicks=0),
            ])
], id="outputEliminazionePaz", className="mt-3")

@app.callback(
    Output('eliminaP-button', 'disabled'),
    [Input('pazienti-dropdown', 'value')]
)
def enable_button(paz):
    if paz == None:
        return True
    else:
        return False

elimina_infermieri = html.Div([
    dbc.Container([
        dbc.Form([
                    html.Div([
                                    dbc.Label("Seleziona l'infermiere/a da eliminare"),
                                    dcc.Dropdown(
                                                    id="infermieri-dropdown",
                                                    options=[],
                                                    placeholder="Seleziona infermiere/a"
                                                )
                                    ], className="mt-3")
                ]),
               
                html.Button("Elimina", id="eliminaI-button", className="btn btn-primary btn-block", n_clicks=0),
            ])
], id="outputEliminazioneInf", className="mt-3")

@app.callback(
    Output('eliminaI-button', 'disabled'),
    [Input('infermieri-dropdown', 'value')]
)
def enable_button(inf):
    if inf == None:
        return True
    else:
        return False

#Layout HOME

home_paziente = html.Div([ 
        navbarPaz,
        html.Div(id='contenutoP')
])

home_medico = html.Div([
        navbarMed,
        html.Div(id='contenutoM')
])

home_infermiere = html.Div([ 
        navbarInf,
        html.Div(id='contenutoI')
])

home_segreteria = html.Div([
        navbarSeg,
        html.Div(id='contenutoS', style={'height': '100%','width': '100%'})
])


#CALLBACK

#Aggiornamento menu a tendina orari per prenotazione visita
@app.callback(
    Output('timeV-dropdown', 'options'),
    [Input('medico-prenotazione', 'value'), Input('dateV-dropdown', 'value')]
    
)
def update_date(med, dataVisita):
    if med == " " or dataVisita == None:
        return []
    else:
        orari = sel_orario(date, medici, sostituzioni, controlli, pazienti, utenti, visite, med, dataVisita)
        
        return orari

#Aggiornamento menu a tendina date per prenotazione visita
@app.callback(
    Output('dateV-dropdown', 'options'),
    Input('user-store', 'data')
)
def update_date(trigger):
    return seleziona_data(date)
    

#Prenotazione visita
@app.callback(
    Output('output-prenotazione', 'children'),
    Input('prenotazione-visita', 'n_clicks'),
    [State('paziente-minore-dropdown', 'value'), State('dateV-dropdown', 'value'), State('timeV-dropdown', 'value'), State('regime-dropdown', 'value'), State('tipo-visita-dropdown', 'value'), State('medico-prenotazione', 'value'), State('user-store', 'data')]
)
def update_prenotazione(n_clicks, minore, data, ora, regime, tipo, med, cred):
    user = cred['username']
    psw = cred['password']
    if n_clicks != None:
        result = aggiungi_controllo(controlli, visite, ambulatori, medici, pazienti, utenti, date, minore, data, ora, regime, tipo, med, user, psw)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return prenota_visita

#Aggiornamento menu a tendina date per prenotazione prestazione
@app.callback(
    Output('dateP-dropdown', 'options'),
    Input('tipoP-dropdown', 'value')
)
def update_date(tipoP):
    return seleziona_date_prestazione(sale, servizi, date, tipoP)

#Aggiornamento menu a tendina orario per prenotazione prestazione
@app.callback(
    Output('timeP-dropdown', 'options'),
    [Input('dateP-dropdown', 'value'), Input('tipoP-dropdown', 'value')],#Input('user-store', 'data')  
)
def update_date(dataP, tipoP):
    if dataP == None:
        return []
    else:
        orari = sel_orario_cura(date, prestazioni, cure, sale, dataP, tipoP)
        
        return orari

#Prenotazione della prestazione 
@app.callback(
    Output('output-prestazione', 'children'),
    Input('prenota-prestazione', 'n_clicks'),
    [State('dateP-dropdown', 'value'), State('timeP-dropdown', 'value'), State('tipoP-dropdown', 'value'), State('user-store', 'data')]
)
def update_prenotazione(n_clicks, data_pres, ora_pres, tipoP, cred):
    if n_clicks != None:
        user = cred['username']
        psw = cred['password']
        npaz = find_paziente(user, psw, utenti, pazienti)[0]
        result =  aggiungi_cura(cure, prestazioni, sale, servizi, pazienti, date, npaz, data_pres, ora_pres, tipoP)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return prenota_prestazione

#Aggiornamento menu a tendina medico da sostituire
@app.callback(
    Output('med-sostituire-dropdown', 'options'),
    Input('user-store', 'data')
)
def update_dropdown(trigger):
    return seleziona_medico(medici)

#Aggiornamento menu a tendina medico sostituto
@app.callback(
    Output('med-sostituto-dropdown', 'options'),
    Input('med-sostituire-dropdown', 'value')
)
def update_dropdown(med_da_sostituire):
    return seleziona_sostituti(med_da_sostituire, medici)

#Pianificazione assenza
@app.callback(
    Output('absence-output', 'children'),
    Input('plan-absence-button', 'n_clicks'),
    [State('date-picker-range', 'start_date'), State('date-picker-range', 'end_date'), State('med-sostituire-dropdown', 'value'), State('med-sostituto-dropdown', 'value')]
)
def piano_assenze(n_clicks, dataI, dataF, sos, sostituto):
    if n_clicks != None:
        result = plan(dataI, dataF, sos, sostituto, sostituzioni, medici, date)
        return html.Div([result[0], html.Br(), result[1]], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return assenza_medico

#Aggiornamento visibilità e contenuto del menu a tendina dei pazienti minori in fase di prenotazione visita
@app.callback(
    [Output("paziente-minore-dropdown", 'options'), Output("paziente-minore-stile", 'style')],
    [Input('user-store', 'data'), Input('tipo-visita-dropdown', 'value')]
)
def update(cred, tipoVisita):
    user = cred['username']
    psw = cred['password']
    if tipoVisita == 'Pediatrica':
        if checkRes(user, psw, pazienti, utenti):
            minori = seleziona_paziente_minore(utenti, pazienti, user, psw)
            return minori, {'display':'block'}
        else:
            return [], {'display':'none'}
    else:
        return [], {'display':'none'}


#Accesso alla HOME
@app.callback(
    [Output("content", "children"), Output('user-store', 'data')],
    [Input("login-button", "n_clicks")],
    [State("username", "value"), State("password", "value")]
)
def update_output(n_clicks, username, password):
    if n_clicks > 0:
        if username and password:
            if check_credentials(username, password, utenti):
                user_data = {'username': username, 'password': password}
                stringa = check_user(username, password, medici, infermieri, pazienti, utenti)
                if stringa=="MEDICO":
                    return [f"Benvenuto, {username}!\n", home_medico], user_data
                elif stringa=="INFERMIERE":
                    return [f'Benvenuto, {username}!\n', home_infermiere], user_data
                elif stringa=="SEGRETERIA":
                    return [f'Accesso del personale amministrativo!', home_segreteria], user_data
                elif stringa=='PAZIENTE':
                    return [f'Benvenuto, {username}!\n', home_paziente], user_data

            else:
                return [login_layout, html.Div("Nome utente o password errati.", style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'16px'})], None

        else:
            return [login_layout, html.Div("Per favore, inserisci sia il nome utente che la password.", style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'16px'})], None

    else:
        return login_layout, None


#Visualizzazione del medico in fase di prenotazione visita (PAZIENTE)
@app.callback(
    Output('medico-prenotazione', 'value'),
    [Input('paziente-minore-dropdown', 'value'), Input('user-store', 'data'), Input('dateV-dropdown', 'value')]
)
def update(minorenne, cred, data_visita):
    user = cred['username']
    psw = cred['password']
    med = find_medico(medici, pazienti, utenti, sostituzioni, date, user, psw, minorenne, data_visita)
    if med != None:
        return med[0][0]+" "+med[0][1]
    else:
        return find_medico_conv(user, psw, pazienti, utenti, medici)[0][0]+" "+find_medico_conv(user, psw, pazienti, utenti, medici)[0][1]


#Cambio pagina PAZIENTE
@app.callback(
    Output('contenutoP', 'children'),
    [Input('prenotaV', 'n_clicks'), Input('visualizzaVP', 'n_clicks'), Input('prenotaP', 'n_clicks'), Input('visualizzaPP', 'n_clicks'), Input('user-store', 'data')],

)
def update(n_clicksPvis, n_clicksVvis, n_clicksPpr, n_clicksVpr, cred):

    user = cred['username']
    psw = cred['password']
    

    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'prenotaV':
            return prenota_visita
        elif button_id == 'visualizzaVP':
            if checkRes(user, psw, pazienti, utenti):
                return gestione_visita_adulti_minori
                                
            else:
                return visualizza_visite
        elif button_id == 'prenotaP':
            if checkRes(user, psw, pazienti, utenti):
                return prenotazione_prestazione_adulti_minori
            else:
                return prenota_prestazione
        elif button_id == 'visualizzaPP':
            if checkRes(user, psw, pazienti, utenti):
                return gestione_prestazione_adulti_minori
            else:
                return visualizza_prestazioni
        else:
            return []



#Cambio pagina MEDICO
@app.callback(
    Output('contenutoM', 'children'),
    [Input('gestisciV', 'n_clicks'), Input('visualizzaVM', 'n_clicks')]
)
def update(n_clicksGvis, n_clicksVMvis):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'gestisciV':
            return gestisci_visita
        elif button_id == 'visualizzaVM':
            return visualizza_visite


#Cambio pagina INFERMIERE
@app.callback(
    Output('contenutoI', 'children'),
    [Input('gestisciP', 'n_clicks'), Input('visualizzaPI', 'n_clicks'), Input('visualizzaPS', 'n_clicks')]
)
def update(n_clicksGpr, n_clicksVIpr, n_clicksPS):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'gestisciP':
            return gestisci_prestazione
        elif button_id == 'visualizzaPI':
            return visualizza_prestazioni
        elif button_id == 'visualizzaPS':
            return mostra_servizio


#cambio pagina SEGRETERIA
@app.callback(
    Output('contenutoS', 'children'),
    [Input('gestisciVS', 'n_clicks'), Input('gestisciPS', 'n_clicks'), Input('inserisciPaz', 'n_clicks'), Input('inserisciMed', 'n_clicks'), Input('inserisciInf', 'n_clicks')]
)
def update(n_clicksGVS, n_clicksGPS, n_clicksIP, n_clicksIM, n_clicksII):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'gestisciVS':
            return gestisci_visita_seg
        elif button_id == 'gestisciPS':
            return gestisci_prestazione_seg
        elif button_id == 'inserisciPaz':
            return gestione_pazienti
        elif button_id == 'inserisciMed':
            return gestione_medici
        elif button_id == 'inserisciInf':  
            return gestione_infermieri

#Aggiornamento pagina nav medico segreteria
@app.callback(
    Output('contenuto-gestione-medico', 'children'),
    [Input('inserisci-medico-button', 'n_clicks'), Input('elimina-medico-button', 'n_clicks'), Input('sostituzione-medico-button', 'n_clicks')]
)
def update_pag(n_clicksINS, n_clicksDEL, n_clicksSOS):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'inserisci-medico-button':
        return inserisci_medico
    elif button_id == 'elimina-medico-button':
        return elimina_medici
    elif button_id == 'sostituzione-medico-button':
        return assenza_medico


#Aggiornamento pagina visualizzazione visite
@app.callback(
    Output('contenuto-gestione-visite-passate', 'children'),
    [Input('visua-visite-passate-button', 'n_clicks'), Input('visua-visite-minori-button', 'n_clicks')]
)
def update_pag(n_clicks1, n_clicks2):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'visua-visite-passate-button':
        return visualizza_visite
    elif button_id == 'visua-visite-minori-button':
        return visualizza_visite_minori


#Aggiornamento menu a tendina pazienti minori per visualizzazione visite
@app.callback(
    Output('paziente-minore-visua-visite-dropdown', 'options'),
    [Input('visua-visite-minori-button', 'n_clicks'), Input('user-store', 'data')]
)
def update(n_clicks, cred):
    user = cred['username']
    psw = cred['password']
    return seleziona_paziente_minore(utenti, pazienti, user, psw)


#Aggiornamento pagina visualizzazione prestazioni DA VEDERE
@app.callback(
    Output('contenuto-gestione-prestazioni-passate', 'children'),
    [Input('visua-prestazioni-passate-button', 'n_clicks'), Input('visua-prestazioni-minori-button', 'n_clicks')]
)
def update_pag(n_clicks1, n_clicks2):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'visua-prestazioni-passate-button': #DA GESTIRE IN BASE AL PAZIENTE, NON VOGLIO VISUALIZZARE TUTTI I CONTROLLI
        return visualizza_prestazioni
    elif button_id == 'visua-prestazioni-minori-button':
        return visualizza_prestazioni_minori


#Aggiornamento menu a tendina pazienti minori per visualizzarne le prestazioni DA RIVEDERE
@app.callback(
    Output('paziente-minore-visua-prestazioni-dropdown', 'options'),
    [Input('visua-prestazioni-minori-button', 'n_clicks'), Input('user-store', 'data')]
)
def update(n_clicks, cred):
    user = cred['username']
    psw = cred['password']
    return seleziona_paziente_minore(utenti, pazienti, user, psw)

#Cambio pagina nav infermieri segreteriaa
@app.callback(
    Output('contenuto-gestione-infermiere', 'children'),
    [Input('inserisci-infermiere-button', 'n_clicks'), Input('elimina-infermiere-button', 'n_clicks'), Input('servizio-infermiere-button', 'n_clicks')]
)
def update_pag(n_clicksin1, n_clicksdel2, n_clicks3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'inserisci-infermiere-button':
        return inserisci_infermiere
    elif button_id == 'elimina-infermiere-button':
        return elimina_infermieri
    elif button_id =='servizio-infermiere-button':
        return mostra_servizio

#Visualizzazione tabella di servizio
@app.callback(
    [Output('table-servizio', 'columns'), Output('table-servizio', 'data')],
    Input('date-servizio-dropdown', 'value')
)
def update(dataS):
    piano_servizio = show_servizi(servizi, date, infermieri, sale, dataS)
    if piano_servizio != None:
        piano = {'Cognome e Nome': piano_servizio[0], 'Sala':piano_servizio[1]}       
        df = pd.DataFrame(piano)
        colonne = [{"name": i, "id": i} for i in df.columns]
        dati = df.to_dict('records')
        return colonne, dati
    else:
        return [], []
        


#Cambio pagina nav paziente segreteria
@app.callback(
    Output('contenuto-gestione-paziente', 'children'),
    [Input('inserisci-paziente-button', 'n_clicks'), Input('elimina-paziente-button', 'n_clicks')]
)
def update_pag(n_clicksINS, n_clicksDEL):
    ctx = dash.callback_context

    if not ctx.triggered:
        return
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0] 

    if button_id == 'inserisci-paziente-button':
        return inserisci_paziente
    elif button_id == 'elimina-paziente-button':
        return elimina_pazienti


#Azioni segreteria

#Inserimento medico
@app.callback(
        Output('outputM', 'children'),
        Input('inserisciM-button', 'n_clicks'),
        [State('codice-fiscale', 'value'), State('nomeM', 'value'), State('cognomeM', 'value'), State('specialita', 'value')]

)
def return_result_insertM(n_clicksIns, cf, n, c, s):
    if n_clicksIns > 0:
        result = insert_med(medici, utenti, cf, n, c, s)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return inserisci_medico
    

#Inserimento infermiere
@app.callback(
        Output('outputI', 'children'),
        Input('inserisciI-button', 'n_clicks'),
        [State('codice-fiscale-inf', 'value'), State('nomeI', 'value'), State('cognomeI', 'value')]

)
def return_result_insertI(n_clicksInsInf, cf, n, c):
    if n_clicksInsInf > 0:
        result = insert_inf(infermieri, utenti, date, sale, servizi, cf, n, c)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return inserisci_infermiere


#Inserimento paziente
@app.callback(
        Output('outputP', 'children'),
        Input('inserisciP-button', 'n_clicks'),
        [State('nome', 'value'), State('cognome', 'value'), State('data-nascita', 'date'), State('luogo-nascita', 'value'), State('email', 'value'), State('responsabile', 'value'), State('medico-convenzionato', 'value')]

)
def return_result_insertP(n_clicks, nome, cognome, data, luogo, email, resp, medico):
    if n_clicks > 0:
        result = insert_paz(nome, cognome, data, luogo, email, resp, medico, medici, pazienti, utenti)
        return html.Div([result[0], html.Br(), html.Br(), result[1], html.Br(), result[2]], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return inserisci_paziente

#Visualizzazione mail responsabile per inserimento paziente minore
@app.callback(
    Output('email-responsabile', 'value'),
    Input('responsabile', 'value')
)
def update_mail(rvalue):
    if rvalue != None:
        return checkMail(rvalue, pazienti)
    else:
        return



#Eliminazione medico
@app.callback(
    Output('outputEliminazione', 'children'),
    Input('eliminaM-button', 'n_clicks'),
    State('medici-dropdown', 'value')
)
def update(n_clicks, med):
    if n_clicks > 0:
        result = elimina_med(medici, utenti, pazienti, sostituzioni, visite, date, controlli, med)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return elimina_medici

#Eliminazione infermiere
@app.callback(
    Output('outputEliminazioneInf', 'children'),
    Input('eliminaI-button', 'n_clicks'),
    State('infermieri-dropdown', 'value')
)
def update(n_clicks, inf):
    if n_clicks > 0:
        result = elimina_inf(infermieri, utenti, servizi, date, cure, prestazioni, inf)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return elimina_infermieri

#Eliminazione paziente
@app.callback(
    Output('outputEliminazionePaz', 'children'),
    Input('eliminaP-button', 'n_clicks'),
    State('pazienti-dropdown', 'value')
)
def update(n_clicks, p):
    if n_clicks > 0:
        result = elimina_paz(pazienti, utenti, controlli, cure, date, visite, prestazioni, p)
        return html.Div(result, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100%', 'width': '100%', 'margin-top':'20px', 'font-size':'20px', 'fontWeight': 'bold'}, className="p-4 shadow-lg rounded")
    else:
        return elimina_pazienti

#Aggiornamento dropdown paziente
@app.callback(
    Output('pazienti-dropdown', 'options'),
    [Input('elimina-paziente-button', 'n_clicks'), Input('eliminaP-button', 'n_clicks')]
)
def update(n_clicks1, n_clicks2):
    return seleziona_paziente(pazienti)


#Aggiornamento dropdown medico
@app.callback(
    Output('medici-dropdown', 'options'),
    [Input('elimina-medico-button', 'n_clicks'), Input('eliminaM-button', 'n_clicks')]
)
def update(n_clicks1, n_clicks2):
    return seleziona_medico(medici)


#Aggiornamento dropdown infermiere
@app.callback(
    Output('infermieri-dropdown', 'options'),
    [Input('elimina-infermiere-button', 'n_clicks'), Input('eliminaI-button', 'n_clicks')]
)
def update(n_clicks1, n_clicks2):
    return seleziona_infermiere(infermieri)



#Aggiornamento dropdown medici convenzionati
@app.callback(
    Output('medico-convenzionato', 'options'),
    Input('inserisci-paziente-button', 'n_clicks')
)
def update(n_clicks):
    return seleziona_medico(medici)

        
#Aggiornamento visbilità campi PAZIENTE
@app.callback(
    [
        Output('email', 'style'),
        Output('stileResp', 'style'),
        Output('email-responsabile', 'style'),
        Output('responsabile', 'options')
    ],
    [Input('data-nascita', 'date')]
)
def update_fields_visibility(date):
    if date:
        date_obj = dt.datetime.strptime(date, '%Y-%m-%d')
        threshold_date = dt.datetime(2010, 1, 1)
        if date_obj < threshold_date:
            return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, []
        else:
            return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}, seleziona_responsabile(pazienti)
    return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, []


app.layout = html.Div(
    [
        html.Div([login_layout], id='content', style={'height': '100%', 'width': '100%'}),
        dcc.Store(id='user-store')
    ]
)

if __name__ == "__main__":
    app.run(debug=True)