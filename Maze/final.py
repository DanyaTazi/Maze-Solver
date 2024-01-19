
import turtle                    # import turtle library
import time
import cProfile
import sys
from collections import deque
from tkinter import *
from queue import PriorityQueue




wn = turtle.Screen()               # define the turtle screen
wn.bgcolor("#5A189A")                # set the background colour
wn.title("Maze Solver By: Danya and Youssef") 
wn.setup(1400,700)                  # setup the dimensions of the working window


# this is the class for the Maze
class Maze(turtle.Turtle):               # define a Maze class
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # the turtle shape
        self.color("white")             # colour of the turtle
        self.penup()                    # lift up the pen so it do not leave a trail
        self.speed(0)

# this is the class for the finish line - pathOrange square in the maze
class PathOrange(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#F56A00")
        self.penup()
        self.speed(0)

class FtierOrange(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#FF9E00")
        self.penup()
        self.speed(0)


# this is the class for the dark purple backtracking
class Red(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#5A189A")
        self.penup()
        self.speed(0)

class Violet(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("#240046")
        self.penup()
        self.speed(0)



# classes
maze = Maze()
red = Red()
ftierOrange = FtierOrange()
pathOrange = PathOrange()
violet = Violet()


# lists

#For BFS
path = []
visitedBFS = set()
frontierBFS = deque()
solution = {}                           # solution dictionary

#For DFS
visitedDFS = []
frontierDFS = []

#For A star
frontierA = PriorityQueue()
visitedA = []

#For GBFS
frontierGBFS = PriorityQueue()
visitedGBFS = []


is_paused = False
is_verbose = False




def create_maze_grid(file_path):
    with open(file_path, 'r') as file:
        maze_data = file.readlines()

    # Remove trailing newline characters
    maze_data = [line.rstrip('\n') for line in maze_data]

    num_rows = len(maze_data)
    num_cols = len(maze_data[0])

    global grid

    grid = [[' ' for _ in range(num_cols)] for _ in range(num_rows)]

    for i in range(num_rows):
        for j in range(num_cols):
            grid[i][j] = maze_data[i][j]

    return grid





def setup_maze(grid):                          # define a function called setup_maze
    global start_x, start_y, end_x, end_y      # set up global variables for start and end locations
    
    for y in range(len(grid)):                 # read in the grid line by line
        for x in range(len(grid[y])):          # read each cell in the line
            character = grid[y][x]             # assign the varaible "character" the x and y location on the grid
            screen_x = -588 + (x * 24)         # move to the x location on the screen staring at -588
            screen_y = 288 - (y * 24)          # move to the y location of the screen starting at 288
            if character == "+":
                maze.goto(screen_x, screen_y)         # move pen to the x and y locaion and
                maze.stamp()                          # stamp a copy of the turtle on the screen
            if character == " " or character == "e":
                path.append((screen_x, screen_y))     # add " " and e to path list
            if character == "e":
                red.color("red")
                red.goto(screen_x, screen_y)       # send red sprite to screen location
                end_x, end_y = screen_x,screen_y     # assign end locations variables to end_x and end_y
                red.stamp()
                pathOrange.color("#F56A00")
            if character == "s":
                start_x, start_y = screen_x, screen_y  # assign start locations variables to start_x and start_y
                red.color("red")
                red.goto(screen_x, screen_y)
                red.stamp()


def endProgram():
    wn.exitonclick()
    sys.exit()




def BFS(x,y):
    frontierBFS.append((x, y))                             # add the x and y position to the frontier list
    solution[x,y] = x,y                                    # add x and y to the solution dictionary 
    BFSlogic(x,y)


def DFS(x,y):
    frontierDFS.append((x, y))                            
    solution[x, y] = x, y                                                        
    DFSlogic(x,y)


def GBFS(x,y):
    frontierGBFS.put((heuristic(x,y), (x,y)))
    solution[x, y] = x, y 
    GBFSlogic(x,y)

def Astar(x,y):
    frontierA.put((total_cost(x,y), (x,y)))
    solution[x, y] = x, y 
    Astarlogic(x,y)


def total_cost(x, y):

    path_cost = 0
    while (x, y) != (start_x, start_y):    # stop loop when current cells == start cell
        x, y = solution[x, y]               # "key value" now becomes the new key
        path_cost += 1
    totalVal = abs(end_x - x) + abs(end_y - y) + path_cost
    return totalVal


def heuristic(x, y):

    heurVal = abs(end_x - x) + abs(end_y - y)
    
    return heurVal


def BFSlogic(x,y):
    
    global valInc
    global is_paused
    global is_verbose
    count = 0

    while (x,y) != (end_x, end_y) and not is_paused:          # exit while loop when goal is reached
        #time.sleep(0)
        x, y = frontierBFS.popleft()     # pop next entry in the frontier queue an assign to x and y location
        if(x - 24, y) in path and (x - 24, y) not in visitedBFS:  # check the cell on the left
            cell = (x - 24, y)
            solution[cell] = x, y    
            ftierOrange.goto(cell)        # identify frontier cells
            ftierOrange.stamp()
            frontierBFS.append(cell)   # add cell to frontier list
            visitedBFS.add((x, y))  # add current cell to visited list
        if (x, y - 24) in path and (x, y - 24) not in visitedBFS:  # check the cell down
            cell = (x, y - 24)
            solution[cell] = x, y
            ftierOrange.goto(cell)
            ftierOrange.stamp()
            frontierBFS.append(cell)
            visitedBFS.add((x, y))
        if(x + 24, y) in path and (x + 24, y) not in visitedBFS:   # check the cell on the  right
            cell = (x + 24, y)
            solution[cell] = x, y
            ftierOrange.goto(cell)
            ftierOrange.stamp()
            frontierBFS.append(cell)
            visitedBFS.add((x, y))
        if(x, y + 24) in path and (x, y + 24) not in visitedBFS:  # check the cell up
            cell = (x, y + 24)
            solution[cell] = x, y
            ftierOrange.goto(cell)
            ftierOrange.stamp()
            frontierBFS.append(cell)
            visitedBFS.add((x, y))


        count +=1

        if is_verbose and count == int(valInc):
            print(f"The Number of explored nodes: {len(visitedBFS)}")
            count = 0
            is_paused = not is_paused


        pathOrange.goto(x,y)
        pathOrange.stamp()

        if (x,y) == (end_x, end_y):             # makes sure the red end turtle is still visible after been visited
            red.stamp()                         # restamp the red turtle at the end position 
        if (x,y) == (start_x, start_y):         # makes sure the red start turtle is still visible after been visited
            red.stamp()                         # restamp the red turtle at the start position 

    print(f"The Number of explored nodes: {len(visitedBFS)}")

    if is_paused:
        wn.ontimer(lambda: BFSlogic(x, y), 100)  # Schedule the next BFS iteration

    if not is_paused:
        backRoute(end_x,end_y)



def DFSlogic(x,y):

    global valInc
    global is_paused
    global is_verbose
    count = 0

    while (x,y) != (end_x, end_y) and not is_paused:                          
        time.sleep(0)                                  # change this value to make the animation go slower
        current = (x,y)                                # current cell equals x and  y positions

        if(x - 24, y) in path and (x - 24, y) not in visitedDFS:  # check left
            cellleft = (x - 24, y)
            solution[cellleft] = x, y  
            ftierOrange.goto(cellleft)        # ftierOrange turtle goto the  cellleft position
            ftierOrange.stamp()               # stamp a ftierOrange turtle on the maze
            frontierDFS.append(cellleft)  # add cellleft to the frontier list

        if (x, y - 24) in path and (x, y - 24) not in visitedDFS:  # check down
            celldown = (x, y - 24)
            solution[celldown] = x, y  
            ftierOrange.goto(celldown)
            ftierOrange.stamp()
            frontierDFS.append(celldown)

        if(x + 24, y) in path and (x + 24, y) not in visitedDFS:   # check right
            cellright = (x + 24, y)
            solution[cellright] = x, y  
            ftierOrange.goto(cellright)
            ftierOrange.stamp()
            frontierDFS.append(cellright)

        if(x, y + 24) in path and (x, y + 24) not in visitedDFS:  # check up
            cellup = (x, y + 24)
            solution[cellup] = x, y 
            ftierOrange.goto(cellup)
            ftierOrange.stamp()
            frontierDFS.append(cellup)

        count += 1

        x, y = frontierDFS.pop()             # remove last entry from the frontier list and assign to x and y
        visitedDFS.append(current)           # add current cell to visited list

        if is_verbose and count == int(valInc) :
            print(f"The Number of explored nodes: {len(visitedDFS)}")
            count = 0
            is_paused = not is_paused

        pathOrange.goto(x,y)                 # pathOrange turtle goto x and y position
        pathOrange.stamp()                   # stamp a copy of the pathOrange turtle on the maze

        
        if (x,y) == (end_x, end_y):          # makes sure the red end turtle is still visible after been visited
            red.stamp()                      # restamp the red turtle at the end position 
        if (x,y) == (start_x, start_y):      # makes sure the red start turtle is still visible after been visited
            red.stamp()                      # restamp the red turtle at the start position 


    print(f"The Number of explored nodes: {len(visitedDFS)}")

    if is_paused:
        wn.ontimer(lambda: DFSlogic(x, y), 100)  # Schedule the next DFS iteration

    if not is_paused:
        backRoute(end_x,end_y)



    
def GBFSlogic(x,y):

    global valInc
    global is_paused
    global is_verbose
    count = 0


    while (x,y) != (end_x, end_y) and not is_paused:
        time.sleep(0)
        current = (x,y)

        if(x - 24, y) in path and (x - 24, y) not in visitedGBFS:  # check left
            cellleft = (x - 24, y)
            solution[cellleft] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellleft)        # ftierOrange turtle goto the  cellleft position
            ftierOrange.stamp()               # stamp a ftierOrange turtle on the maze
            frontierGBFS.put((heuristic(cellleft[0], cellleft[1]), cellleft))  # add cellleft to the frontier list

        if (x, y - 24) in path and (x, y - 24) not in visitedGBFS:  # check down
            celldown = (x, y - 24)
            solution[celldown] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(celldown)
            ftierOrange.stamp()
            frontierGBFS.put((heuristic(celldown[0], celldown[1]), celldown))

        if(x + 24, y) in path and (x + 24, y) not in visitedGBFS:   # check right
            cellright = (x + 24, y)
            solution[cellright] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellright)
            ftierOrange.stamp()
            frontierGBFS.put((heuristic(cellright[0], cellright[1]), cellright))

        if(x, y + 24) in path and (x, y + 24) not in visitedGBFS:  # check up
            cellup = (x, y + 24)
            solution[cellup] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellup)
            ftierOrange.stamp()
            frontierGBFS.put((heuristic(cellup[0], cellup[1]), cellup))

        count += 1

        tempTuple = frontierGBFS.get()
        x, y = tempTuple[1]
        visitedGBFS.append(current)

        if is_verbose and count == int(valInc):
            print(f"The Number of explored nodes: {len(visitedGBFS)}")
            count = 0
            is_paused = not is_paused


        pathOrange.goto(x,y)                 # pathOrange turtle goto x and y position
        pathOrange.stamp() 
    

        if (x,y) == (end_x, end_y):     # makes sure the yellow end turtle is still visible after been visited
            red.stamp()              # restamp the yellow turtle at the end position 
        if (x,y) == (start_x, start_y): # makes sure the red start turtle is still visible after been visited
            red.stamp()                 # restamp the red turtle at the start position 

    print(f"The Number of explored nodes: {len(visitedGBFS)}")   


    if is_paused:
        wn.ontimer(lambda: GBFSlogic(x, y), 100)  # Schedule the next GBFS iteration

    if not is_paused:
        backRoute(end_x,end_y)



def Astarlogic(x,y):

    global valInc
    global is_paused
    global is_verbose
    count = 0
    

    while (x,y) != (end_x, end_y) and not is_paused:
        time.sleep(0)
        current = (x,y)

        if(x - 24, y) in path and (x - 24, y) not in visitedA:  # check left
            cellleft = (x - 24, y)
            solution[cellleft] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellleft)        # ftierOrange turtle goto the  cellleft position
            ftierOrange.stamp()               # stamp a ftierOrange turtle on the maze
            frontierA.put((total_cost(cellleft[0], cellleft[1]), cellleft))  # add cellleft to the frontier list

        if (x, y - 24) in path and (x, y - 24) not in visitedA:  # check down
            celldown = (x, y - 24)
            solution[celldown] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(celldown)
            ftierOrange.stamp()
            frontierA.put((total_cost(celldown[0], celldown[1]), celldown))

        if(x + 24, y) in path and (x + 24, y) not in visitedA:   # check right
            cellright = (x + 24, y)
            solution[cellright] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellright)
            ftierOrange.stamp()
            frontierA.put((total_cost(cellright[0], cellright[1]), cellright))

        if(x, y + 24) in path and (x, y + 24) not in visitedA:  # check up
            cellup = (x, y + 24)
            solution[cellup] = x, y  # backtracking routine [cell] is the previous cell. x, y is the current cell
            ftierOrange.goto(cellup)
            ftierOrange.stamp()
            frontierA.put((total_cost(cellup[0], cellup[1]), cellup))

        count += 1


        tempTuple = frontierA.get()
        x, y = tempTuple[1]
        visitedA.append(current)


        if is_verbose and count == int(valInc):
            print(f"The Number of explored nodes: {len(visitedA)}")
            count = 0
            is_paused = not is_paused

        pathOrange.goto(x,y)                 # pathOrange turtle goto x and y position
        pathOrange.stamp() 



        if (x,y) == (end_x, end_y):     # makes sure the red end turtle is still visible after been visited
            red.stamp()              # restamp the red turtle at the end position 
        if (x,y) == (start_x, start_y): # makes sure the red start turtle is still visible after been visited
            red.stamp()                 # restamp the red turtle at the start position 

    print(f"The Number of explored nodes: {len(visitedA)}")   


    if is_paused:
        wn.ontimer(lambda: Astarlogic(x, y), 100)  # Schedule the next A star iteration

    if not is_paused:
        backRoute(end_x,end_y)




