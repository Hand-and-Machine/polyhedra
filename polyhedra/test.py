import os

__location__ = os.path.dirname(__file__)

def hello():
    print("What the hell did you expect? A greeting or something?")

def doggo():
    file = open(os.path.join(__location__, "data/testdoc.txt"), 'r')
    for line in file:
        print(line,end="")

def lookaround():
    print(os.listdir(__location__))
