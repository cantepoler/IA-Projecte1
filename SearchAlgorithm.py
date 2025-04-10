    # This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1706732'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import Map, Path
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    result = []
    last = path.last
    if last in map.stations.keys():
        for vei, cost in map.connections[last].items():
            novaRuta = path.route + [vei]
            nouPath = Path(novaRuta)
            nouPath.update_g(path.g) #Actualitzem el cost del path
            result.append(nouPath)
    
    return result

def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    nova_llista = []
    path_actual = []
    for path in path_list:
        path_actual = path.route
        if len(path_actual) == len(set(path_actual)):     #Si hi ha elements repetits hi ha cicle
            nova_llista.append(path)
            
    return nova_llista


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    
    return expand_paths + list_of_path
    
    


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    result = [Path(origin_id)]        #Mirar de canviar la forma per no haver de crear un nou objecte
    while result:
        cap = result[0]
        if cap.last == destination_id:
            return cap
        expandir = expand(cap, map)
        expandir = remove_cycles(expandir)
        result = insert_depth_first_search(expandir, result[1:])
 
    print("No existeix solucio")
    return 1

def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths



def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    result = [Path(origin_id)]        #Mirar de canviar la forma per no haver de crear un nou objecte
    while result:
        cap = result[0]
        if cap.last == destination_id:
            return cap
        expandir = expand(cap, map)
        expandir = remove_cycles(expandir)
        result = insert_breadth_first_search(expandir, result[1:])
    print("No existeix solucio")
    return 1


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    result = []
    if(type_preference == 0):
        for path in expand_paths:
            path.update_g(1)
            result.append(path)
        
    elif(type_preference == 1):     #el temps ens ve donat dins de connections
        for path in expand_paths:
            ruta = path.route
            time = map.connections[ruta[-2]][ruta[-1]] #agafem el valor del diccionari connections corresponent al temps entre la penultima i ultima parada del path.
            path.update_g(time)
            result.append(path)

    
    elif(type_preference == 2):
        for path in expand_paths:
            ruta = path.route
            linia1 = map.stations[ruta[-2]]['line']
            linia2 = map.stations[ruta[-1]]['line']
            if linia1 == linia2:
                time = map.connections[ruta[-2]][ruta[-1]]
                velocity = map.velocity[linia1]
                distancia = time * velocity
                path.update_g(distancia)
            result.append(path)
      
    elif(type_preference == 3):
        for path in expand_paths:
            ruta = path.route
            linia1 = map.stations[ruta[-2]]['line']
            linia2 = map.stations[ruta[-1]]['line']
            if (linia1 != linia2):
                path.update_g(1)
            result.append(path)
        
    return result


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    for expandit in expand_paths:    
        for ind, element in enumerate(list_of_path):
            if expandit.g <  element.g:
                list_of_path.insert(ind, expandit)
                break
        else:
            list_of_path.append(expandit)
    return list_of_path


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    result = [Path(origin_id)]
    while result:
        cap = result[0]
        if cap.last == destination_id:
            return cap
        expandir = expand(cap, map)
        expandir = remove_cycles(expandir)
        expandir =calculate_cost(expandir, map, type_preference)
        result = insert_cost(expandir, result[1:])
 
    print("No existeix solucio")
    return 1
