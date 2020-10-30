class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __cmp__(self, other):
        return self.id == other.id