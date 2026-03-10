class Intern:
    """An intern"""

    def __init__(self, name="My name? I’m nobody, an intern, I have no name."):
        self.Name = name

    def __str__(self):
        return self.Name

    def work(self):
        raise Exception("I'm just an intern, I can't do that...")
    def make_coffee(self):
        return Coffee()

class Coffee:
    """A coffee"""

    def __str__(self):
        return "This is the worst coffee you ever tasted."

if __name__ == "__main__":
    noname = Intern()
    mark = Intern("Mark")

    print(str(noname))
    print(str(mark))
    print(str(mark.make_coffee()))

    try:
        noname.work()
    except Exception as e:
        print(e)
