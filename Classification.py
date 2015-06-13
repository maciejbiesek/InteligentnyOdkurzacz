import dtree
import id3

'''funkcje rozmywajace konkretne dane, aby byly zrozumiale dla agenta'''

def fuzzifyEquipment(capacity, equipment):
        fill = float(equipment) / capacity
        if fill < 0.5:
            return 'empty'
        elif fill < 0.8:
            return 'almost full'
        else:
            return 'full'

def fuzzifyDistance(size, distance):
        dist = float(distance) / size
        if dist < 0.4:
            return 'short'
        elif dist < 0.7:
            return 'medium'
        else:
            return 'far'

class Classification:

    def __init__(self, file):
        '''otwieranie pliku z danymi treningowymi'''
        fin = open(file, "r")

        '''przygotowywanie danych treningowych'''
        #lista wszystkich linii z pliku z danymi testowymi
        lines = [line.strip() for line in fin.readlines()]

        #usuwanie atrybutow z listy linii i umieszczanie ich na liscie atrybutow
        lines.reverse()
        attributes = [attr.strip() for attr in lines.pop().split(",")]
        target_attr = attributes[-1]
        lines.reverse()

        #tworzenie slownika danych
        data = []
        for line in lines:
            data.append(dict(zip(attributes,
                                 [datum.strip() for datum in line.split(",")])))

        '''tworzenie drzewa decyzyjnego na podstawie danych treningowych'''
        self.tree = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)


    def classify(self, trashlist, game):
        '''tworzenie slownika danych testowych'''
        #obliczanie odleglosci dla kazdego smiecia, rozmywanie danych informacji
        #tworzenie slownika danych
        table = []
        for i in range(len(trashlist)):
            collection = {}
            max_size = max(game.tilemap.mapheight, game.tilemap.mapwidth)
            collection['Distance'] = fuzzifyDistance(max_size, game.distance(trashlist[i]))
            collection['Points']=str(trashlist[i][2])
            collection['Equipment'] = fuzzifyEquipment(game.player.capacity, game.player.sumEquipment())
            table.append(collection)

        '''klasyfikacja danych testowych'''
        classification = dtree.classify(self.tree,table)
        table1=[]
        for item in classification:
            table1.append(item)

        return table1

    
