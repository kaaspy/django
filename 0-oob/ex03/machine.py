import random
from beverages import *

class CoffeeMachine:
    """A coffee machine"""

    def __init__(self):
        self.served = 0
        self.broken = False
    
    class EmptyCup(HotBeverage):
        """An emtpy cup"""

        def __init__(self):
            self.name = "empty cup"
            self.price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        """It broke again..."""
        def __init__(self):
            self.message = "This coffee machine has to be repaired."
            super().__init__(self.message)
    
    def repair(self):
        self.broken = False
        self.served = 0

    def serve(self, beverage):
        self.served += 1
        if self.served > 10:
            self.broken = True

        if self.broken:
            raise self.BrokenMachineException()

        if random.random() > 0.5:
            return self.EmptyCup()
        else:
            return beverage()

if __name__ == "__main__":
    machine = CoffeeMachine()
    for _ in range(22):
        try:
            print(str(machine.serve(Coffee)))
            print("~~~")
        except Exception as e:
            print(e)
            machine.repair()
            print("Machine is now repaired")
            print("~~~")



