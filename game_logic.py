import geojson
from random import choice

with open('departements-version-simplifiee.geojson', mode='r') as file:
    geodata = geojson.load(file)
    file.close()


def get_dept_from_json_list(json_list):
    """ Retourn le nom du département """
    return json_list["properties"]["nom"]


def get_dept_list_init():
    with open('departements-version-simplifiee.geojson', mode='r') as tmp_file:
        tmp_geodata = geojson.load(tmp_file)
        tmp_file.close()
    """ Retourne la liste de tous les département à partir du JSON complet"""
    return [tmp_geodata["features"][i]["properties"]["nom"] for i in range(len(tmp_geodata["features"]))]


def remove_dept_from_list(dept_list, dept_to_remove):
    dept_list = dept_list.remove(dept_to_remove)
    return dept_list


def random_select_dept(with_replacement=False):
    """ Sélectionne un département au hasard dans la liste complète.
    Tirage sans remise de base """
    dept_list = get_dept_list_init()
    if with_replacement:
        return choice(dept_list)
    random_choice = choice(dept_list)



def assert_dept(dept_to_guess, actual_guess, nb_try):
    if dept_to_guess == actual_guess:
        return f"Tentatives restantes : {nb_try}"
    return f"Tentatives restantes : {nb_try-1}"

def try_until_failure(dept_to_guess, actual_guess, nb_try=3, n_try=1):
    if dept_to_guess == actual_guess:
        return f'Bravo vous avez trouvé en {n_try} coup'
    elif dept_to_guess != actual_guess or n_try < nb_try:
        n_try += 1
        try_until_failure(dept_to_guess, actual_guess, nb_try, n_try)
    else:
        return f"Comment on en est arrivé la"
