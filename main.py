import sys
from utils.Graph import Graph
from DrawMap import Map
import timeit

if __name__ == "__main__":
    dataFile = sys.argv[1]
    method = sys.argv[2]
    gui = False
    calc = False
    try:
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--gui':
                gui = True
            if sys.argv[i] == '--calc':
                calc = True
            if sys.argv[i] == '--jump':
                if method.lower() == 'a_star':
                    method = 'A_star_jump'
                elif method.lower() == 'a_star_bidirection':
                    method = 'A_star_bidirection_jump'
                else:
                    print('Jump is only available with A* and bidirectional A* methods.')
                    sys.exit()
    except:
        pass

    

    if calc:
        total_time = 0
        runs = 50

        for i in range(runs):
            with open(dataFile) as f:
                height, width = map(int,f.readline().strip('[]\n').split(',')) #Get the width and height
                start = tuple(map(int, f.readline().strip('()\n').split(','))) #Get the initial state

                goals =  [tuple(map(int, line.strip('()').split(','))) for line in f.readline().strip().split(' | ')]
                walls = [tuple(map(int, line.strip('()\n').split(','))) for line in f.readlines()]

                graph = Graph(width, height, start, goals, walls, method)
                if (i == runs-1):
                    mapping = Map(width, height, start, goals, walls)
            start_time = timeit.default_timer()
            solving = graph.solve()
            solution = solving['solution']
            
            node = solving['node']
            goal = solving['goal']
            steps = solving['steps']

            end_time = timeit.default_timer()
            execution_time = end_time - start_time  # time taken
            total_time += execution_time

        average_time = total_time / runs  # average time
        print(f"The {method} ran in average {average_time*1000} mili seconds over {runs} runs")
        
    else:
        with open(dataFile) as f:
            height, width = map(int,f.readline().strip('[]\n').split(',')) #Get the width and height
            start = tuple(map(int, f.readline().strip('()\n').split(','))) #Get the initial state
            goals =  [tuple(map(int, line.strip('()').split(','))) for line in f.readline().strip().split(' | ')]
            walls = [tuple(map(int, line.strip('()\n').split(','))) for line in f.readlines()]
            graph = Graph(width, height, start, goals, walls, method)
            mapping = Map(width, height, start, goals, walls)
            solving = graph.solve()
            solution = solving['solution']
            node = solving['node']
            goal = solving['goal']
            steps = solving['steps']

    print(f'{dataFile} {method}')
    if goal != None:
        print(f'{goal}  {len(node)}') 
        print(solution)
    else:
        print(f'{solution} {len(node)}')

    #Draw map
    if gui:
        mapping.get_step(steps)
        mapping.get_solution(solution)
        mapping.run()

