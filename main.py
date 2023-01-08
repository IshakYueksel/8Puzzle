import heapq
import random
from copy import deepcopy
from time import time

"""
Inspired by github user rickybassom
https://github.com/rickybassom/8-puzzle-problem-solver
"""
class PriorityQueue:                                # Class for creating a PriorityQueue
    def __init__(self):                             # Initializing
        self.heap = []
        self.count = 0                              # Setting heap count to 0

    def push(self, item, priority):                 # Adding element to queue
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):                                  # Removing element from queue
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):                              # Clearing heap
        return len(self.heap) == 0


class Grid:                                         # Class for creating the playgrid
    n = 0                                                                                   # Variable for keeping track of nodes

    def __init__(self, nodes, node_positions=None, last_move=None, parent=None):
        Grid.n += 1                                                                         # Tracking nodecount
        self.last_move = last_move
        self.nodes = nodes
        N = len(self.nodes)

        if node_positions == None:
            self.node_positions = {}                                                        # stores node position (x, y)
            for y in range(N):
                for x in range(N):
                    self.node_positions[self.nodes[y][x]] = (y, x)
        else:
            self.node_positions = node_positions

        self.g = 0
        self.parent = parent

        if self.parent: self.g = self.parent.g + 1

    def swap_values(self, tile1_pos, tile2_pos):                                            # swapping nodes
        temp = self.nodes[tile1_pos[0]][tile1_pos[1]]
        self.nodes[tile1_pos[0]][tile1_pos[1]] = self.nodes[tile2_pos[0]][tile2_pos[1]]
        self.nodes[tile2_pos[0]][tile2_pos[1]] = temp

        self.node_positions[self.nodes[tile1_pos[0]][tile1_pos[1]]] = (tile1_pos[0], tile1_pos[1])
        self.node_positions[self.nodes[tile2_pos[0]][tile2_pos[1]]] = (tile2_pos[0], tile2_pos[1])

    def swipes_that_change_board_config(self):
        swipes = ["up", "down", "left", "right"]
        blank_tile_ypos, blank_tile_xpos = self.node_positions[0]

        if blank_tile_ypos + 1 > len(self.nodes) - 1: swipes.remove("up")
        if blank_tile_ypos - 1 == -1: swipes.remove("down")

        if blank_tile_xpos + 1 > len(self.nodes) - 1: swipes.remove("left")
        if blank_tile_xpos - 1 == -1: swipes.remove("right")
        return swipes

    def next_move(self, swipe_direction):
        blank_tile_ypos, blank_tile_xpos = self.node_positions[0]
        if swipe_direction not in self.swipes_that_change_board_config():
            print("move results in no change")
            return
        elif (swipe_direction == "up"):
            self.swap_values((blank_tile_ypos, blank_tile_xpos), (blank_tile_ypos + 1, blank_tile_xpos))
        elif (swipe_direction == "down"):
            self.swap_values((blank_tile_ypos, blank_tile_xpos), (blank_tile_ypos - 1, blank_tile_xpos))
        elif (swipe_direction == "right"):
            self.swap_values((blank_tile_ypos, blank_tile_xpos), (blank_tile_ypos, blank_tile_xpos - 1))
        elif (swipe_direction == "left"):
            self.swap_values((blank_tile_ypos, blank_tile_xpos), (blank_tile_ypos, blank_tile_xpos + 1))


    def get_child_boards(self):
        child_boards = []
        for swipe in self.swipes_that_change_board_config():
            child = Grid(deepcopy(self.nodes), node_positions=self.node_positions.copy(), parent=self, last_move=swipe)
            child.next_move(swipe)
            child_boards.append(child)

        return child_boards


    def __eq__(self, other):
        return self.nodes == other.nodes

    def __hash__(self):
        return hash(str(self.nodes))

    def __str__(self):
        return '\n'.join([' '.join(str(tile) if tile != 0 else " " for tile in aa) for aa in self.nodes])


