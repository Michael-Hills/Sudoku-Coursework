"""Module to solve an 8-Puzzle using an A* Search Algorithm"""

#Used for the 2D array to store the grid
import numpy as np

class Node():
    """A Class to represent a node in the graph for the algorithm

    Attributes
    ----------

    parent: Node
        the parent node of a node

    grid: 2D Array
        the arrangement of the tiles in the game

    f: int
        the result of the f function (cost of reaching node + heuristic)

    g: int
        the cost to get to this current node"""


    def __init__(self, parent, grid, f = 0, g=0):
        """Method to construct a node object"""
        self.parent = parent
        self.grid = grid
        self.f = f
        self.g = g



def get_start():

    """Function to get the starting grid for the game"""


    # Enter the string in command line and convert to list
    grid = input("\nEnter starting grid in the form of the numbers on the puzzle \nseperated by commas and the blank square as an _:\n\n")
    dim_grid = list()

    # Keep looping until correct format
    while(True):

        grid_list = grid.split(',')

        # Must be numbers 1-8 and a _
        if len(grid_list) != 9:
            grid = input("Wrong format. Please enter in correct format:\n\n")
            continue

        if set(grid_list) == set(['1','2','3','4','5','6','7','8','_']):
            dim_grid = np.array([grid_list[0:3],
                                grid_list[3:6],
                                grid_list[6:10]])
            break
        else:
            grid = input("Wrong format. Please enter in correct format:\n\n")
            continue

    return dim_grid


def get_end():

    """Function to get the end grid from command line"""


     # Enter the string in command line and convert to list
    grid = input("\nEnter goal in the same format as the starting grid:\n\n")
    dim_grid = list()

     # Keep looping until correct format
    while(True):

        grid_list = grid.split(',')

        # Must be numbers 1-8 and a _
        if len(grid_list) != 9:
            grid = input("Wrong format. Please enter in correct format:\n\n")
            continue

        if set(grid_list) == set(['1','2','3','4','5','6','7','8','_']):
            dim_grid = np.array([grid_list[0:3],
                                grid_list[3:6],
                                grid_list[6:10]])
            break
        else:
            grid = input("Wrong format. Please enter in correct format:\n\n")
            continue

    return dim_grid


def manhattan(grid,goal):

    """Function to calculate the manhattan distance to the goal state

       Parameters
       ----------
       grid - 2D array representing the current position of tiles in the game
       goal - 2D array representing the position of the tiles in the goal state"""

    # If the node does not have a grid, set manhattan to 1000 as this will never get picked
    if grid is None:
        return 1000
    else:
        total = 0

        # Go through each numbe tile and add manhattan distance
        # to its correct position to the total
        for i in range(8):

            cur_loc = np.argwhere(grid == str(i+1))
            goal_loc = np.argwhere(goal == str(i+1))

            total += abs(cur_loc[0][0] - goal_loc[0][0]) +  abs(cur_loc[0][1] - goal_loc[0][1])

        return total



def getChildren(parent):
    """Function to get the child nodes of the current node

       Parameters
       ----------
       parent - Node object of the parent node of the children to be generated"""

    children = []

    # Create a copy so the parent node isnt changed
    newgrid = parent.grid.copy()

    # Finc current positionin the grid of the _
    current = np.argwhere(newgrid == '_')
    x = current[0][0]
    y = current[0][1]


    # The child node for the blank tile to move left
    newgrid = parent.grid.copy()
    if y != 0:
        newgrid[x][y], newgrid[x][y-1] = newgrid[x][y-1], newgrid[x][y]
        children.append(Node(parent,newgrid))
    else:
        children.append(None)

    # The child node for the blank tile to move right
    newgrid = parent.grid.copy()
    if y != 2:
        newgrid[x][y], newgrid[x][y+1] = newgrid[x][y+1], newgrid[x][y]
        children.append(Node(parent,newgrid))
    else:
        children.append(None)

    # The child node for the blank tile to move up
    newgrid = parent.grid.copy()
    if x != 0:
        newgrid[x][y], newgrid[x-1][y] = newgrid[x-1][y], newgrid[x][y]
        children.append(Node(parent,newgrid))
    else:
        children.append(None)

    # The child node for the blank tile to move down
    newgrid = parent.grid.copy()
    if x != 2:
        newgrid[x][y], newgrid[x+1][y] = newgrid[x+1][y], newgrid[x][y]
        children.append(Node(parent,newgrid))
    else:
        children.append(None)


    return children



def get_path(end_node):

    """Function to backtrack through the graph once a solution is found

       Parameters
       ----------
       end_node - Node object of the final node returned by main (the solution)"""

    nodes = []
    node = end_node
    nodes.append(node)

    # Keep looping whilst a parent node exists
    while (True):
        parent = node.parent
        if (parent is not None):
            nodes.append(parent)
            node = parent
        else:
            nodes.reverse()
            # Print the nodes in order from root to leaves
            for i in nodes:
                print("   |   ")
                print("   |   ")
                print("   |   ")
                print("   V   ")
                print(i.grid)

            break




# Main function that runs the other functions
if __name__ == "__main__":

    # List of nodes in the graph that have not been visited
    open = []
    # List of nodes in the graph that have been visited
    closed = []


    # Create start and end grids
    start_grid = get_start()
    end_grid = get_end()

    # Create start node and add to open list
    start_node = Node(None,start_grid)
    open.append(start_node)

    # Loop until solved or no nodes left to visit
    count = 0
    while (len(open) > 0):
        if len(open) == 0:
            print("Unsolvable")
            exit(0)
        count += 1

        # Pick the node in open with smallest F value, remove from open and add to closed
        q = min(open, key=lambda node: node.f)
        open.remove(q)
        closed.append(q)

        # If we have the solution, Stop
        if (q.grid == end_grid).all():
            print("Nodes Visited: ", count)
            get_path(q)
            exit(1)

        # Get the children of the current node
        children = getChildren(q)

        # Loop through children
        for child in children:
            if child is not None:

                add = True

                # If child nodes grid has already been seen in a node in closed list, dont add to open
                for c in closed:
                    if (c.grid == child.grid).all():
                        add = False
                        break

                if add == False:
                    continue

                # Set the g and f values of the child
                child.g = q.g + 1
                child.f = child.g + manhattan(child.grid,end_grid)


                # If childs grid already seen in open list list, and the g value is larger in new child node
                for o in open:
                    if (o.grid == child.grid).all():
                        if child.g > o.g:
                            add = False
                            break

                # Else add child to open
                if add == True:
                    open.append(child)
