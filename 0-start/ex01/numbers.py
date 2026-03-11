def parse_file():
    with open("numbers.txt", "r") as f:
        content = f.read()
        return content.split(",")

def print_nums():
    vals = parse_file()
    for num in vals:
        print(num)

if __name__ == "__main__":
    print_nums()