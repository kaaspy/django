
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

def mappings():
    states, capitals = input()

    #Can be done since both dict entries are matched 1 to 1
    capital_to_state = {}
    for (k1, _), (_, v2) in zip(states.items(), capitals.items()):
        capital_to_state[v2] = k1

    state_to_capital = {}
    for (k1, _), (_, v2) in zip(states.items(), capitals.items()):
        state_to_capital[k1] = v2
    
    return capital_to_state, state_to_capital

def parse_sysin():
    if len(sys.argv) != 2:
        return
    output = []
    input = sys.argv[1].split(",")
    for field in input:
        output.append((field.strip().lower().capitalize(), field.strip()))
            
    return list(filter(lambda f: f[0] != "", output))


def all_in():
    fields = parse_sysin()
    if not fields:
        return

    capital_to_state, state_to_capital = mappings()
    for f, o in fields:
        try:
            val = capital_to_state[f]
            print(f"{f} is the capital of {val}")
        except:
            try:
                val = state_to_capital[f]
                print(f"{val} is the capital of {f}")
            except:
                print(f"{o} is neither a capital city nor a state")

if __name__ == "__main__":
    all_in()