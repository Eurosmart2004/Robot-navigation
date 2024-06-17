from method.DFS import DFS
from method.BFS import BFS
from method.GBFS import GBFS
from method.A_star import A_Star
from method.Bidrection import Bidirection
from method.A_star_bidirection import A_star_bidirection
from method.A_star_jump import A_Star_jump
from method.A_star_bidirection_jump import A_star_bidirection_jump
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False
        self.distance = []

class Graph:
    def __init__(self, width, height, start, goal, walls, method):
        self.width = width
        self.height = height
        self.start = start
        self.goal = goal
        self.graph = [[Cell(x, y) for x in range(width)] for y in range(height)]


        for w in walls:
            for i in range(w[0], w[0] + w[2]):
                for j in range(w[1], w[1] + w[3]):
                    self.graph[j][i].wall = True

        if method.lower() == 'dfs':
            self.method = DFS(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'bfs':
            self.method = BFS(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'bidirection':
            self.method = Bidirection(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'gbfs':
            self.method = GBFS(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'a_star':
            self.method = A_Star(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'a_star_bidirection':
            self.method = A_star_bidirection(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'a_star_jump':
            self.method = A_Star_jump(self.graph, self.start, self.goal, self.width, self.height)
        if method.lower() == 'a_star_bidirection_jump':
            self.method = A_star_bidirection_jump(self.graph, self.start, self.goal, self.width, self.height)

    def solve(self):
        solving = self.method.solve()
        solution = solving['path']
        node = solving['node']
        goal = solving['goal']
        steps = solving['steps']

        if solution == []:
            return {'solution':'No goal is reachable', 
                'node':node, 
                'goal':goal, 
                'steps':steps}
        
        solution = '; '.join(solution)
        return {'solution':solution, 
                'node':node, 
                'goal':goal, 
                'steps':steps}
    