class Game():
    def __init__(self, start_state, goal_state):
        self.start_state = Grid(nodes=start_state)
        self.goal_state = Grid(nodes=goal_state)

        print("Loaded start state")
        print(self.start_state)
        print("Loaded goal state")
        print(self.goal_state)
        print()

    def manhattan_distance_heuristic(self, grid1, grid2):               # Manhattan heuristic
        sum = 0
        for y in range(len(grid1.nodes)):
            for x in range(len(grid1.nodes)):
                if grid1.nodes[y][x] == 0: continue  # skip blank tile

                goal_state_tile = grid2.node_positions[grid1.nodes[y][x]]
                sum += abs(y - goal_state_tile[0]) + abs(x - goal_state_tile[1])

        return sum

    def num_misplaced_tiles_heuristic(self, grid1, grid2):              # Hamming heuristic
        count = 0
        for y in range(len(grid1.nodes)):
            for x in range(len(grid1.nodes)):
                if grid1.nodes[y][x] == 0: continue  # skip blank tile

                if grid1.nodes[y][x] != grid2.nodes[y][x]:
                    count += 1

        return count

    def solve(self, h_function):                                            # h_function chosen heuristic
        """
        A* algorithm

        """
        open_set = PriorityQueue()                                          # stored ordered nodes by f value
        f = h_function(self.start_state, self.goal_state) + self.start_state.g
        open_set.push(self.start_state, f)
        closed_set = set()

        found = False
        while not open_set.isEmpty():
            current = open_set.pop()

            if current == self.goal_state:
                found = current
                break

            if current in closed_set:
                continue

            closed_set.add(current)

            for child in current.get_child_boards():
                f = h_function(child, self.goal_state) + child.g
                open_set.push(child, f)

        if found:
            path = []
            while found:
                path.append(found)
                found = found.parent
            path.reverse()

            print("Solution found")
            return path
        else:
            print("No solution found")


def grid(S, i):
     if i == 1:
        print("Enter grid seperated by single spaces (use zero as a space) and press enter to input new row")
        arr2d = [[int(j) for j in input().strip().split(" ")] for i in range(S)]            #Creating your own Grid
        print(arr2d)
        return arr2d
     elif i == 2:                                                                           #Creating a randomized Grid
         a = random.sample(range(0, 3), 3)
         b = random.sample(range(3, 6), 3)
         c = random.sample(range(6, 9), 3)
         lst = []
         i = random.randint(0, 2)

         if i == 0:
             lst.append(a)
             lst.append(b)
             lst.append(c)
         elif i == 1:
             lst.append(b)
             lst.append(a)
             lst.append(c)
         elif i == 2:
             lst.append(c)
             lst.append(b)
             lst.append(a)
         return lst


if __name__ == "__main__":
    example_start_state = [
        [7, 2, 4],
        [5, 0, 6],
        [8, 3, 1]
    ]

    example_goal_state = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8]
    ]


    while True:
        S = 3
        break
    gametype = input("Type 1 for a single game with custom start and end grids or type 2 for 100 randomly generated games\n")
    if gametype == "1":
        print("Enter start grid")
        start_grid = grid(S, 1)                                         #Creating start grid
        print()
        print("Enter end grid")
        goal_grid = grid(S, 1)                                          #Creating goal grid
        game = Game(start_grid, goal_grid)                              #Initializing Game
        while True:
            which_h = input("Hamming heuristic (1) or Manhattan distance heuristic (2)? ")
            if which_h in ["1", "2"]:
                break
            print('Please enter 1 or 2')

            print("Processing")
            print()

        if which_h == "1":
            start_time = time()
            path = game.solve(game.num_misplaced_tiles_heuristic)       #Starting Game with hamming heurisitc
            end_time = time()
        else:
            start_time = time()
            path = game.solve(game.manhattan_distance_heuristic)        #Starting Game with manhattan heuristic
            end_time = time()


        print(end_time - start_time, "seconds to solve")
        print(Grid.n, "nodes created")
    if gametype == "2":

        while True:
            which_h = input("Number of misplaced tiles heuristic (1) or Manhattan distance heuristic (2)? ")
            if which_h in ["1", "2"]:
                break
            print('Please enter 1 or 2')

            print("Processing")
            print()

        if which_h == "1":
            start_time = time()
            for k in range(100):                                            #100 Random Games with hamming heuristic
                start_grid = grid(S, 2)
                goal_grid = grid(S, 2)
                game = Game(start_grid, goal_grid)
                path = game.solve(game.num_misplaced_tiles_heuristic)
            end_time = time()
        else:
            start_time = time()
            for m in range(100):                                            #100 Random Games with Manhattan heurisitc
                start_grid = grid(S, 2)
                goal_grid = grid(S, 2)
                game = Game(start_grid, goal_grid)
                path = game.solve(game.manhattan_distance_heuristic)
            end_time = time()


        print(end_time - start_time, "seconds to solve")
        print(Grid.n, "nodes created")