def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
    """
                            #0 - Adjacency          H: Si es l'objectiu h=0, si no h=1
                            #1 - minimum Time       H: h=euclidian_dist/vel_maxima
                            #2 - minimum Distance   H: h=euclidian_dist
                            #3 - minimum Transfers  H: Si linia_origen == linia_desti, h=0. Si no h=1
    """
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    result = []
    
    destinacio = map.stations[destination_id]
    coordsDestinacio = [destinacio['x'], destinacio['y']]
    
    if type_preference == 0:   #Adjacència
        for path in expand_paths:
            heuristica = 1
            if path.route[-1] == destination_id:
                heuristica = 0
            path.update_h(heuristica)
            result.append(path)
        
    elif type_preference == 1:      #Temps minim
        vel_maxima = max(map.velocity.values())
        
        for path in expand_paths:
            origen = map.stations[path.route[-1]]
            coordsOrigen = [origen['x'], origen['y']]
            heuristica = euclidean_dist(coordsOrigen, coordsDestinacio)/vel_maxima
            path.update_h(heuristica)
            result.append(path)
    
    elif type_preference == 2:     #Distancia minima
        for path in expand_paths:
            origen = map.stations[path.route[-1]]
            coordsOrigen = [origen['x'], origen['y']]
            heuristica = euclidean_dist(coordsOrigen, coordsDestinacio)
            path.update_h(heuristica)
            result.append(path)
      
    elif type_preference == 3:     #Transbords minims
        for path in expand_paths:
            heuristica = 1
            ruta = path.route
            linia1 = map.stations[ruta[-2]]['line']
            linia2 = map.stations[ruta[-1]]['line']
            if (linia1 == linia2):
                heuristica = 0
            path.update_h(heuristica)
            result.append(path)
        
    return result



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    result = []
    for path in expand_paths:
        path.update_f()
        result.append(path)
    return result

def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """
    for ind, path in enumerate(expand_paths):
        last = path.route[-1]
        if last in visited_stations_cost:
            if path.g < visited_stations_cost[last]:
                list_of_path = [Gpath for Gpath in list_of_path if last not in Gpath.route]     #Eliminem tots els paths de la llista global que continguin el node del que hem millorat el cost
                visited_stations_cost[last] = path.g
            else:
                expand_paths.pop(ind)
        else:
            visited_stations_cost[last] = path.g
            
    return expand_paths, list_of_path, visited_stations_cost
                    
    

def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    for path in expand_paths:
        for ind, Gpath in enumerate(list_of_path):
            if path.f < Gpath.f:
                list_of_path.insert(ind, path)
                break
        else:
            list_of_path.append(path)
    return list_of_path

def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    result = {}
    for clau, valor in map.stations.items():
        result[clau] = euclidean_dist([valor['x'], valor['y']], coord)  #Guardem distancia euclidiana de coord a totes les estacions
    return result

def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    
    list_of_path = [Path([origin_id])]
    visited_stations_cost = {}
    while list_of_path:
        cap = list_of_path[0]
        if cap.last == destination_id:
            return cap
        expanded_paths = expand(cap, map)
        expanded_paths = remove_cycles(expanded_paths)
        expanded_paths = calculate_cost(expanded_paths, map, type_preference)
        expanded_paths = calculate_heuristics(expanded_paths, map, destination_id, type_preference)
        expanded_paths = update_f(expanded_paths)

        expanded_paths, list_of_path, visited_stations_cost = remove_redundant_paths(expanded_paths, list_of_path, visited_stations_cost)        
        
        list_of_path = insert_cost_f(expanded_paths, list_of_path[1:])
    print("No existeix solucio")
    return None


def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    WVEL = 5
    
    map.add_station(0, "origen", 5, origin_coord[0], origin_coord[1])
    connections = map.connections
    connections[0] = {}
    for id_estacio in connections:
        if id_estacio != 0:
            coords_estacio = [map.stations[id_estacio]['x'], map.stations[id_estacio]['y']]
            temps = euclidean_dist(origin_coord, coords_estacio)/WVEL
            connections[id_estacio][0] = temps
            connections[0][id_estacio] = temps
    
    map.add_station(-1, "desti", 5, destination_coord[0], destination_coord[1])
    connections = map.connections
    connections[-1] = {}
    for id_estacio in connections:
        if id_estacio != -1:
            coords_estacio = [map.stations[id_estacio]['x'], map.stations[id_estacio]['y']]
            temps = euclidean_dist(destination_coord, coords_estacio)/WVEL
            connections[id_estacio][-1] = temps
            connections[-1][id_estacio] = temps
            
    connections[0][-1] = connections[-1][0]

    return Astar(0, -1, map, type_preference=1)