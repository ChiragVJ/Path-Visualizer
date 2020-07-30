import pygame
import math
from queue import PriorityQueue
import sys
from tkinter import *
from tkinter import messagebox
from pygame.locals import *
import random

pygame.init()
WIDTH = 900  # width of screen
ROWS = 75 #IMPORTANT -- NUMBER OF ACTUAL ROWS DISPLAYED ON THE PYGAME SCREEN 
WIN = pygame.display.set_mode((WIDTH, WIDTH))  # setting width

pygame.display.set_caption("Path Finding Visualizer")  # title

clock = pygame.time.Clock()
clock.tick(144)  ##fps
RED = (255, 0, 0)  ##colours in rgb
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Tile:
    def __init__(self, row, col, width, total_rows):  # constructor
        self.row = row  # all self explanatory
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.visited = False

    def get_pos(self):  # getter
        return self.row, self.col

    def is_closed(self):  # colour assignments
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = YELLOW

    def draw(self, win):  # drawing the actual rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):  # updating neighbours
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):  # heuristic
    x1, y1 = p1
    x2, y2 = p2
    # return abs(x1 - x2) + abs(y1 - y2)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # heuristic calculation


def reconstruct_path(came_from, current, draw):  # used to draw the final shortest path
    while current in came_from:  # while the end node is in the dictonary containing paths
        current = came_from[current]  # go backwards in the dictionary
        current.make_path()
    draw()


def Astar_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}  # keeps track of the previous node
    g_score = {spot: float("inf") for row in grid for spot in
               row}  # dictionary comprehension to make g score of all nodes infinity
    g_score[start] = 0  # starting g node is 0
    f_score = {spot: float("inf") for row in grid for spot in
               row}  # dictionary comprehension to make f score of all nodes infinity
    f_score[start] = h(start.get_pos(), end.get_pos())  # f score of the starting node is equal to the heuristic

    open_set_hash = {start}  # set that keeps track of the item s in queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            Tk().wm_withdraw()
            temp = f_score[end]
            restartMessage = messagebox.askokcancel('A Star Completed', 'Shortest distance is ' + str(temp) +
                                                    ' blocks away, \nWould you like to run the A star algorithm again?')
            if restartMessage:
                restart()
            else:
                mainMenu()

            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # increases g score by one when travelling to neighbour

            if temp_g_score < g_score[neighbor]:  # if g score of current is lower than g score of neighbour
                came_from[neighbor] = current  # update the camefrom to say we came from the previous node
                g_score[neighbor] = temp_g_score  # update g score of neighbour
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(),
                                                     end.get_pos())  # calculate new f score of neighbour using heuristic
                if neighbor not in open_set_hash:  # if neighbour not in hash
                    count += 1  # add to hash so increase counter
                    open_set.put((f_score[neighbor], count, neighbor))  # push new neighbour in
                    open_set_hash.add(neighbor)  # also add to hash
                    neighbor.make_open()  # open all the neighbours

        draw()

        if current != start:  # if the current node is not the start node
            current.make_closed()  # close it as it has been traversed

    return False


def dijkstras_Algorithm(draw, grid, start, end): #most of it follows the same stucture as A star just the neighbours bit is different
    count = 0
    distances_set = PriorityQueue()
    distances_set.put((0, count, start))
    came_from = {}
    # individual_distances = {spot: float("inf") for row in grid for spot in row}
    individual_distances = {spot: float("inf") for row in grid for spot in row}
    individual_distances[start] = 0
    distances_set_hash = {start}

    while not distances_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = distances_set.get()[2]

        distances_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            Tk().wm_withdraw()
            temp = individual_distances[end]
            restartMessage = messagebox.askokcancel('Dijkstra Completed', 'Shortest distance is ' + str(temp) +
                                                    ' blocks away, \nWould you like to run the Dijkstras again?')
            if restartMessage:
                restart()
            else:
                mainMenu()

            return True

        for neighbor in current.neighbors: #for every neighbour of the current node
            temp_node_distance = individual_distances[current] + 1 #increase the distance of the current node by 1

            if temp_node_distance < individual_distances[neighbor]: #if the new temp distance is less than the distance to any of the neighbours
                came_from[neighbor] = current #update the came from list
                individual_distances[neighbor] = temp_node_distance #update the distance of the neighbour to the temp distance

                if neighbor not in distances_set_hash: #if the neighbour isnt in the distance hash
                    count += 1 #increase it
                    distances_set.put((individual_distances[neighbor], count, neighbor)) #add the distance of the new neighbour, count and the actual neighbour itself to the stack 
                    distances_set_hash.add(neighbor) #also add the neighbour to the distances hash
                    neighbor.make_open() #make the neighbour green 
        draw() # draw

        if current != start:
            current.make_closed() #if the current node isnt the start node then close it and make it red 
    return False