def backRoute(x, y):
    count = 0
    while (x, y) != (start_x, start_y):    # stop loop when current cells == start cell
        violet.goto(solution[x, y])        # move the violet sprite to the key value of solution ()
        violet.stamp()
        x, y = solution[x, y]               # "key value" now becomes the new key
        count += 1
        print(f"{((x-12)/24, y/24)},")
    print(f"The Length of the Solution is: {count}")



# Function to toggle pause state
def toggle_pause():
    global is_paused
    is_paused = not is_paused

# Function to handle user input
def handle_input():
    wn.onkeypress(toggle_pause, 'p')  # Press 'p' key to pause/unpause
    wn.listen()




def button1():
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    num.place_forget()
    canvas.delete("val")
    dropSelect.place_forget()
    modeSelect.place_forget()
    canvas.create_text(-510, -320, text="Click P to pause           Current Algorithm: BFS", fill="white", font=('Helvetica 15 bold'))
    setup_maze(create_maze_grid(mfile))
    handle_input() 
    BFS(start_x,start_y)



def button2():
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    num.place_forget()
    canvas.delete("val")
    dropSelect.place_forget()
    modeSelect.place_forget()
    canvas.create_text(-510, -320, text="Click P to pause           Current Algorithm: DFS", fill="white", font=('Helvetica 15 bold'))
    setup_maze(create_maze_grid(mfile))
    handle_input() 
    DFS(start_x,start_y)


