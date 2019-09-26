from typing import List, Tuple
from math import sqrt
from random import randint, random
from copy import copy
from yaml import load, dump, Loader, Dumper
from pdb import set_trace

# La lista de ciudades. Cada ciudad está representada por un nombre y sus
# coordenadas, una tupla de floats.
Ciudades = List[Tuple[str, Tuple[float, float]]]

# La matriz de distancias, que representa un grafo completo con las distancias
# calculadas entre las ciudades.
Distancias = List[List[float]]

# La matriz que contiene la cantidad de feromona en cada camino del grafo.
Feromonas = List[List[float]]

# La lista de ciudades, esta vez según su índice en la lista.
Indices = List[int]


def calcProb(i: int,  # ciudad de origen.
             js: List[int],  # ciudad de destino.
             distancias: Distancias,
             feromonas: Feromonas,
             facDst: float=0.8,
             facFrm: float=0.8) -> List[float]:
    """
    Calcula la probabilidad de que una hormiga, estando en un nodo i,
    vaya a cualquiera de los nodos aún no visitados.
    """
    # calcula los valores
    vals = [
        ((1/distancias[i][j])**facDst) * (feromonas[i][j]**facFrm)
        for j in js
    ]
    # el total de estos valores
    total1 = sum(vals)

    # probabilidad de cada valor
    probs3 = [
        x/total1
        for x in vals
    ]

    # generando lista de valores acumulados
    acumulado = 0.0
    probs4 = []
    for val in probs3:
        acumulado += val
        probs4.append(acumulado)
    return probs4


def calcCost(ruta: Indices, distancias: Distancias) -> float:
    """
    calcula el costo de una ruta particular.
    """
    costo = 0.0
    for i in range(0, len(ruta)):
        costo = costo + distancias[ruta[i - 1]][ruta[i]]
    return costo


def changeFero(ferom: Feromonas,
               ruta: Indices,
               dists: Distancias) -> None:
    """
    a partir del recorrido de una hormiga, deposita feromona en los
    caminos utilizados.
    """
    # ahora se calcula la longitud de la ruta.
    costo = calcCost(ruta, dists)
    # a cada uno de los tramos de la ruta, se le añade la correspondiente
    # feromona.
    for i in range(0, len(ruta)):
        ferom[ruta[i - 1]][ruta[i]] += 1/costo


def evaporar(ferom: Feromonas, evap_param: float) -> None:
    """
    reduce la cantidad de feromona en el mapa, en una proporción determinada.
    """
    for x in ferom:
        for y in x:
            y = y * evap_param


def hormiga(ferom: Feromonas,
            dists: Distancias,
            first: int,
            fac_dist: float,
            fac_ferom: float) -> None:
    """
    ciclo principal del algoritmo.
    envía una hormiga a recorrer el grafo, pasando una sola vez por cada nodo.
    La hormiga decide a dónde ir después de forma probabilística.
    """
    # se crea una variable para almacenar la ciudad actual.
    # se inicializa con un parámetro.
    ciudad = first
    # se hace una lista con las ciudades.
    # se elimina la inicial.
    indices = list(range(0, len(dists)))
    indices = indices[:ciudad] + indices[(ciudad + 1):]
    # y una lista vacía con la ruta
    ruta: Indices = []
    # mientras halla elementos en la lista de indices:
    while(len(indices) > 0):
        # se genera un número aleatorio
        rand = random()
        # se calculan las probabilidades de escoger cualquiera de las ciudades
        # restantes en la lista.
        listProb = calcProb(ciudad, indices, dists, ferom, fac_dist, fac_ferom)
        i = 0
        # por cada elemento en las probabilidades:
        for prob in listProb:
            # si el valor aleatorio es menor, se escoge la ciudad de la lista,
            # y se termina la ejecución.
            if rand < prob:
                ruta.append(indices[i])
                del indices[i]
                break
            # de otro modo, se pasa a la siguiente ciudad en la lista.
            i += 1
    # una vez se tiene la ruta, se procede a añadir la feromona a los
    # respectivos sitios.
    changeFero(ferom, ruta, dists)


