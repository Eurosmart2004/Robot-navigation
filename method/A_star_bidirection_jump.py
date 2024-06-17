from method.Method import Method

class A_star_bidirection_jump(Method):
    def __init__(self, graph, start, end, width, height):
        super().__init__(graph, start, end, width, height)
        for i in range(width):
            for j in range(height):
                for g in end:
                    forward_distance = abs(g[0] - i) + abs(g[1] - j)
                    backward_distance = abs(start[0] - i) + abs(start[1] - j)
                    self.graph[j][i].distance.append(
                        {
                            'forward': forward_distance,
                            'backward': backward_distance
                        }
                    )



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

        return list(zip(neighbors, directions, costs))  # Return a list of (neighbor, direction) tuples
    
    def get_neighbors_reverse(self, x, y):
        neighbors = []
        directions = []
        costs = []
        #Down
        if y > 0 and not (self.graph[y - 1][x].explored_reverse or self.graph[y - 1][x].wall):
            neighbors.append((x, y - 1))
            directions.append("down")
            costs.append(1)

        #Right
        if x > 0 and not (self.graph[y][x - 1].explored_reverse or self.graph[y][x - 1].wall):
            neighbors.append((x - 1, y))
            directions.append("right")
            costs.append(1)

        #Up
        if y < self.height - 1 and not (self.graph[y + 1][x].explored_reverse or self.graph[y + 1][x].wall):
            neighbors.append((x, y + 1))
            directions.append("up")
            costs.append(1)

        #Left
        if x < self.width - 1 and not (self.graph[y][x + 1].explored_reverse or self.graph[y][x + 1].wall):
            neighbors.append((x + 1, y))
            directions.append("left")
            costs.append(1)

        # Jump down
        for n in range(2, self.height):
            if y - n >= 0 and not self.graph[y - n][x].wall and self.graph[y - 1][x].wall and not self.graph[y - n][x].explored_reverse:
                neighbors.append((x, y - n))
                directions.append(f"jump_down({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump up
        for n in range(2, self.height):
            if y + n < self.height and not self.graph[y + n][x].wall and self.graph[y + 1][x].wall and not self.graph[y + n][x].explored_reverse:
                neighbors.append((x, y + n))
                directions.append(f"jump_up({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump right
        for n in range(2, self.width):
            if x - n >= 0 and not self.graph[y][x - n].wall and self.graph[y][x - 1].wall and not self.graph[y][x - n].explored_reverse:
                neighbors.append((x - n, y))
                directions.append(f"jump_right({n})")
                costs.append(2 ** (n - 1))
                break
            
        # Jump left
        for n in range(2, self.width):
            if x + n < self.width and not self.graph[y][x + n].wall and self.graph[y][x + 1].wall and not self.graph[y][x + n].explored_reverse:
                neighbors.append((x + n, y))
                directions.append(f"jump_left({n})")
                costs.append(2 ** (n - 1))
                break

        return list(zip(neighbors, directions, costs))  # Return a list of (neighbor, direction) tuples

    def reset(self, index):
        self.queue = {
            (self.start): {
                'path': [],
                'f': self.graph[self.start[1]][self.start[0]].distance[index]['forward'],
                'g': 0
            }
        }

        self.queue_reverse = {
            (self.end[index]): {
                'path': [],
                'f': self.graph[self.end[index][1]][self.end[index][0]].distance[index]['backward'],
                'g': 0
            }
        }


        self.node = [(self.start[0], self.start[1])]
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
                (x,y) = min(self.queue, key=lambda x: self.queue[x]['f'])
                self.steps[self.times]['selected'].append((x, y))
                path = self.queue[(x,y)]['path']
                f = self.queue[(x,y)]['f']
                g = self.queue[(x,y)]['g']
                del self.queue[(x,y)]

                if not self.graph[y][x].explored:
                    self.graph[y][x].explored = True


                    if (x, y) in self.backward_node:
                        return {'path': path + self.backward_node[(x, y)], 
                                'node': self.node, 
                                'goal': self.end[i], 
                                'steps': self.steps}
    
                    neighbors = self.get_neighbors(x, y)
    
                    for (nx, ny), direction, cost in (neighbors):
                    
                        if (nx, ny) not in self.node: self.node.append((nx, ny))
                        self.steps[self.times]['visited'].append((nx, ny))
                        g_n = cost + g
                        h_n = self.graph[ny][nx].distance[i]['forward']
    
                        if (nx, ny) not in self.forward_node:
                            self.forward_node[(nx, ny)] = path + [direction]
    
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
                                self.forward_node[(nx, ny)] = path + [direction]

                # Reverse direction

                (x,y) = min(self.queue_reverse, key=lambda x: self.queue_reverse[x]['f'])
                self.steps[self.times]['selected'].append((x, y))
                path = self.queue_reverse[(x,y)]['path']
                f = self.queue_reverse[(x,y)]['f']
                g = self.queue_reverse[(x,y)]['g']

                del self.queue_reverse[(x,y)]

                if not self.graph[y][x].explored_reverse:
                    self.graph[y][x].explored_reverse = True

                    if (x, y) in self.forward_node:
                        return {'path': self.forward_node[(x, y)] + path, 
                                'node': self.node, 
                                'goal': self.end[i], 
                                'steps': self.steps}

                    neighbors = self.get_neighbors_reverse(x, y)
                    for (nx, ny), direction, cost in neighbors:
                        if (nx, ny) not in self.node: self.node.append((nx, ny))
                        self.steps[self.times]['visited_reverse'].append((nx, ny))
                        g_n = cost + g
                        h_n = self.graph[ny][nx].distance[i]['backward']

                        if (nx, ny) not in self.backward_node:
                            self.backward_node[(nx, ny)] = [direction] + path

                        if (nx, ny) not in self.queue_reverse:
                            self.queue_reverse[(nx, ny)] = {
                                'path': [direction] + path,
                                'f': h_n + g_n,
                                'g': g_n
                            }
                        else:
                            if self.queue_reverse[(nx, ny)]['f'] >= g_n + h_n:
                                self.queue_reverse[(nx, ny)]['f'] = g_n + h_n
                                self.queue_reverse[(nx, ny)]['g'] = g_n
                                self.queue_reverse[(nx, ny)]['path'] = [direction] + path
                                self.backward_node[(nx, ny)] = [direction] + path

        return {'path': [], 
                'node': self.node, 
                'goal': None, 
                'steps': self.steps}