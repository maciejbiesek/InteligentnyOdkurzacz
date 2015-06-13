import cv2
import pygame, sys, time
from pygame.locals import *
import math
import NNTestData

import Sprite
import Player
import Tilemap

import Classification
import AStar


class Game():

    # konstruktor gry
    def __init__(self, textures, map, numtrash, neuralNetwork):
        # deklaracja mapy,gracza i obiektow
        self.map = map
        self.tilemap = Tilemap.Tilemap(textures, map, len(map[0]), len(map))
        self.player = Player.Player(3, 7, 'textures/roomba_down.png', 'textures/roomba_up.png',
                                    'textures/roomba_left.png', 'textures/roomba_right.png')
        self.trashbin = [5, 1]
        self.neuralNetwork = neuralNetwork
        self.trashTextures = {
            11: "textures/stain.png",
            12: "textures/dirt.png",
            13: "textures/can.png"
        }

        # tablica obiektow
        objectList = []
        objectList.append(Sprite.Sprite(7, 6, 'textures/tvset.png'))
        objectList.append(Sprite.Sprite(11, 2, 'textures/bookshelf1.png'))
        objectList.append(Sprite.Sprite(13, 2, 'textures/bookshelf1.png'))
        objectList.append(Sprite.Sprite(15, 2, 'textures/bookshelf2.png'))
        objectList.append(Sprite.Sprite(2, 3, 'textures/shelf1.png'))
        objectList.append(Sprite.Sprite(4, 3, 'textures/flower.png'))
        objectList.append(Sprite.Sprite(15, 9, 'textures/flower2.png'))
        objectList.append(Sprite.Sprite(15, 10, 'textures/flower2.png'))
        objectList.append(Sprite.Sprite(15, 11, 'textures/flower2.png'))
        objectList.append(Sprite.Sprite(3, 9, 'textures/sofa.png'))
        objectList.append(Sprite.Sprite(7, 9, 'textures/table.png'))
        objectList.append(Sprite.Sprite(1, 4, 'textures/kosz2.png'))
        self.objectList = objectList

        # czcionka
        pygame.font.init()
        self.INVFONT = pygame.font.Font('xxx.ttf', 18)

        # losowanie smieci
        self.numTrash1 = numtrash[0]
        self.numTrash2 = numtrash[1]
        self.numTrash3 = numtrash[2]
        self.numTrashTotal = sum(numtrash)

        self.trash_list = self.tilemap.create_trash(self.numTrash1, self.numTrash2, self.numTrash3)

        # stworzenie drzewa decyzyjnego
        self.classification = Classification.Classification("trainingset")

        # rozpocznij gre
        pygame.init()

        # wyswietl okno gry
        width = self.tilemap.mapwidth * self.tilemap.tilesize
        height = self.tilemap.mapheight * self.tilemap.tilesize + 200
        self.DISPLAYSURF = pygame.display.set_mode([width, height])

        # algorytm genetyczny
        self.generation = 0
        self.evaluated_player = 0
        self.population_size = 0
        self.best_fitness = 0
        self.best_capacity = 0


    # wyswietlanie i odswiezanie okna gry


    def display(self, pregen=None):



        # rysowanie mapy
        for row in range(self.tilemap.mapheight):
            for column in range(self.tilemap.mapwidth):
                # rysuj w okreslonym miejscu okreslony typ kafelka/obiektu
                self.DISPLAYSURF.blit(self.tilemap.textures[self.tilemap.matrix[row][column]],
                                      (column * self.tilemap.tilesize, row * self.tilemap.tilesize))

        # rysowanie gracza
        icon = pygame.image.load(self.player.image).convert_alpha()
        self.DISPLAYSURF.blit(icon, (self.player.x * self.tilemap.tilesize, self.player.y * self.tilemap.tilesize))

        # rysowanie wszystkich obiektow
        for i in range(len(self.objectList)):
            icon = pygame.image.load(self.objectList[i].image).convert_alpha()
            # rysuj w okreslonym miejscu okreslony obiekt z listy

            self.DISPLAYSURF.blit(icon, (
                self.objectList[i].x * self.tilemap.tilesize, self.objectList[i].y * self.tilemap.tilesize))

        pygame.draw.rect(self.DISPLAYSURF, pygame.Color('black'),
                         (0, self.tilemap.mapheight * self.tilemap.tilesize, 400, 200))


        # wyswietlanie potrzebnych informacji
        self.DISPLAYSURF.blit(pygame.image.load('textures/dirt.png'),
                              (10, self.tilemap.mapheight * self.tilemap.tilesize + 10))
        textObj1 = self.INVFONT.render(str(self.player.equipment["dirt"]), True, (255, 255, 255), (0, 0, 0))
        self.DISPLAYSURF.blit(textObj1, (40, self.tilemap.mapheight * self.tilemap.tilesize + 10))

        self.DISPLAYSURF.blit(pygame.image.load('textures/can.png'),
                              (80, self.tilemap.mapheight * self.tilemap.tilesize + 10))
        textObj2 = self.INVFONT.render(str(self.player.equipment["can"]), True, (255, 255, 255), (0, 0, 0))
        self.DISPLAYSURF.blit(textObj2, (110, self.tilemap.mapheight * self.tilemap.tilesize + 10))

        self.DISPLAYSURF.blit(pygame.image.load('textures/stain.png'),
                              (160, self.tilemap.mapheight * self.tilemap.tilesize + 10))
        textObj3 = self.INVFONT.render(str(self.player.equipment["stain"]), True, (255, 255, 255), (0, 0, 0))
        self.DISPLAYSURF.blit(textObj3, (190, self.tilemap.mapheight * self.tilemap.tilesize + 10))

        textObj4 = self.INVFONT.render("Points: " + str(self.player.points), True, (255, 255, 255), (0, 0, 0,))
        self.DISPLAYSURF.blit(textObj4, (310, self.tilemap.mapheight * self.tilemap.tilesize + 10))

        # wypisywanie do genetyka
        textObj5 = self.INVFONT.render("Generation: " + str(self.generation), True, (255, 255, 255), (0, 0, 0,))
        self.DISPLAYSURF.blit(textObj5, (10, self.tilemap.mapheight * self.tilemap.tilesize + 50))

        textObj6 = self.INVFONT.render(
            "Evaluating: " + str(self.evaluated_player + 1) + " / " + str(self.population_size), True, (255, 255, 255),
            (0, 0, 0,))
        self.DISPLAYSURF.blit(textObj6, (10, self.tilemap.mapheight * self.tilemap.tilesize + 80))

        textObj7 = self.INVFONT.render(
            "Best fitness: " + str(self.best_fitness) + "  (" + str(self.best_capacity) + ")", True, (255, 255, 255),
            (0, 0, 0,))
        self.DISPLAYSURF.blit(textObj7, (10, self.tilemap.mapheight * self.tilemap.tilesize + 110))

        textObj8 = self.INVFONT.render("Capacity: " + str(self.player.capacity), True, (255, 255, 255), (0, 0, 0,))
        self.DISPLAYSURF.blit(textObj8, (10, self.tilemap.mapheight * self.tilemap.tilesize + 140))


      #  print self.generation
       # print pregen
        # if self.generation != pregen:
        #     pregen = self.generation
        #     print "Generation: " + str(self.generation)
        # print "Evaluating: " + str(self.evaluated_player + 1) + " / " + str(self.population_size)



        # odswiezanie widoku
        pygame.display.update()

    # funkcja obliczajaca odleglosc
    def distance(self, target):
        return abs(self.player.y - target[0]) + abs(self.player.x - target[1])

    def cleaning(self):
        # sprzatanie plam

        test = NNTestData.NNTestData(cv2.imread(self.trashTextures[self.tilemap.matrix[self.player.y][self.player.x]]))
        test.prepareTestData()
        outputString = self.neuralNetwork.testNetwork(test)
        print "Decyzja: " + outputString

        self.tilemap.matrix[self.player.y][self.player.x] = 1
        if outputString == "stain":
            points = 3
        elif outputString == "dirt":
            points = 1
        else:
            points = 2
        self.player.clean(outputString, points)

    def evaluatePlayer(self, player):
        self.player = player
        self.player.route_length = 0

        if len(self.trash_list) < self.numTrashTotal:
            self.trash_list = self.tilemap.create_trash(self.numTrash1, self.numTrash2, self.numTrash3)

        while True:
            if self.update() == "finished":
                break

        fitness = 10000.0 / (self.player.route_length * (self.player.capacity + 1000))

        if fitness > self.best_fitness:
            self.best_fitness = fitness
        self.best_capacity = self.player.capacity
        return fitness

    def update(self):
        # output = self.handle_events()
        path1 = []

        self.display()

        if self.player.cleaned >= self.numTrashTotal and [self.player.y, self.player.x] == self.trashbin:
            return "finished"

        go_to_trash = True

        if self.player.sumEquipment() < self.player.capacity:
            # klasyfikacja i podjecie decyzji
            decisions = self.classification.classify(self.trash_list, self)

            any_decision = False

            decisions_sorted = []
            for i in range(len(decisions)):
                distance = self.distance(self.trash_list[i])
                decisions_sorted.append([distance, i])
                if decisions[i] == 'True':
                    any_decision = True

            decisions_sorted.sort()

            if any_decision == False and self.player.sumEquipment() == 0:
                if len(self.trash_list) > 0:
                    decisions[decisions_sorted[0][1]] = 'True'

            for j in range(len(decisions)):
                i = decisions_sorted[j][1]
                if decisions[i] == 'True':
                    # utworz instancje AStar
                    a = AStar.AStar()
                    a.init_grid(self.map)
                    # wezel poczatowy
                    start = (self.player.y, self.player.x)
                    # droga od wezla poczatkowego do docelowego
                    path = a.process(start, self.trash_list[i][0], self.trash_list[i][1])
                    # ciag akcji agenta od stanu poczatkowego do docelowego
                    path1 = AStar.get_actions(path, start, self.trash_list[i][0], self.trash_list[i][1])
                    # kolejne wykonanie akcji
                    for j in range(len(path1)):
                        self.player.move(path1[j])
                        self.display()
                        # time.sleep(0.1)
                    self.cleaning()
                    self.trash_list.pop(i)
                    go_to_trash = False
                    break

        if go_to_trash:
            # utworz instancje AStar
            a = AStar.AStar()
            a.init_grid(self.map)
            start = (self.player.y, self.player.x)
            # najkrotsza droga do smietnika
            path = a.process(start, self.trashbin[0], self.trashbin[1])
            # ciag akcji agenta od stanu poczatkowego do docelowego (pole obok smietnika)
            path1 = AStar.get_actions(path, start, self.trashbin[0], self.trashbin[1])

            # kolejne wykonanie akcji
            for i in range(len(path1)):
                self.player.move(path1[i])
                self.display()
                # time.sleep(0.1)

            # oproznianie ekwipunku
            for key in self.player.equipment.keys():
                self.player.equipment[key] = 0
                self.display()
                # time.sleep(0.1)

        return "working"


