from method.Method import Method

class BFS(Method):
    def __init__(self, graph, start, end, width, height):
        super().__init__(graph, start, end, width, height)
        self.queue = [(start, [])]   
        self.node = [(start[0], start[1])]
        for i in range(height):
            for j in range(width):
                self.graph[i][j].explored = False
        self.steps = {0: {'selected': [], 'visited': []}}
        self.times = 0

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

    def solve(self):
        while self.queue:
            self.times += 1
            (x, y), path = self.queue.pop(0)
            self.steps[self.times] = {'selected': (x, y), 'visited': []}
            if self.graph[y][x].explored:
                continue
            self.graph[y][x].explored = True

            if (x, y) in self.end:
                return {'path': path, 
                        'node': self.node, 
                        'goal': (x,y), 
                        'steps': self.steps}
            
            neighbors = self.get_neighbors(x, y)
            for (nx, ny), direction in (neighbors):
                if (nx, ny) not in self.node: self.node.append((nx, ny))
                self.steps[self.times]['visited'].append((nx, ny))
                self.queue.append(((nx, ny), path + [direction]))

        return {'path': [], 
                'node': self.node, 
                'goal': None, 
                'steps': self.steps}