from math import *
import pandas as pd
import numpy as np
from time import time
from getSQL import *

WriteData()

ratingDf=pd.read_csv("tempRating.csv")
moviesDf=pd.read_csv("tempMovie.csv")
users=dict()

arr=np.array(ratingDf.iloc[:,])
arrMov=np.array(moviesDf.iloc[:,])


#diccionario de rating
for i in arr:
    userId, movieId = int(float(i[0])), int(float(i[1]))
    rating = float(i[2])
    if userId not in users:
        users[userId] = {movieId: rating}
    else:
        users[userId][movieId] = rating

movies=dict()
#diccionario de peliculas
for i in arrMov:
    movieId = int(i[0])
    movieTitle = i[1]
    movies[movieId] = movieTitle

## DIstancias
def cosine(dicc1, dicc2):
    xy = 0
    xx = 0
    yy = 0
    ing = True

    for i in dicc1:
        if i in dicc2:
            xy = xy + dicc1[i] * dicc2[i]
            xx = xx + dicc1[i] * dicc1[i]
            yy = yy + dicc2[i] * dicc2[i]
            ing = False

    if xx == 0 or yy == 0 or ing:
        ang = -100
    else:
        ang = xy / (sqrt(xx) * sqrt(yy))
    return ang


def pearson(dicc1, dicc2):
    xy = 0
    x = 0
    y = 0
    xx = 0
    yy = 0
    n = 0

    for i in dicc1:
        if i in dicc2:
            n = n + 1
            xy = xy + dicc1[i] * dicc2[i]
            x = x + dicc1[i]
            y = y + dicc2[i]
            xx = xx + dicc1[i] * dicc1[i]
            yy = yy + dicc2[i] * dicc2[i]

    if n == 0:
        r = -100
    else:
        if sqrt(xx - (x * x / n)) == 0 or sqrt(yy - (y * y / n)) == 0:
            r = -1
        else:
            r = (xy - ((x * y) / n)) / (sqrt(xx - (x * x / n)) * sqrt(yy - (y * y / n)))
    return r

def manhathan(dicc1, dicc2):
    distance = 0.0
    ing=True
    for i in dicc1:
        if i in dicc2:
            distance = distance + abs(dicc1[i] - dicc2[i])
            ing=False
    if ing:
        return -100
    else:
        return distance

def euclidean(dicc1, dicc2):
    distance = 0.0
    ing=True
    for i in dicc1:
        if i in dicc2:
            distance += (dicc1[i] - dicc2[i])**2
            ing=False
    if ing:
        return -100
    else:
        return sqrt(distance)

#se encarga de buscar los vecinos de manera ordenada, para seleccionar k vecinos
def get_neighbors(users,id_test,distancia):
    distances = list()
    for i in users:
        #evitar comparar con el mismo
        if (i!=id_test):

            dist = distancia(users[i],users[id_test])
            #si la distancia es valida
            if dist!=-100:
                distances.append((i,dist))
    distances.sort(key=lambda tup: tup[1])
    return distances


def knn(result, users, persona, vecinos, distancia, umbral):
    # halla los vecinos
    neighbors = get_neighbors(users, persona, distancia)
    contador = 0

    # si es metrica de distancia a menor valor mejor
    if distancia == euclidean or distancia == manhathan:
        for i in range(len(users.keys())):
            # if neighbors[i][1]>umbral:
            print("id: " + str(neighbors[i][0] + 1) + " distancia: " + str(neighbors[i][1]))
            result[neighbors[i][0] + 1] = neighbors[i][1]
            contador = contador + 1
            if contador == vecinos:
                break

    # si es correlacion si el valor es mayor cercano a 1 mejor
    else:
        for i in range(len(users.keys())):
            # if neighbors[i][1]>umbral:
            print("id: " + str(neighbors[len(neighbors) - i - 1][0] + 1) + " distancia: " + str(
                neighbors[len(neighbors) - i - 1][1]))
            result[neighbors[len(neighbors) - i - 1][0] + 1] = neighbors[len(neighbors) - i - 1][1]
            contador = contador + 1
            if contador == vecinos:
                break



def knn(result, users, persona, vecinos, distancia, umbral):
    neighbors = get_neighbors(users, persona, distancia)
    contador = 0

    # euclidean  manhathan  pearson  cosine
    if distancia == euclidean or distancia == manhathan:
        for i in range(len(users.keys())):
            # if neighbors[i][1]>umbral:
            result[neighbors[i][0] ] = neighbors[i][1]
            contador = contador + 1
            if contador == vecinos:
                break
    else:
        for i in range(len(users.keys())):
            # if neighbors[i][1]>umbral:
            result[neighbors[len(neighbors) - i - 1][0]] = neighbors[len(neighbors) - i - 1][1]
            contador = contador + 1
            if contador == vecinos:
                break

def getRecomendations(id,vecinos_num,umbral = 0):
    persona = id
    vecinos = vecinos_num
    umbral = 0

    sendData = []
    result=dict()
    knn(result,users,persona,vecinos,euclidean,umbral)
    result = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    sendData.append(result)

    result=dict()
    knn(result,users,persona,vecinos,manhathan,umbral)
    result = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    sendData.append(result)

    result=dict()
    knn(result,users,persona,vecinos,pearson,umbral)
    result = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    sendData.append(result)

    result=dict()
    knn(result,users,persona,vecinos,cosine,umbral)
    result = dict(sorted(result.items(), key=lambda item: item[1],reverse=True))
    sendData.append(result)


    return  sendData
