class Sprite(object):
    #konstruktor obiektu
    def __init__(self,x,y,texture):
        self.x = x	     #wspolrzedna x obiektu 												#pozycja x obiektu
        self.y = y           #wspolrzedna y obiektu											#pozycja y obiektu
        self.image = texture #tekstura obiektu
