import Tilemap
import Sprite

class Player(Sprite.Sprite):
    #przeladowanie konstruktora obiektu
    def __init__(self,x,y,texture_down,texture_up,texture_left,texture_right):
        super(Player,self).__init__(x,y,texture_down)
        self.texture_down = texture_down
        self.texture_up = texture_up
        self.texture_left = texture_left
        self.texture_right = texture_right
        self.equipment = {
            "stain": 0,
            "can": 0,
            "dirt": 0
        }  #plamy #puszki #kurz
        self.capacity = 10
        self.cleaned = 0
        self.points = 0
        self.route_length = 0
    
    #funkcja poruszajaca postacia gracza
    def move(self,direction):
        self.route_length += 1

        #w lewo
        if direction == 'left':
            self.x -= 1
            #zmiana tekstury gracza
            self.image = self.texture_left
        # w prawo
        elif direction == 'right':
            self.x += 1
            #zmiana tekstury gracza
            self.image = self.texture_right
        # w gore
        elif direction == 'up':
            self.y -= 1
            #zmiana tekstury gracza
            self.image = self.texture_up
        #w dol
        elif direction == 'down':
            self.y += 1
            #zmiana tekstury gracza
            self.image = self.texture_down

    def clean(self, type, points):
        self.equipment[type] += 1
        self.cleaned += 1
        self.points += points

    #funkcja wykrywajaca ewentualne kolizje
    #uniemozliwia wyjscia postaci gracza poza mape i wejscia na kafelek zajety przez inny obiekt
    def collision(self,tilemap,direction):
        #w lewo
        if direction == 'left':
            if self.x <= 1 or tilemap.matrix[self.y][self.x-1] == 0:
                #docelowy kafelek zajety
                return False
        #w prawo
        elif direction == 'right':
            if self.x >= tilemap.mapwidth - 2 or tilemap.matrix[self.y][self.x+1] == 0:
                #docelowy kafelek zajety
                return False
        #w gore
        elif direction == 'up':
            if self.y <= 4 or tilemap.matrix[self.y-1][self.x] == 0:
                #docelowy kafelek zajety
                return False
        #w dol
        elif direction == 'down':
            if self.y >= tilemap.mapheight - 2 or tilemap.matrix[self.y+1][self.x] == 0:
                #docelowy kafelek zajety
                return False

        #docelowy kafelek jest wolny
        return True

    #funkcja podsumowujaca ekwipunek
    def sumEquipment(self):
        sum = 0
        for value in self.equipment.values():
            sum += value
        return sum

        
            

    
            

    
        

    
