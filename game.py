import dash_leaflet as dl
from dash import Dash, html, callback, Output, Input, State, ctx
from dash_extensions.javascript import arrow_function
from game_logic import *

dept_list = list
reset_dept_selec, game_started = False, False

app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children=["Quizz des départements français"],
            style={'textAlign': 'center',
                   'font-weight': 'bold',
                   'font-family': 'Calibri',
                   'font-size': 40}),
    # Boutton de changement de département
    html.Button(children=['Choisir un département'], id='dept_button',
                n_clicks=0),
    html.Button(children='Supprimer', id='delete_button',
                n_clicks=0),
    # Regroupe le département à trouver, et le compteur de tentatives
    html.Div(children=[
        html.Div(children=['Ou se situe le : '], id='dept_to_found',
                 style={'font-family': 'calibri',
                        'font-weight': 'bold'}),
        # Compteur de tentatives
        html.Div(children=['Tentatives restantes : 3'], id='tenta_rest',
                 style={'textAlign': 'end',
                        'font-family': 'calibri',
                        'font-weight': 'bold'})

    ]),
    # Carte du monde avec les frontières des départements
    dl.Map(center=[46.5, 2], zoom=5, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geodata, id='geodata',
                   hoverStyle=arrow_function(dict(weight=3, color='#333', dashArray='')),
                   n_clicks=0)
    ],  style={'height': '50vh'}),
    # Affiche le département sur lequel on a cliqué
    html.Div(children=[], id='selected_dept',
             style={'font-family': 'calibri'}),
    # Booléen de la comparaison entre le dept a trouver et celui choisi
    html.Div(children=[], id='assert_dept',
             style={'font-family': 'calibri'}),
    # compteur de départements restants
    html.Div(children=[], id='n_dept_remaining',
             style={'font-family': 'calibri'}),
])


@callback(
    Output(component_id='dept_button', component_property='children'),
    Input(component_id='dept_button', component_property='n_clicks'),
    Input(component_id='dept_button',component_property='children')
)
def start_game(n_click, content):
    global dept_list, reset_dept_selec

    if n_click == 0:
        dept_list = get_dept_list_init()
        return 'Choisir un département'

    elif len(dept_list) == 0:
        return 'Fin du jeu'

    else:
        if game_started:
            reset_dept_selec = True
        return 'Changer de département'

# DEBUT CODE TEMPORAIRE
@callback(
    Output(component_id='delete_button', component_property='children'),
    Input(component_id='dept_to_found', component_property='children'),
    Input(component_id='delete_button', component_property='n_clicks')
)
def on_click_remove(dept_to_found, delete_button):
    global dept_list

    if type(dept_to_found) is list or dept_to_found == "Cliquez sur commencer le jeu"\
            or dept_to_found == 'Ou se situe le :':
        return "Jeu non initialisé"

    elif ctx.triggered_id == 'delete_button':
        remove_dept_from_list(dept_list, dept_to_found)
        return 'Supprimer'

    else:
        return 'Supprimer'
# FIN CODE TEMPORAIRE


