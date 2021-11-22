'''This a Path finder Visualizer and this contain A-star , DFS, and Floodfill algorithm for finding shortest path'''

# Importing pygame bcs this run in pygame
import pygame
# importing Priority Queue for A* algorithm
from queue import PriorityQueue

# Initializing pygame font
pygame.font.init()

# Screen Resolution of a side
SIDE = 800

# Pygame Display
WIN = pygame.display.set_mode((SIDE, SIDE))
pygame.display.set_caption("A* path finder")

# colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Class for a cell


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.colour = WHITE
        self.neighbours = []
        self.total_rows = total_rows
        self.number = 0  # for floodfill algorithm
        self.check = False  # for floodfill algorithm

# Getiing the position of node
    def get_pos(self):
        return self.row, self.col

# check if this cell is checked
    def is_closed(self):
        return self.colour == RED

# checking this cell is in checking
    def is_open(self):
        return self.colour == GREEN

# check is this cell is a wall
    def is_barrier(self):
        return self.colour == BLACK

# check is this cell is start node
    def is_start(self):
        return self.colour == ORANGE

# check is this cell is end note
    def is_end(self):
        return self.colour == TURQUOISE

# reset all the cells to initial
    def reset(self):
        self.colour = WHITE

# make the cell is checked
    def make_closed(self):
        self.colour = RED

# make the cell as checking cell
    def make_open(self):
        self.colour = GREEN

# make the cell as wall
    def make_barrier(self):
        self.colour = BLACK

# make the cell as start node
    def make_start(self):
        self.colour = ORANGE

# make the cell as end note
    def make_end(self):
        self.colour = TURQUOISE

# make this cell as a node of shortest path
    def make_path(self):
        self.colour = PURPLE

# drawing the cell
    def draw(self, window):
        pygame.draw.rect(
            window,
            self.colour,
            (self.x,
             self.y,
             self.width,
             self.width))

# updating neighbours list (check the limit of screen and is neighbor cell
# is a barrier)
    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - \
                1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row -
                                     1][self.col].is_barrier():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col -
                                               1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - \
                1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

# if node was check with each other always return False
    def __lt__(self, other):
        return False

# finding manhattance distance for A* algorithm (Guess function)


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

# make the two dimensional matrix contains Node objects


def make_grid(rows, width):
    grid = []
    gap = width // rows  # side length of a node

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

# visualizing the grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# drawing the allthe things want to draw


