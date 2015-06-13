# InteligentnyOdkurzacz

Projekt powstal na zaliczenie przedmiotu "Sztuczna inteligencja" i zostal wykonany przez piecioosobowa grupe w skladzie: Maciej Biesek, Sebastian Gradys, Adam Klimczyk, Antonina Krawczyk, Joanna Wetesko.

Celem projektu było zaimplementowanie samosprzątającego odkurzacza, wykorzystującego elementy sztucznej inteligencji.

Odkurzacz porusza się po planszy 25x25, a jego zadaniem jest posprzątanie zabałaganionego pokoju. Elementami scenografii są ściany, meble i inne elementy wystroju wnętrza, z którymi agent musi unikać kolizji - plamy po winie, kurz i rozrzucone puszki, które musi posprzątać - oraz kosz na śmieci, do którego opróżnia swój ekwipunek. Za każdy zebrany śmieć naliczona jest pewna liczba punktów w zależności od rodzaju brudu. Dodatkowo, odkurzacz posiada parametr “pojemność”, który określa maksymalną liczbę śmieci, które agent może zebrać - w przypadku zapełnienia konieczne jest odwiedzenie kosza na śmieci i opróżnienie ekwipunku. Warto dodać, że im mniej elementów agent posiada w ekwipunku, tym łatwiej jest mu się poruszać.

Wykorzystane metody uczenia i rozwiazywania problemow:

  uczenie drzew decyzyjnych (Joanna Wetesko)
  przeszukiwanie przestrzeni stanów - algorytm A* (Antonina Krawczyk)
  przeszukiwanie przestrzeni stanów - algorytm IDA* (Sebastian Gradys)
  sieci neuronowe (Maciej Biesek)
  algorytm genetyczny (Adam Klimczyk)


