from method.Method import Method

class GBFS(Method):
    def __init__(self, graph, start, end, width, height):
        super().__init__(graph, start, end, width, height)
        for i in range(width):
            for j in range(height):
                for g in end:
                    self.graph[j][i].distance.append(abs(g[0] - i) + abs(g[1] - j))

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

    def reset(self, i):
        self.queue = {
            (self.start): {
                'path': [],
                'f': self.graph[self.start[1]][self.start[0]].distance[i],
            }
        }
        self.node = [(self.start)]
        for i in range(len(self.graph)):
            for j in range(len(self.graph[0])):
                self.graph[i][j].explored = False

        self.times = 0
        self.steps = {0: {'selected': [], 'visited': []}}

    def solve(self):
        for i in range(len(self.end)):
            self.reset(i)
            while self.queue:

                # Increase the time
                self.times += 1

                (x,y) = min(self.queue, key=lambda x: self.queue[x]['f'])
                self.steps[self.times] = {'selected': (x, y), 'visited': []}

                path = self.queue[(x,y)]['path']
                f = self.queue[(x,y)]['f']
                del self.queue[(x,y)]

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

                    f_n = self.graph[ny][nx].distance[i]
                    if (nx, ny) not in self.queue:
                        self.queue[(nx, ny)] = {
                            'path': path + [direction],
                            'f': f_n
                        }
                    else:
                        if self.queue[(nx, ny)]['f'] >= f_n:
                            self.queue[(nx, ny)]['f'] = f_n
                            self.queue[(nx, ny)]['path'] = path + [direction]
        
        return {'path': [], 
                'node': self.node, 
                'goal': None, 
                'steps': self.steps}