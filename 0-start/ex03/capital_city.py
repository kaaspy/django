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

def capital_city():
    if len(sys.argv) != 2:
        return
    
    states, capitals = input()
    try:
        code = states[sys.argv[1]]
    except:
        print("Unknown state")
        return
    print(capitals[code])

if __name__ == "__main__":
    capital_city()