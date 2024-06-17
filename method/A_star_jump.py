from method.Method import Method

class A_Star_jump(Method):
    def __init__(self, graph, start, end, width, height):
        super().__init__(graph, start, end, width, height)

        for i in range(width):
            for j in range(height):
                for g in end:
                    self.graph[j][i].distance.append(abs(g[0] - i) + abs(g[1] - j))


    def get_neighbors(self, x, y):
        neighbors = []
        directions = []
        costs = []
        #Up
        if y > 0 and not (self.graph[y - 1][x].explored or self.graph[y - 1][x].wall):
            neighbors.append((x, y - 1))
            directions.append("up")
            costs.append(1)
        #Left
        if x > 0 and not (self.graph[y][x - 1].explored or self.graph[y][x - 1].wall):
            neighbors.append((x - 1, y))
            directions.append("left")
            costs.append(1)
        #Down
        if y < self.height - 1 and not (self.graph[y + 1][x].explored or self.graph[y + 1][x].wall):
            neighbors.append((x, y + 1))
            directions.append("down")
            costs.append(1)
        #Right
        if x < self.width - 1 and not (self.graph[y][x + 1].explored or self.graph[y][x + 1].wall):
            neighbors.append((x + 1, y))
            directions.append("right")
            costs.append(1)

        # Jump up
        for n in range(2, self.height):
            if y - n >= 0 and not self.graph[y - n][x].wall and self.graph[y - 1][x].wall and not self.graph[y - n][x].explored:
                neighbors.append((x, y - n))
                directions.append(f"jump_up({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump down
        for n in range(2, self.height):
            if y + n < self.height and not self.graph[y + n][x].wall and self.graph[y + 1][x].wall and not self.graph[y + n][x].explored:
                neighbors.append((x, y + n))
                directions.append(f"jump_down({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump left
        for n in range(2, self.width):
            if x - n >= 0 and not self.graph[y][x - n].wall and self.graph[y][x - 1].wall and not self.graph[y][x - n].explored:
                neighbors.append((x - n, y))
                directions.append(f"jump_left({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump right
        for n in range(2, self.width):
            if x + n < self.width and not self.graph[y][x + n].wall and self.graph[y][x + 1].wall and not self.graph[y][x + n].explored:
                neighbors.append((x + n, y))
                directions.append(f"jump_right({n})")
                costs.append(2 ** (n - 1))
                break
            
        return list(zip(neighbors, directions, costs))

    def reset(self, i):
        self.queue = {
            (self.start): {
                'path': [],
                'f': self.graph[self.start[1]][self.start[0]].distance[i],
                'g': 0
            }
        }
        self.node = [(self.start)]
        for i in range(self.height):
            for j in range(self.width):
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
                g = self.queue[(x,y)]['g']
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

                for (nx, ny), direction, cost in (neighbors):

                    if (nx, ny) not in self.node: self.node.append((nx, ny))
                    self.steps[self.times]['visited'].append((nx, ny))
                    g_n = cost + g
                    h_n = self.graph[ny][nx].distance[i]
                    if (nx, ny) not in self.queue:
                        self.queue[(nx, ny)] = {
                            'path': path + [direction],
                            'f': h_n + g_n,
                            'g': g_n
                        }
                    else:
                        if self.queue[(nx, ny)]['f'] >= g_n + h_n:
                            self.queue[(nx, ny)]['f'] = g_n + h_n
                            self.queue[(nx, ny)]['g'] = g_n
                            self.queue[(nx, ny)]['path'] = path + [direction]
                        else:
                            continue

                        
        return {'path': [], 
                'node': self.node, 
                'goal': None, 
                'steps': self.steps}