def bestPath(first: int,
             ferom: Feromonas) -> Indices:
    """
    selecciona el mejor camino basado en la cantidad de feromona.
    """
    ruta: Indices = []
    # lista que contiene todos los índices.
    indices = list(range(0, len(ferom[0])))
    # se elimina el inicial.
    indices = indices[:first] + indices[(first + 1):]
    # y se añade al principio de la ruta.
    ruta.append(first)
    # la ciudad actual.
    current = first
    # mientras queden índices:
    while(len(indices) > 0):
        # set_trace()
        # se selecciona el camino con la mayor cantidad de feromona
        # de la tabla.
        mayorFeromona = max([ferom[current][j] for j in indices])
        mejorCamino = ferom[current].index(mayorFeromona)
        ruta.append(mejorCamino)
        current = mejorCamino
        del indices[indices.index(mejorCamino)]
    return ruta


# import main as m; (distancias, feromonas) = m.calcMatrices(m.parseFile("cities2")); m.exploracion(20, [0,1,2,3], distancias, feromonas); m.bestPath(0, feromonas)


def exploracion(numEx: int,
                ciudades: Indices,
                dists: Distancias,
                ferom: Feromonas) -> None:
    """
    recorre el mapa varias veces, aleatoriamente, para darle valores
    iniciales a todos los caminos.
    Adicionalmente, añade la feromona respectiva.
    """
    # variable que con
    # número de veces.
    # set_trace()
    for times in range(0, numEx):
        # se copia la lista de índices de ciudades.
        ciudades2 = copy(ciudades)
        # se crea una variable temporal para guardar la ruta.
        # estas no se conservan más allá del ciclo.
        ruta = []
        # mientras la lista de índices tenga elementos:
        while(len(ciudades2) > 0):
            # tomar un elemento entre 0 y el tamaño de ciudades2.
            numb = randint(0, len(ciudades2) - 1)
            # se añade este elemento a nueva ruta.
            ruta.append(ciudades2[numb])
            # se elimina de la lista.
            ciudades2 = ciudades2[:numb] + ciudades2[(numb + 1):]
        # se cambia la cantidad de feromona.
        changeFero(ferom, ruta, dists)


# DONE: generar tanto distancias como feromonas acá
def calcMatrices(ciudades: Ciudades) -> Tuple[Distancias, Feromonas]:
    """
    a partir de la lista de ciudades, calcula las distancias entre ellas.
    También genera la matriz de feromonas inicial.
    """
    distancias: Distancias = []
    feromonas: Feromonas = []
    for cty in ciudades:
        distanceRow = []
        feromoneRow = []
        for ciudad in ciudades:
            distanceRow.append(sqrt((cty[1][0] - ciudad[1][0])**2
                                    + (cty[1][1] - ciudad[1][1])**2))
            feromoneRow.append(0.0)
        distancias.append(distanceRow)
        feromonas.append(feromoneRow)
    return (distancias, feromonas)


def parseFile(filename: str) -> Ciudades:
    """
    lee el archivo y pasa sus contenidos a la variable ciudades.
    """
    ciudades: Ciudades = []
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        values = line.split(" ")
        ciudades.append((values[0], (float(values[1]), float(values[2]))))
    return ciudades


if __name__ == "__main__":
    print("Bienvenido al programa.")
    filename = input("Por favor ingrese el nombre del archivo en que se "
                     "encuentran las ciudades: ")
    firstName = input("Cuál de estas ciudades va a ser el punto de partida? ")
    with open('params.yaml', 'r') as file:
        config = load(file, Loader=Loader)

    ciudades = parseFile(filename)
    first = 0
    indx = 0
    for ciudad in ciudades:
        if ciudad[0] == firstName:
            first = indx
            break
        indx += 1

    (distances, feromones) = calcMatrices(ciudades)
    exploracion(config["explorer_ants"],
                [i for i in range(0, len(ciudades))], distances, feromones)
    print("el costo de la ruta inicial es: ",
          calcCost(bestPath(first, feromones), distances))
    for x in range(0, config["number_of_ants"]):
        hormiga(feromones, distances, first, config["visibility_weight"],
                config["feromone_weight"])
        evaporar(feromones, config["feromone_evaporation"])
    camino = bestPath(first, feromones)
    print("El mejor camino ha sido calculado.\n")
    listaNombres = [ciudades[i][0] for i in camino]
    print(listaNombres)
    print("el costo de la ruta es:", calcCost(camino, distances))
