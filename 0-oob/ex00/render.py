import sys, os
from settings import *

#
# Input validation
#
def valid_filename(filename):
    ext = filename.split(".")[-1]
    if ext != "template":
        print(f"Extension is not supported : {filename}")
        return False
    if not os.path.exists(filename):
        print(f"The file does not exists : {filename}")
        return False
    return True

def valid_input():
    if len(sys.argv) != 2:
        print("You must specify only one file to parse")
        return False
    return valid_filename(sys.argv[1])
    
#
# CV generation
#
def generate_cv():
    template = None
    with open(sys.argv[1], "r") as t:
        template = t.read()
    CV = template.format(**globals()) #Expansion of all global keywords
    with open("cv.html", "w") as c:
        c.write(CV)
    
if __name__ == "__main__":
    if valid_input():
        generate_cv()
