from tkinter import *
import re

STATE = {
    "VISITED": 'VISITED',
    "VISITED_REVERSE": "VISITED_REVERSE", # For the reverse search
    "WALL": 'WALL',
    "GOAL": 'GOAL',
    "START": 'START',
    "NORMAL": 'NORMAL',
    "PATH": 'PATH',
    "SELECTED": 'SELECTED'
}

class Map:
    def __init__(self, width, height, start, goals, walls):
        self.root = Tk()
        self.root.geometry("800x600")  # Adjust the size of the window as needed
        self.root.title("Robot navigation")  # Set the title of the window
        self.cell_size = 40
        self.offset = 10  # Offset for the rectangles

        # Create a frame to hold the vertical scrollbar and the frame for the canvas and horizontal scrollbar
        self.outer_frame = Frame(self.root)
        self.outer_frame.pack(side=LEFT)

        # Create the vertical scrollbar and pack it to the left of the outer frame
        vbar=Scrollbar(self.outer_frame,orient=VERTICAL)
        vbar.pack(side=LEFT,fill=Y)

        # Create a frame to hold the canvas and horizontal scrollbar
        self.frame = Frame(self.outer_frame)
        self.frame.pack(side=RIGHT)

        self.canvas = Canvas(self.frame, width=512, height=512, scrollregion=(0,0,(width+1)*self.cell_size,(height+1)*self.cell_size))  # Set the size of the canvas and its scroll region
        self.canvas.pack(side=TOP)  # Pack canvas to the top of the frame
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.drag_move)
        self.start = start
        self.goals = goals
        self.walls = walls
        self.height = height
        self.width = width
        self.maze = [[Cell(x, y, self.canvas, self.cell_size, self.offset) for x in range(width)] for y in range(height)]
        self.step = {}
        self.it = 0

        # Buttons are now on the left side of the map
        self.buttonNext = Button(self.root, text="Next", command=lambda: self.update('next'), height=2, width=10)  # Increase button size
        self.buttonNext.pack(side=TOP, padx=5, pady=5)  # Add padding around the button

        self.buttonBack = Button(self.root, text="Back", command=lambda: self.update('back'), height=2, width=10)  # Increase button size
        self.buttonBack.pack(side=TOP, padx=5, pady=5)  # Add padding around the button

        for w in walls:
            for i in range(w[0], w[0] + w[2]):
                for j in range(w[1], w[1] + w[3]):
                    self.maze[j][i].state = STATE["WALL"]

        for goal in goals:
                self.maze[goal[1]][goal[0]].state = STATE["GOAL"]

        self.maze[start[1]][start[0]].state = STATE["START"]

        # Create scrollbars for the canvas
        hbar=Scrollbar(self.frame,orient=HORIZONTAL)
        hbar.pack(side=BOTTOM,fill=X)
        hbar.config(command=self.canvas.xview)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        
    def start_move(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def get_step(self, step):
        self.step = step

    def get_solution(self, solution):
        current_position = self.start
        solution = solution.split('; ')
        self.solution = []
        for s in solution:
            if 'jump' in s:
                direction, num = re.findall(r'(\w+)\((\d+)\)', s)[0]  # Extract the direction and number from the string
                num = int(num)
                if direction == 'jump_up':
                    current_position = (current_position[0], current_position[1] - num)
                elif direction == 'jump_down':
                    current_position = (current_position[0], current_position[1] + num)
                elif direction == 'jump_left':
                    current_position = (current_position[0] - num, current_position[1])
                elif direction == 'jump_right':
                    current_position = (current_position[0] + num, current_position[1])
            else:
                if s == 'up':
                    current_position = (current_position[0], current_position[1] - 1)
                if s == 'down':
                    current_position = (current_position[0], current_position[1] + 1)
                if s == 'left':
                    current_position = (current_position[0] - 1, current_position[1])
                if s == 'right':
                    current_position = (current_position[0] + 1, current_position[1])
            
            self.solution.append(current_position)

    def update(self, direction):

        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x].number = ''
                if self.maze[y][x].state == STATE["VISITED"]:
                    self.maze[y][x].state = STATE["NORMAL"]
                if self.maze[y][x].state == STATE["VISITED_REVERSE"]:
                    self.maze[y][x].state = STATE["NORMAL"]
                if self.maze[y][x].selected:
                    self.maze[y][x].selected = False
                if self.maze[y][x].state == STATE["PATH"]:
                    self.maze[y][x].state = STATE["NORMAL"]


        if direction == 'next' and self.it < len(self.step) - 1:
            self.it += 1

        if direction == 'back' and self.it > 0:
            self.it -= 1

        j = 0
        while True:

            selected = None
            if j == self.it:
                if isinstance(self.step[j]['selected'], list):
                    for selected in self.step[j]['selected']:
                        self.maze[selected[1]][selected[0]].selected = True
                else:
                    selected = self.step[j]['selected']
                    self.maze[selected[1]][selected[0]].selected = True
                
            for v in self.step[j]['visited']:
                if self.maze[v[1]][v[0]].state != STATE["START"] and self.maze[v[1]][v[0]].state != STATE["GOAL"]:
                    self.maze[v[1]][v[0]].state = STATE["VISITED"]
            if ('visited_reverse' in self.step[j]):
                for v in self.step[j]['visited_reverse']:
                    if self.maze[v[1]][v[0]].state != STATE["START"] and self.maze[v[1]][v[0]].state != STATE["GOAL"]:
                        self.maze[v[1]][v[0]].state = STATE["VISITED_REVERSE"]
            
            j += 1

            if j > self.it:
                break
        if j > len(self.step) - 1:
            for index, s in enumerate(self.solution):
                self.maze[s[1]][s[0]].number = index
                if self.maze[s[1]][s[0]].state != STATE["START"] and self.maze[s[1]][s[0]].state != STATE["GOAL"]:
                    self.maze[s[1]][s[0]].state = STATE["PATH"]
        self.draw_map()

    def draw_map(self):
        for y in range(self.height):
            for x in range(self.width):
                self.maze[y][x].draw()

        
        

    def run(self):
        self.draw_map()
        self.root.mainloop()



