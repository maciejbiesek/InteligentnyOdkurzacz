import heapq


def get_walls(matrix):
    """
    przeszukuje mape gry w celu znalezienia scian - stanow nieosiagalnych
    """
    walls = []
    limits = [0, 2, 3, 4, 5]
    for x in range(len(matrix[0])):
        for y in range(len(matrix)):
            if matrix[y][x] in limits:
                walls.append((y, x))
    return walls


class Node(object):
    def __init__(self, x, y, reachable):
        """
        Inicjalizuje nowy wezel dla danego stanu
        """
        self.reachable = reachable  # czy wezel stanu jest osiagalny (czy pole nie jest sciana)
        self.x = x  # wspolrzedna x pola
        self.y = y  # wspolrzedna y pola
        self.parent = None  # wskaznik na wezel poprzedniego stanu
        self.g = 0  # koszt dotarcia z wezla poczatkowego do danego
        self.h = 0  # koszt dotarcia z danego wezla do celu
        self.f = 0  # koszt calkowity

    def __str__(self):
        """
        Zwraca informacje o wspolrzednych wezla reprezntujacego stan w formie stringa
        """
        return '(' + str(self.x) + ',' + str(self.y) + ')'


class AStar(object):
    """
    tworzy nowy obiekt AStar
    """

    def __init__(self):
        self.opened = []  # lista otwartych stanow - pola nieprzejrzane/nieodwiedzone
        heapq.heapify(self.opened)  # kolejka priorytetowa otwartych pol do odwiedzenia
        self.closed = []  # pola zamkniete - pola juz przejrzane/odwiedzone
        self.nodes = []  # wszystkie mozliwe dostepne pola
        self.mapheight = 0  # wymiary przestrzeni stanow - mapy
        self.mapwidth = 0

    def init_grid(self, matrix):  # przeksztalcanie mapy na przestrzen stanow
        self.mapheight = len(matrix)
        self.mapwidth = len(matrix[0])
        walls = get_walls(matrix)  # znalezienie scian - wezlow dla stanow nieosiagalnych
        for y in range(self.mapheight):
            for x in range(self.mapwidth):
                if (y, x) in walls:
                    reachable = False
                else:
                    reachable = True
                self.nodes.append(Node(x, y, reachable))  # umieszczenie wezlow reprezentujacych dostepne stany na liscie

    def get_heuristic(self, node):
        """
        oblicza wartosc funkcji heurystycznej H dla danego stanu: dystans pomiedzy
        wezlem reprezentujacym dany stan, a wezlem reprezentujacym stan docelowy
        """
        return 100 * (abs(node.x - self.end.x) + abs(node.y - self.end.y))

    def get_node(self, y, x):
        """
        zwraca wezel dla danego stanu z listy wezlow wszystkich stanow
        """
        return self.nodes[y * self.mapwidth + x]

    def get_adjacent_nodes(self, node):
        """
        odpowiednik funkcji ROZSZERZAJACEJ DRZEWO
        zwraca liste nastepnikow dla wezla danego stanu
        """
        nodes = []
        if node.x < self.mapwidth - 1:
            nodes.append(self.get_node(node.y, node.x + 1))
        if node.y > 0:
            nodes.append(self.get_node(node.y - 1, node.x))
        if node.x > 0:
            nodes.append(self.get_node(node.y, node.x - 1))
        if node.y < self.mapheight - 1:
            nodes.append(self.get_node(node.y + 1, node.x))

        return nodes

    def get_path(self, path):
        """
        zwraca liste wezlow dla stanow przy kolejnych akcjach podejmowanych przez agenta
        """
        node = self.end
        while node.parent is not self.start:
            node = node.parent
            path.append((node.y, node.x))
        return list(reversed(path))

    def update_node(self, adj, node):
        """
        wybiera najlepszy wezel z listy nastepnikow konkretnego wezla dla danego stanu
        """
        adj.g = node.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = node
        adj.f = adj.h + adj.g

    def process(self, start, end1, end2):
        """
        proces znajdowania listy wezlow stanow dla kolejnych akcji podejmowanych przez agenta
        """
        self.start = self.get_node(start[0], start[1])  # poczatkowy wezel reprezentujacy stan poczatkowy
        self.end = self.get_node(end1, end2)  # docelowy wezel reprezentujacy docelowy stan
        path = []  # lista wszystkich przebytych wezlow
        if self.end == self.start:
            return path
        # poczatkowy wezel otwiera kolejke priorytetowa
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # zdejmij wezel z kolejki
            f, node = heapq.heappop(self.opened)
            # dodaj wezel do listy zamknietych wezlow
            self.closed.append(node)
            # jezeli to docelowy wezel - zwroc liste wszystkich przebytych wezlow
            if node is self.end:
                return self.get_path(path)
            # znajdz liste nastepnikow danego wezla
            adj_nodes = self.get_adjacent_nodes(node)
            for adj_node in adj_nodes:
                if adj_node.reachable and adj_node not in self.closed:
                    if (adj_node.f, adj_node) in self.opened:
                        # jezeli nastepnik jest na otwartej liscie i jest osiagalny
                        # to sprawdz czy nowa, przechodzaca przez niego sciezka
                        # jest lepsza od starej
                        if adj_node.g > node.g + 10:
                            self.update_node(adj_node, node)
                    else:
                        self.update_node(adj_node, node)
                    # dodaj nastepnik nastepnika na otwarta liste
                    heapq.heappush(self.opened, (adj_node.f, adj_node))


def get_actions(path, start, end1, end2):
    """
    odpowiednik FUNKCJI NASTEPNIKA - zwraca liste akcji, ktore musi wykonac agent
    aby przejsc od stanu poczatkowego do stanu koncowego
    """
    path.insert(0, start)  # dodaj wezel reprezentujacy stan poczatkowy
    path.append((end1, end2))  # dodaj wezel reprezentujacy stan koncowy
    path1 = []  # zwracana lista akcji - akcja to ruch w okreslonym kierunku
    for x in range(len(path) - 1):
        if path[x][0] < path[x + 1][0]:
            path1.append('down')
        elif path[x][0] > path[x + 1][0]:
            path1.append('up')
        elif path[x][1] < path[x + 1][1]:
            path1.append('right')
        elif path[x][1] > path[x + 1][1]:
            path1.append('left')
    return path1
