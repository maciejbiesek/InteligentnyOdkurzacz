import math

def entropy(data, target_attr):
    '''Oblicza entropie danego zestawu danych, dla danego atrybutu'''
    val_freq = {}
    data_entropy = 0.0

    #oblicz czestotliwosc wystepowania kazdego atrybutu
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    #oblicz entropie zestawu danych dla atrybutu
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy
    
def gain(data, attr, target_attr):
    '''Oblicza zysk informacyjny (information gain), powstaly z podzialu
    danych wedlug wybranego atrybutu'''
    
    val_freq = {}
    subset_entropy = 0.0

    #oblicz czestotliwosc wystepowania kazdego atrybutu
    for record in data:
        if (val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else:
            val_freq[record[attr]] = 1.0

    #oblicz srednia wazona entropii dla kazdego podzbioru danych
    #gdzie waga jest prawdopodobienstwem, ze taki zestaw pojawi sie w zbiorze
    #treningowym
    for val in val_freq.keys():
        val_prob = val_freq[val] / sum(val_freq.values())
        data_subset = [record for record in data if record[attr] == val]
        subset_entropy += val_prob * entropy(data_subset, target_attr)

    #odejmij entropie wybranego atrybutu od entropii calego zestawu danych
    #i zwroc wynik
    return (entropy(data, target_attr) - subset_entropy)
            