def make_grid(rows, width): #making the actual grid and assigning the spot class to each node in the grid 
    global grid
    grid = []
    gap = width // rows #distance between each node visualized, used to allow for a dynamic size
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Tile(i, j, gap, rows) #for every  spot assign it a tile and add it to the grid 
            grid[i].append(spot) 

    return grid


def drawOuterWalls(rows): #draws the outer black walls of the screen to make it look nice 
    global grid
    for i in range(0, rows): 
        grid[0][i].make_wall()
        grid[i][0].make_wall()
        grid[rows - 1][i].make_wall()
        grid[i][rows - 1].make_wall()


def initiateMaze(rows, win): #used to initialize the creation of a maze by clearing screen and setting  all nodes to un visited

    global grid
    restart()
    for i in range(0, rows):
        for j in range(0, rows):
            # print(i)
            grid[i][j].make_wall()
            grid[i][j].visited = False


    dfs(rows, win) #run dfs


def dfs(rows, win):
    global grid

    currentX = random.randrange(1,rows-1,2) # generate random x and y values between 1 and the rows-2 (the outer limit of the grid)
    currentY = random.randrange(1,rows-1,2)
    grid[currentX][currentY].visited = True #mark the cuurrent node in the grid as visited
    grid[currentX][currentY].reset() #reset the current node so its white
    dfs_stack = [] #stack to store coordinates
    dfs_stack.append(currentY)  #append the Y coordinate then X coordinate so when we pop the coordinates we pop them in reverse order 
    dfs_stack.append(currentX)
    while dfs_stack:
        #draw(win,grid,rows,WIDTH)
        if (currentX > 1  and (grid[currentX - 2][currentY].visited == False) or 
                (currentX < rows -2 and grid[currentX + 2][currentY].visited == False) or
                (currentY > 1 and grid[currentX][currentY - 2].visited == False) or
                (currentY < rows  -2 and grid[currentX][currentY + 2].visited == False)): #if any of the neighbouring nodes are unvisited and also inbounds
 

            direction = random.randint(1, 4) #generate a number to represent a direction IE up down left right
            if direction == 1 and currentY > 1: # GOING UP
                if not grid[currentX][currentY - 2].visited: #if the node above isnt visited
                    grid[currentX][currentY - 1].reset() #break the wall
                    grid[currentX][currentY - 1].visited = True #mark the wall as visited
                    dfs_stack.append(currentY) #add coordinates to stack
                    dfs_stack.append(currentX)
                    currentY -= 2 # move to next node
                    grid[currentX][currentY].visited = True # mark 'next node' as visited
                    grid[currentX][currentY].reset() #reset 'next node' to make it white  


                else:
                    continue 
            if direction == 2 and currentY < rows - 2: #GOING DOWN
                if not grid[currentX][currentY + 2].visited:
                    grid[currentX][currentY + 1].reset()
                    grid[currentX][currentY + 1].visited = True
                    dfs_stack.append(currentY)
                    dfs_stack.append(currentX)
                    currentY += 2
                    grid[currentX][currentY].visited = True
                    grid[currentX][currentY].reset()

                else:
                    continue
            if direction == 3 and currentX > 1: # GOING LEFT
                if not grid[currentX - 2][currentY].visited:
                    grid[currentX - 1][currentY].reset()
                    grid[currentX - 1][currentY].visited = True
                    dfs_stack.append(currentY)
                    dfs_stack.append(currentX)
                    currentX -= 2
                    grid[currentX][currentY].visited = True
                    grid[currentX][currentY].reset()

                else:
                    continue
            if direction == 4 and currentX < rows - 2: # GOING RIGHTT
                if not grid[currentX + 2][currentY].visited:
                    grid[currentX + 1][currentY].reset()
                    grid[currentX + 1][currentY].visited = True
                    dfs_stack.append(currentY)
                    dfs_stack.append(currentX)
                    currentX += 2
                    grid[currentX][currentY].visited = True
                    grid[currentX][currentY].reset()

                else:
                    continue
        else:
            currentX = dfs_stack.pop()
            currentY = dfs_stack.pop()


