from method.Method import Method

class Bidirection(Method):
    def __init__(self, graph, start, end, width, height):
        super().__init__(graph, start, end, width, height)


    def get_neighbors(self, x, y):
        neighbors = []
        directions = []
        #Up
        if y > 0 and not (self.graph[y - 1][x].explored or self.graph[y - 1][x].wall):
            neighbors.append((x, y - 1))
            directions.append("up")

        #Left
        if x > 0 and not (self.graph[y][x - 1].explored or self.graph[y][x - 1].wall):
            neighbors.append((x - 1, y))
            directions.append("left")

        #Down
        if y < self.height - 1 and not (self.graph[y + 1][x].explored or self.graph[y + 1][x].wall):
            neighbors.append((x, y + 1))
            directions.append("down")

        #Right
        if x < self.width - 1 and not (self.graph[y][x + 1].explored or self.graph[y][x + 1].wall):
            neighbors.append((x + 1, y))
            directions.append("right")

        return list(zip(neighbors, directions))  # Return a list of (neighbor, direction) tuples
    
    def get_neighbors_reverse(self, x, y):
        neighbors = []
        directions = []
        #Down
        if y > 0 and not (self.graph[y - 1][x].explored_reverse or self.graph[y - 1][x].wall):
            neighbors.append((x, y - 1))
            directions.append("down")

        #Right
        if x > 0 and not (self.graph[y][x - 1].explored_reverse or self.graph[y][x - 1].wall):
            neighbors.append((x - 1, y))
            directions.append("right")

        #Up
        if y < self.height - 1 and not (self.graph[y + 1][x].explored_reverse or self.graph[y + 1][x].wall):
            neighbors.append((x, y + 1))
            directions.append("up")

        #Left
        if x < self.width - 1 and not (self.graph[y][x + 1].explored_reverse or self.graph[y][x + 1].wall):
            neighbors.append((x + 1, y))
            directions.append("left")

        return list(zip(neighbors, directions))  # Return a list of (neighbor, direction) tuples

    def reset(self, index):
        self.queue = [(self.start, [])]
        self.queue_reverse = [(self.end[index], [])]
        self.node = [(self.start)]
        for i in range(self.height):
            for j in range(self.width):
                self.graph[i][j].explored = False
                self.graph[i][j].explored_reverse = False

        self.steps = {0: {'selected': [], 'visited': []}}
        self.forward_node = {}
        self.backward_node = {}
        self.times = 0

    def solve(self):
        for i in range(len(self.end)):
            self.reset(i)
            while self.queue and self.queue_reverse:
                self.times += 1
                self.steps[self.times] = {'selected': [], 'visited': [], 'visited_reverse': []}
                # Forward direction
                (x, y), path = self.queue.pop(0)

                self.steps[self.times]['selected'].append((x, y))

                if not self.graph[y][x].explored:
                    self.graph[y][x].explored = True

                    if (x, y) in self.backward_node:
                        return {'path': path + self.backward_node[(x, y)], 
                                'node': self.node, 
                                'goal': self.end[i], 
                                'steps': self.steps}

                    neighbors = self.get_neighbors(x, y)
                    for (nx, ny), direction in neighbors:
                        if (nx, ny) not in self.node: self.node.append((nx, ny))
                        self.steps[self.times]['visited'].append((nx, ny))
                        self.queue.append(((nx, ny), path + [direction]))
                        self.forward_node[(nx, ny)] = path + [direction]


                # Reverse direction
                (x, y), path = self.queue_reverse.pop(0)
                self.steps[self.times]['selected'].append((x, y))
                if not self.graph[y][x].explored_reverse:
                    self.graph[y][x].explored_reverse = True

                    if (x, y) in self.forward_node:
                        return {'path': self.forward_node[(x, y)] + path, 
                                'node': self.node, 
                                'goal': self.end[i], 
                                'steps': self.steps}


                    neighbors = self.get_neighbors_reverse(x, y)
                    for (nx, ny), direction in neighbors:            
                        if (nx, ny) not in self.node: self.node.append((nx, ny))
                        self.steps[self.times]['visited_reverse'].append((nx, ny))
                        self.queue_reverse.append(((nx, ny), [direction] + path))
                        self.backward_node[(nx, ny)] = [direction] + path

        return {'path': [], 
                'node': self.node, 
                'goal': None, 
                'steps': self.steps}