@callback(
    Output(component_id='dept_to_found', component_property='children', allow_duplicate=True),
    Output(component_id='n_dept_remaining', component_property='children'),
    Input(component_id='dept_button', component_property='n_clicks'),
    Input(component_id='assert_dept', component_property='children'),
    Input(component_id='dept_to_found', component_property='children'),
    Input(component_id='tenta_rest', component_property='children'),
    Input(component_id='delete_button', component_property='n_clicks'),
    prevent_initial_call=True
)
def on_click_found_dept(n_click_btn, assert_rslt, current_dept, tenta_rest, delete_button):
    global dept_list

    if type(tenta_rest) is list:
        tenta_rest = tenta_rest[0]
    n_tenta_rest = int(tenta_rest[-1:])

    # Ne s'éxécute pas si la dept_list ne contient pas les départements
    if not (type(dept_list) is type):
        if len(dept_list) != 0:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

            dept = choice(dept_list)

            # print(f"----------\n{len(dept_list)}") check len dept list
            if trigger_id == 'dept_button':
                if n_click_btn > 0:
                    return dept, f"{len(dept_list)}"
                elif n_click_btn == 0:
                    return "Le jeu n'a pas commencer", f"{len(dept_list)}"
                else:
                    return "Aucun département choisi", f"{len(dept_list)}"

            elif trigger_id == 'assert_dept' and len(dept_list) != 0:
                # Si on a trouver ou qu'on n'a plus de tentatives
                if assert_rslt in ['Bonne réponse', '3 Échecs, département suivant']:
                    return dept, f"{len(dept_list)}"
                # Si on a mauvais ou qu'on
                elif 'Mauvaise réponse' in assert_rslt or 'Veuillez selectionner' in assert_rslt:
                    return f"{current_dept}", f"{len(dept_list)}"
                # Le jeu n'a pas été lancé, il faut cliquer sur le bouton
                else:
                    return "Cliquez sur choisir un departement", ""
            # DEBUT CODE TEMPORAIRE
            elif trigger_id == 'delete_button':
                print('Triggered delete button')
                return dept, f"{len(dept_list)}"
            # FIN CODE TEMPORAIRE

        else:
            return "Fin du jeu", f"{len(dept_list)}"


@callback(
    Output(component_id="selected_dept", component_property="children"),
    Input(component_id="geodata", component_property="clickData"),
)
def dept_click(dept_clicked):
    """ dept_clicked is a JSON list with all atributes """
    if dept_clicked:
        return f"Département sélectionné : {get_dept_from_json_list(dept_clicked)}"
    else:
        return "Aucun département sélectionné"


@callback(
    Output(component_id='assert_dept', component_property='children'),
    Output(component_id='tenta_rest', component_property='children', allow_duplicate=True),
    Input(component_id='dept_to_found', component_property='children'),
    Input(component_id='geodata', component_property='clickData'),
    Input(component_id='tenta_rest', component_property='children'),
    prevent_initial_call=True
)
def recount_tenta(dept_to_chose, dept_chosen, tenta_rest):
    global dept_list, reset_dept_selec, game_started

    if type(dept_to_chose) is list or dept_to_chose == "Cliquez sur commencer le jeu":
        return "Veuillez cliquer sur choisir un département", "Tentatives restantes : 3"

    if type(tenta_rest) is list:
        tenta_rest = tenta_rest[0]
    n_tenta_rest = int(tenta_rest[-1:])

    # Si on a pas cliqué sur un département encore
    if not dept_chosen:
        return "Le jeu n'a pas commencé", f"Tentatives restantes : {n_tenta_rest}"

    # SI on a cliqué et qu'il reste des département dans la liste
    elif dept_chosen and len(dept_list) != 0:
        game_started = True
        dept_chosen = get_dept_from_json_list(dept_chosen)

        if not reset_dept_selec:

            if dept_to_chose == dept_chosen:
                remove_dept_from_list(dept_list, dept_to_chose)
                return "Bonne réponse", "Tentatives restantes : 3"
            else:
                if n_tenta_rest > 1:
                    answ = "Bonne réponse" if dept_to_chose == dept_chosen else "Mauvaise réponse"
                    return f"{answ}", f"{assert_dept(dept_to_chose, dept_chosen, n_tenta_rest)}"
                else:
                    remove_dept_from_list(dept_list, dept_to_chose)
                    return f"3 Échecs, département suivant", "Tentatives restantes : 3"
        else:
            reset_dept_selec = False
            return "Veuillez selectionner un département", "Tentatives restantes : 3"

    # Cas quand il ne reste plus qu'un département à trouver
    # WIP
    elif len(dept_list) == 0 and n_tenta_rest >= 1:
        return f"{dept_to_chose == dept_chosen}", f"{assert_dept(dept_to_chose, dept_chosen, n_tenta_rest)}"

    else:
        return f"Tous les départements ont été joués", "Fin du jeu"


if __name__ == '__main__':
    app.run(debug=True)