def restart():
    global start
    global end
    global grid
    start = None
    end = None
    grid = make_grid(ROWS, WIDTH) # clear screen 


def draw(win, grid, rows, width): #draw to pygame screen 
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    drawOuterWalls(rows)
    pygame.display.update() 


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def initiateMouse(win, width, algo):
    global ROWS
    global grid
    grid = make_grid(ROWS, width)
    global start
    global end
    start = None
    end = None
    run = True
    while run: #while the game is running 
        draw(win, grid, ROWS, width) #draw to screen 
        for event in pygame.event.get(): #grab pygame event
            if event.type == pygame.QUIT: #if quit is recorded then make run = false to break out of loop
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) #grab position of the mouse click
                spot = grid[row][col] # assign it a spot 


                if not start and spot != end:
                    start = spot 
                    start.make_start() #if there is no start then make the position clicked the starting node

                elif not end and spot != start:
                    end = spot
                    end.make_end() #if there is no end but there is a start then make the position clicked the ending node

                elif spot != end and spot != start:
                    spot.make_wall() #if both start and end exists then make the click spawn a wall 

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) #grab position of click 
                spot = grid[row][col]
                spot.reset() #reset the node at the position of the click 
                if spot == start:
                    start = None #if the click is registed on the starting node, then assign startt to NONE
                elif spot == end: # if the click is registered on the ending node, then assign end to NONE 
                    end = None

            if event.type == pygame.KEYDOWN: #if key press

                if event.key == pygame.K_SPACE and start and end: #if the start and end exists and space is clicked 
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) #update the neighbours in  the grid so the algorithm can work
                    if algo == 0:

                        Astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) #call A star with lambda draw function and arguments 
                    elif algo == 1:
                        dijkstras_Algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # call dijkstras with lambda draw function and arguments
                if event.key == pygame.K_c:
                    restart() # if c is pressed then clear the screen
                if event.key == pygame.K_m:
                    mainMenu() #if m is pressed then return to the main menu
                if event.key == pygame.K_a:
                    initiateMaze(ROWS, win)  #if a is pressed then draw a maze 
            

    pygame.quit()


def draw_text(text, font, color, surface, x, y): #used to draw text to the scren 
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# pygame.display.update()

def font_size(size): # used to change font size easily
    font = pygame.font.SysFont(None, size)
    return font


def mainMenu(): # the actual main menu 
    click = False
    while True:
        WIN.fill(WHITE)
        draw_text('Main menu', font_size(50), BLACK, WIN, 40,
                  40)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        button_3 = pygame.Rect(700, 700, 70, 40)

        if button_1.collidepoint((mx, my)): #if the postion in which the mouse clicks then run the algorithms depending on what was clicked 
            if click:
                initiateMouse(WIN, WIDTH, 0)
                pass
        if button_2.collidepoint((mx, my)):
            if click:
                initiateMouse(WIN, WIDTH, 1)
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
        pygame.draw.rect(WIN, RED, button_1)
        pygame.draw.rect(WIN, RED, button_2)
        pygame.draw.rect(WIN, RED, button_3)
        draw_text('A Star path finding', font_size(25), BLACK, WIN, 60, 115)
        draw_text('Dijkstra path finding', font_size(25), BLACK, WIN, 60, 215)
        draw_text('Press "A" to draw a maze', font_size(25), BLACK, WIN, 60, 515)
        draw_text('Press "C" to clear the screen', font_size(25), BLACK, WIN, 60, 535)
        draw_text('Press "M" to go to the Main Menu', font_size(25), BLACK, WIN, 60, 555)
        draw_text('Use left click to place the start and end positions and to place walls', font_size(25), BLACK, WIN, 60, 575)
        draw_text('Use right click to erase walls or the starting and ending positions', font_size(25), BLACK, WIN, 60, 595)
        draw_text('Press ESC at any time to close the program', font_size(25), BLACK, WIN, 60, 615)
        draw_text('Press SPACE once placing the start and end to begin visualisation', font_size(25), BLACK, WIN, 60, 635)
        draw_text('QUIT', font_size(30), BLACK, WIN, 710, 710)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


mainMenu()
