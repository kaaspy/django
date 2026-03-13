import sys
from antigravity import geohash

def geohashing():
    if len(sys.argv) != 4:
        print("Invalid args")
        return
    try:
        geohash(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3].encode("utf-8"))
    except:
        print("Geohashing broke, go browse some internet")
        return

if __name__ == "__main__":
    geohashing()