'''
    #funkcja obslugujaca zdarzenia w grze
    #def handle_events(self):
        #for event in pygame.event.get():
            #wyjscie
            if event.type == QUIT:
                #zakoncz gre i zamknij okno
                pygame.quit()
                sys.exit()
            #klawisze - poruszanie graczem
            elif event.type == KEYDOWN:
                #poruszanie w prawo
                if (event.key == K_RIGHT):
                    self.player.image = self.player.texture_right
                    if (self.player.collision(self.tilemap,'right')):
                        #zmiana pozycji x gracza
                        self.player.move('right')
                    
                #poruszanie w lewo
                elif (event.key == K_LEFT):
                    self.player.image = self.player.texture_left
                    if (self.player.collision(self.tilemap,'left')):
                        #zmiana pozycji x gracza
                        self.player.move('left')
                                     
                #poruszenie w dol
                elif (event.key == K_DOWN):
                    self.player.image = self.player.texture_down
                    if (self.player.collision(self.tilemap,'down')):
                        #zmiana pozycji y gracza
                        self.player.move('down')
                                       
                #poruszenie w gore
                elif (event.key == K_UP):
                    self.player.image = self.player.texture_up
                    if (self.player.collision(self.tilemap,'up')):
                        #zmiana pozycji y gracza
                        self.player.move('up')

                #sprzatanie plam
                elif (event.key == K_p):
                   if self.tilemap.matrix[self.player.y][self.player.x] == 11:
                       self.tilemap.matrix[self.player.y][self.player.x] = 1
                       self.player.equipment[0] += 1
                       print(self.player.equipment)

                #sprzatanie kurzu
                elif (event.key == K_k):
                   if self.tilemap.matrix[self.player.y][self.player.x] == 12:
                       self.tilemap.matrix[self.player.y][self.player.x] = 1
                       self.player.equipment[2] += 1
                       print(self.player.equipment)

                #sprzatanie puszek
                elif (event.key == K_o):
                   if self.tilemap.matrix[self.player.y][self.player.x] == 13:
                       self.tilemap.matrix[self.player.y][self.player.x] = 1
                       self.player.equipment[1] += 1
                       print(self.player.equipment)
'''
