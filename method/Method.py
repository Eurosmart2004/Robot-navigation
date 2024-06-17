from abc import ABC, abstractmethod

class Method(ABC):
    def __init__(self, graph, start, end, width, height):
        self.graph = graph
        self.start = start
        self.end = end
        self.width = width
        self.height = height

    @abstractmethod
    def get_neighbors(self, x, y):
        pass

    @abstractmethod
    def solve(self):
        pass