def button3():
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    num.place_forget()
    canvas.delete("val")
    dropSelect.place_forget()
    modeSelect.place_forget()
    canvas.create_text(-510, -320, text="Click P to pause           Current Algorithm: GBFS", fill="white", font=('Helvetica 15 bold'))
    setup_maze(create_maze_grid(mfile))
    handle_input() 
    GBFS(start_x,start_y)


def button4():
    button1.place_forget()
    button2.place_forget()
    button3.place_forget()
    button4.place_forget()
    num.place_forget()
    canvas.delete("val")
    dropSelect.place_forget()
    modeSelect.place_forget()
    canvas.create_text(-510, -320, text="Click P to pause           Current Algorithm: A Star", fill="white", font=('Helvetica 15 bold'))
    setup_maze(create_maze_grid(mfile))
    handle_input() 
    Astar(start_x,start_y)

def getfile(file):          #get file name selected
    global mfile
    mfile =  (drop.get())

def getinc():            #get increment value selected
    global valInc
    valInc =  (num.get())

def getmode(modeS):
    global modeV
    global is_verbose
    modeV = (mode.get())
    if modeV == 'Verbose':
        is_verbose = True




def main():

    global drop
    global dropSelect
    global modeSelect
    global button1
    global button2
    global button3
    global button4
    global num
    global canvas
    global mode



    canvas = wn.getcanvas()


    button1 = Button(canvas.master, text="BFS", highlightbackground='#5A189A', command=button1)

    button2 = Button(canvas.master, text="DFS", highlightbackground='#5A189A', command=button2)

    button3 = Button(canvas.master, text="GBFS", highlightbackground='#5A189A', command=button3)

    button4 = Button(canvas.master, text="A star", highlightbackground='#5A189A', command=button4)


    canvas.create_text(55,-170, text="Select increment value if using Verbose Mode", fill="white", font=('Helvetica 12'), tag="val")

    num = Spinbox(canvas.master,  bg='white', fg='black', highlightbackground="#5A189A", width=10, from_=0, to=100,increment=10, command=getinc)
    num.pack()
    num.place(x=700, y=200)



    button1.pack()
    button1.place(x=300, y=100)  # place the button on the screen

    button2.pack()
    button2.place(x=400, y=100)  # place the button on the screen

    button3.pack()
    button3.place(x=500, y=100)  # place the button on the screen

    button4.pack()
    button4.place(x=600, y=100)  # place the button on the screen

    
    drop = StringVar(canvas)
    drop.set("Choose Maze") # default value

    dropSelect = OptionMenu(canvas.master, drop, "maze1.txt", "maze2.txt", "maze3.txt", "maze4.txt", command=getfile)
    dropSelect.config(highlightbackground='#5A189A')
    dropSelect.pack()
    dropSelect.place(x=300, y=200)

    mode = StringVar(canvas)
    mode.set("Choose Mode") #default value

    modeSelect = OptionMenu(canvas.master, mode, "Silent", "Verbose", command=getmode )
    modeSelect.config(highlightbackground='#5A189A')
    modeSelect.pack()
    modeSelect.place(x=500, y=200)


    wn.exitonclick()





if __name__ == "__main__":
    main()



























