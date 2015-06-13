'''tworzenie nowego drzewa decyzyjnego oraz klasyfikacja danych treningowych'''

def majority_value(data, target_attr):
    '''tworzy liste wszystkich wartosci danego atrybutu dla kazdego rekordu
    w zestawie danych i zwraca wartosc wystepujaca najczesciej'''
    data = data[:]
    return most_frequent([record[target_attr] for record in data])

def most_frequent(lst):
    '''zwraca najczesciej wystepujacy element na danej liscie'''
    lst = lst[:]
    highest_freq = 0
    most_freq = None

    for val in unique(lst):
        if lst.count(val) > highest_freq:
            most_freq = val
            highest_freq = lst.count(val)
            
    return most_freq

def unique(lst):
    '''zwraca liste utworzona z unikalnych wartosci - usuwa powtarzajace
    sie rekordy'''
    lst = lst[:]
    unique_lst = []

    #przejdz przez cala lista i wstaw element kazdego typu tylko raz
    for item in lst:
        if unique_lst.count(item) <= 0:
            unique_lst.append(item)
            
    #zwroc liste bez powtarzajacych sie rekordow
    return unique_lst

def get_values(data, attr):
    '''tworzy liste wartosci dla danego atrybutu dla kazdego rekordu w zbiorze
    danych, usuwajac powtarzajace sie wartosci'''
    data = data[:]
    return unique([record[attr] for record in data])

def choose_attribute(data, attributes, target_attr, fitness):
    '''przebiega przez wszystkie dostepne atrybuty i wybiera atrybut o najwiekszym
    zysku informacyjnym (information gain) lub o najnizszej entropii'''
    data = data[:]
    best_gain = 0.0
    best_attr = None

    for attr in attributes:
        gain = fitness(data, attr, target_attr)
        if (gain >= best_gain and attr != target_attr):
            best_gain = gain
            best_attr = attr
                
    return best_attr

def get_examples(data, attr, value):
    '''zwraca liste wszystkich rekordow z listy danych, ktorych wartosc
    dla danego atrybutu pasuje do wzorca'''
    data = data[:]
    rtn_lst = []
    
    if not data:
        return rtn_lst
    else:
        record = data.pop()
        if record[attr] == value:
            rtn_lst.append(record)
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst
        else:
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst

def get_classification(record, tree):
    '''przeszukuje rekurencyjnie drzewo decyzyjne i zwraca klasyfikacje
    dla danego rekordu'''
    #jezeli dany wezel jest stringiem, to doszlismy do liscia
    #zwracamy odpowiedz
    if type(tree) == type("string"):
        return tree

    #przeszukuje rekurencyjnie drzewo az natrafi na lisc
    else:
        attr = tree.keys()[0]
        t = tree[attr][record[attr]]
        return get_classification(record, t)

def classify(tree, data):
    '''zwraca liste klasyfikacyjna dla wszystkich rekordow z listy danych
    na podstawie drzewa decyzyjnego'''
    data = data[:]
    classification = []
    
    for record in data:
        classification.append(get_classification(record, tree))

    return classification

def create_decision_tree(data, attributes, target_attr, fitness_func):
    '''zwraca nowe drzewo decyzyjne na podstawie zbioru treningowego'''
    data = data[:]
    vals = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    #jezeli zbior danych lub atrybutow jest pusty, zwroc wartosc domyslna
    #(odejmujemy jedynke, aby nie uwzgledniac atrybutu decyzyjnego)
    if not data or (len(attributes) - 1) <= 0:
        return default
    #jezeli wszystkie rekordy w zbiorze danych maja te sama klasyfikacje
    #zwroc ja
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        #wybierz nastepny najlepszy atrybut, aby klasyfikowac dane
        best = choose_attribute(data, attributes, target_attr,
                                fitness_func)

        #stworz nowe drzewo decyzyjne z najlepszego atrybutu
        #jako pusty slownik
        tree = {best:{}}

        #stworz nowe drzewo decyzyjne/poddrzewo dla kazdej wartosci
        #najlepszego atrybutu
        for val in get_values(data, best):
            #tworz poddrzewo dla danej wartosci z nastepnym najlepszym
            #atrybutem
            subtree = create_decision_tree(
                get_examples(data, best, val),
                [attr for attr in attributes if attr != best],
                target_attr,
                fitness_func)

            #dodaj nowe poddrzewo do slownika
            tree[best][val] = subtree

    return tree
