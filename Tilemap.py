import random
from random import shuffle


class Tilemap:
    # konstruktor mapy
    def __init__(self, textures, matrix, mapwidth, mapheight):
        self.textures = textures  # lista tekstur
        self.matrix = matrix  # lista reprezentujaca mape
        self.tilesize = 23  # rozmiar pojedynczego kafelka
        self.mapwidth = mapwidth  # szerokosc mapy
        self.mapheight = mapheight  # wysokosc mapy

    # funkcja losujaca smieci
    def create_trash(self, x, y, z):
        # lista pomocnicza przechowujaca wolne miejsca
        trashPlaces = []
        # epicka lista do zwrotu
        trashPlacesWow = []
        # przejdz przez cala mape w poszukiwaniu wolnych miejsc

        for row in range(self.mapheight):
            for column in range(self.mapwidth):
                # wolne miejsce
                if self.matrix[row][column] == 1:
                    trashPlaces.append([row, column])

        # losowa permutacja listy pomocniczej
        random.shuffle(trashPlaces, random.random)

        # umieszczanie smieci w odpowiedniej ilosci na mapie
        for i in range(x):
            self.matrix[trashPlaces[i][0]][trashPlaces[i][1]] = 11
        for i in range(x + 1, x + y + 1):
            self.matrix[trashPlaces[i][0]][trashPlaces[i][1]] = 12
        for i in range(x + y + 2, x + y + 2 + z):
            self.matrix[trashPlaces[i][0]][trashPlaces[i][1]] = 13

        # przekazywanie informacji o smieciach (y,x,l.punktow)
        for i in range(x):
            trashPlacesWow.append([trashPlaces[i][0], trashPlaces[i][1], 2])
        for i in range(x + 1, x + y + 1):
            trashPlacesWow.append([trashPlaces[i][0], trashPlaces[i][1], 1])
        for i in range(x + y + 2, x + y + 2 + z):
            trashPlacesWow.append([trashPlaces[i][0], trashPlaces[i][1], 3])

        return trashPlacesWow
