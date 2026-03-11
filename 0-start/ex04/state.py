import sys

def input():
    states = {
    "Oregon" : "OR",
    "Alabama" : "AL",
    "New Jersey": "NJ",
    "Colorado" : "CO"
    }
    capital_cities = {
    "OR": "Salem",
    "AL": "Montgomery",
    "NJ": "Trenton",
    "CO": "Denver"
    }
    return states, capital_cities

def state_from_capital():
    if len(sys.argv) != 2:
        return
    
    states, capitals = input()

    #Can be done since both dict entries are matched 1 to 1
    mapping = {}
    for (k1, v1), (k2, v2) in zip(states.items(), capitals.items()):
        mapping[v2] = k1
    
    #When not matched, list comprehension can be used to iter through all combinaisons
    #Better to use itertools however
    mapping = {}
    combinaisons = [((k1, v1), (k2, v2)) for (k1, v1) in states.items() for (k2, v2) in capitals.items()]
    for (k1, v1), (k2, v2) in combinaisons:
        if v1 == k2:
            mapping[v2] = k1

    try:
        ret = mapping[sys.argv[1]]
    except:
        print("Unknown capital city")
        return
    print(ret)

if __name__ == "__main__":
    state_from_capital()