def draw(win, grid, rows, width, algo):
    win.fill(WHITE)
    # for A* and DFS part
    if algo:
        for row in grid:
            for node in row:
                node.draw(win)

    # for Floodfill Algorithm
    elif not algo:
        fon = pygame.font.SysFont('comicsans', 500 // rows)
        for row in grid:
            for node in row:
                node.draw(win)
                number = node.number
                fon_label = fon.render(f"{number}", 1, BLACK)
                WIN.blit(fon_label,
                         (node.x + (width // rows) // 2 - fon_label.get_width() / 2,
                          node.y + (width // rows) // 2 - fon_label.get_height() / 2))

    # drawing the grid
    draw_grid(win, rows, width)
    pygame.display.update()

# After finding the path in A* reconstructing the path from dictionary


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# A* Algorithm


def A_star(draw, grid, start, end):
    count = 0  # keep a count for find order which the node is put to queue
    # making the piority queue for choose most priortise from the queue
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # putting first element to priority queue
    # g-score is distance from current node to searching node , making all inf
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0  # making fist element distance to zero
    # f_score = G_score + H_score
    f_score = {node: float("inf") for row in grid for node in row}
    # making first element f_score to H_score
    f_score[start] = h(start.get_pos(), end.get_pos())

    came_from = {}  # keeping a dictionary for to keep track of from which node can go to current node

    open_set_hash = {start}  # open_set for keep track of considering nodes

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # taking the most priortised node
        open_set_hash.remove(current)  # and deleting that from open_set

        if current == end:  # make a path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:

            # distance to cell to another cell is 1
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:

                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = g_score[neighbour] + \
                    h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()  # drawing the path and search
        if current != start:
            current.make_closed()

    return False

# get the row and col of a position


def get_clicked(pos, rows, width):
    gap = width // rows

    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# Depth first search algorithm


def DFS(grid, start, end, draw):
    '''Not efficient after 7*7 grid, I think because its finding all the possible path and it's like a brute force method'''
    queue = [[]]  # keeping track of all the possible roots
    current = start  # keep the first node as start
    pop_item = queue.pop(0)  # get the first item from queue
    while current != end:  # loop through until it find the end node
        # Update neighbours of the current cell
        current.update_neighbours(grid)
        neighbours = current.neighbours  # take the neighbours as list
        for neighbor in neighbours:  # loop through all  neighbour list
            if not neighbor.check:  # check if neighbour is look before in a path
                path = pop_item + [neighbor]  # long the path by neighbour
                queue.append(path)
        pop_item = queue.pop(0)
        current = pop_item[-1]

    # draw the path of DFS
    for node in pop_item:
        node.make_path()
        draw()

# Flood fill algorithm


def floodfill(grid, start, end):
    '''I think most efficient for mazes'''
    numberd_di = {0: [end]}  # keep track of the which numbers own which node
    # keeping all the node in a list
    def flatten(l): return [item for sublist in l for item in sublist]
    number = 0
    end.check = True  # to not cheange the number of End node
    while start not in flatten(
            numberd_di.values()):  # while start not in the dictionry loop through

        '''Below code is doing check the available neighbours and giving them a number above than curent cell this is run untill its find the start node'''

        for node in numberd_di[number]:
            node.update_neighbours(grid)
            neighbours = node.neighbours
            for neighbour in neighbours:
                if not neighbour.check:
                    neighbour.number = number + 1
                    if numberd_di.get(neighbour.number, None) is not None:
                        numberd_di[neighbour.number].append(neighbour)
                    else:
                        numberd_di[neighbour.number] = [neighbour]
                    neighbour.check = True
        number += 1
    return numberd_di

# Reconstruct the path from floodfill data


def floodfill_solve(grid, start, numberd_di, draw):
    path = [start]  # start from start node
    keys = list(numberd_di.keys())  # taking the only numbers
    keys.reverse()  # reversing the numbers bcz we start from start nodes
    for key in keys[1:]:  # without start node

        '''Below Code is doing getting a number and finding the nodes which belongs to that number and checking from those cell which is the nighbour and number below 1 is from current cell and keep doign that until it find end node'''

        for node in numberd_di[key]:
            last_member = path[-1]
            last_member.update_neighbours(grid)
            neighbours = last_member.neighbours
            if node in neighbours and node.number == last_member.number - 1:
                path.append(node)

    # Darwing the path
    for key in path:
        key.make_path()
        draw()

# Pathfinder main Function


def main(win, width):
    # how much size of a maze do we want ? (If size is > 7 don't press d
    # button)
    ROWS = 8

    # keeping variable for start and end node
    start = None
    end = None

    # making the grid
    grid = make_grid(ROWS, width)

    # variables for game running and
    run = True
    algo = True

    while run:
        # draw the display of grid and nodes
        draw(win, grid, ROWS, width, algo)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, width)
                node = grid[row][col]

                # making first touch of cell as start
                if not start and node != end:
                    start = node
                    node.make_start()

                # making second touch of cell as end
                elif not end and node != start:
                    end = node
                    node.make_end()

                # making any other touch of cell as walls
                elif node != end and node != start:
                    node.make_barrier()

            # clicking the second mouse button deleting the cells
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_a and start and end:  # pressing the a button run the a star algo

                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    algo = True
                    A_star(
                        lambda: draw(
                            win,
                            grid,
                            ROWS,
                            width,
                            algo),
                        grid,
                        start,
                        end)

                if event.key == pygame.K_f and start and end:  # pressing the f button will run the floodfill algo
                    algo = False
                    num = floodfill(grid, start, end)
                    floodfill_solve(
                        grid, start, num, lambda: draw(
                            win, grid, ROWS, width, algo))

                if event.key == pygame.K_d and start and end:  # pressing the d button will run DFS algo
                    algo = True
                    DFS(grid, start, end, lambda: draw(
                        win, grid, ROWS, width, algo))

                if event.key == pygame.K_c:  # pressing the c button clear the grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, SIDE)  # calling main function