class Cell:
    def __init__(self, 
                 x: int, 
                 y: int, 
                 canvas: Canvas, 
                 cell_size: int,
                 offset: int
                 ) -> None:
        self.x = x
        self.y = y
        self.state = STATE["NORMAL"]
        self.canvas = canvas
        self.cell_size = cell_size
        self.offset = offset
        self.selected = False
        self.number = ''

    def get_color(self):
        if self.state == STATE["VISITED"]:
            return "blue"
        if self.state == STATE["VISITED_REVERSE"]:
            return "purple"
        if self.state == STATE["WALL"]:
            return "gray"
        if self.state == STATE["GOAL"]:
            return "green"
        if self.state == STATE["START"]:
            return "red"
        if self.state == STATE["PATH"]:
            return "yellow"
        if self.state == STATE['NORMAL']:
            return "white"

    def draw(self):
        self.canvas.create_rectangle(
                                    self.offset + self.x * self.cell_size,
                                    self.offset + self.y * self.cell_size,
                                    self.offset + (self.x + 1) * self.cell_size,
                                    self.offset + (self.y + 1) * self.cell_size,
                                    outline="black",
                                    fill=self.get_color())
        if self.selected:
            self.canvas.create_rectangle(
                            self.offset + self.x * self.cell_size,
                            self.offset + self.y * self.cell_size,
                            self.offset + (self.x + 1) * self.cell_size,
                            self.offset + (self.y + 1) * self.cell_size,
                            outline="black",
                            fill="pink")
            
        center_x = self.offset + (self.x + 0.5) * self.cell_size
        center_y = self.offset + (self.y + 0.5) * self.cell_size
        self.canvas.create_text(center_x, center_y, text=self.number)

        