"""Module to solve soduku using an evolutionary algorithm"""

#Used to create a 2D array
import numpy as np
import time as t


class Node():

    """A Class to represent a node in the graph for the algorithm

    Attributes
    ----------

    grid: list
        list representing the numbers in the soduku board

    fitness: int
        the value of the fitness function for this node

    """

    def __init__(self,grid,fitness):
        """Method to construct a node object"""
        self.grid = grid
        self.fitness = fitness

def getProblem():

    """Function to get the starting soduku board a file"""

    f = open("Grid2.ss", "r").read().splitlines()
    grid = []
    for line in f:
        for i in line:
            # add 0 if not prefilled, the number if prefilled
            if i == '.':
                grid.append(0)
            elif i == '!':
                pass
            elif i == '-':
                continue
            else:
                grid.append(int(i))

    return grid

def fillGrid(grid):

    """Function to initially fill the soduku board

       Parameters
       ----------
       grid - a list containing the starting board with blank spaces as 0s"""

    filledGrid = grid.copy()

    for i in range(81):

        if i % 9 == 0:
            # get all available numbers that arent already used in a row
            set = filledGrid[i:i+9]
            available = []
            for num in range(9):
                if num+1 not in set:
                    available.append(num+1)

        if filledGrid[i] == 0:
            # fill in empty cells with numbers that are available
            if len(available) > 1:
                r = np.random.randint(0,len(available))
            else:
                r = 0

            filledGrid[i] = available[r]
            available.remove(filledGrid[i])

    return filledGrid



def getBoolGrid(grid):

    """Function to create a grid of 1s and 0s to be used to know which cells
       cannot be changed as they are prefilled

       Parameters
       ----------
       grid - a list containing the starting board with blank spaces as 0s"""

    boolGrid = []
    for i in range(81):
        if grid[i] != 0:
            boolGrid.append(0)
        else:
            boolGrid.append(1)

    return boolGrid



def fitness(grid):

    """Function to calculate the fitness value of a grid

       Parameters
       ----------
       grid - a list containing the current soduku grid"""

    total = 0

    twoArray = np.reshape(grid,(-1,9))
    for i in range(9):
        j,k = (i//3) * 3, (i%3) * 3
        # calculate unique numbers in row
        total += len(set(twoArray[i,:]))
        # calculate unique numbers in column
        total += len(set(twoArray[:,i]))
        # calculate unique numbers in subgrid
        total +=  len(set(twoArray[j:j+3,k:k+3].ravel()))

    return total

def crossover(node1,node2):

    """Function to perform the crossover functions

       Parameters
       ----------
       node1, node2 - the two grids to perform the crossover function on"""


    # copy so doesnt change original grid
    grid1 = node1.copy()
    grid2 = node2.copy()

    # pick random crossover function
    option = np.random.randint(1,4)

    # single row crossover
    if option == 1:

        row = np.random.randint(0,9)
        temp = grid1.copy()
        grid1[row*9:row*9+9] = grid2[row*9:row*9+9]
        grid2[row*9:row*9+9] = temp[row*9:row*9+9]

    # all rows from random point in grid
    elif option == 2:

        subgrid = np.random.randint(1,9)
        temp = grid1.copy()

        grid1[subgrid*9:] = grid2[subgrid*9:]
        grid2[subgrid*9:] = temp[subgrid*9:]


    # randomly choose swap rows or not
    else:
        temp = grid1.copy()
        for i in range(9):
            num = np.random.randint(1,3)
            if num == 1:
                grid1[i*9:i*9+9] = grid2[i*9:i*9+9]
                grid2[i*9:i*9+9] = temp[i*9:i*9+9]


    # decide to mutate or not
    prob = np.random.randint(0,101)/100

    if prob < 0.7:
        grid1 = mutate(grid1)

    prob = np.random.randint(0,101)/100

    if prob < 0.7:
        grid2 = mutate(grid2)



    return grid1,grid2


def mutate(grid):

    """Function to mutate a grid

       Parameters
       ----------
       grid - a list containing the current soduku grid"""

    # swap 2 numbers in a row
    while count != 1:
        row = np.random.randint(0,9)
        cell1 = np.random.randint(0,9)
        cell2 = np.random.randint(0,9)
        if cell1 != cell2:
            if boolGrid[row*9 + cell1] == 1 and boolGrid[row*9 + cell2] == 1:
                grid[row*9 + cell1], grid[row*9 + cell2] = grid[row*9 + cell2], grid[row*9 + cell1]
                break

    return grid


def printSolution(grid):

    """Function to print the solved grid

       Parameters
       ----------
       grid - a list containing the soduku grid"""

    # convert to 2d array and print
    twoArray = np.reshape(grid,(-1,9))
    print(twoArray)


def repopulate():

    """Function to reill the population after selection

    """

    # keep going until population is refilled
    while len(nodes) != population:

        parent1 = np.random.randint(0,len(nodes)-1)
        while True:
            parent2 = np.random.randint(0,len(nodes)-1)
            if parent1 != parent2:
                break


        grid1, grid2 = crossover(nodes[parent1].grid,nodes[parent2].grid)


        # if fitness of 243, print solution and end
        if fitness(grid1) == 243:
            printSolution(grid1)
            end = t.time()
            print(end-start)
            exit(0)

        elif fitness(grid2) == 243:
            printSolution(grid2)
            end = t.time()
            print(end-start)
            exit(0)

        nodes.append(Node(grid1,fitness(grid1)))
        nodes.append(Node(grid2,fitness(grid2)))



if __name__ == "__main__":

    start = t.time()

    initGrid = getProblem()
    boolGrid = getBoolGrid(initGrid)

    # choose population size

    print("1: 10")
    print("2: 100")
    print("3: 1000")
    print("4: 10,000")
    num = input("Please enter the corresponing number to select the population: ")


    while num not in ['1','2','3','4']:
        num = input("Invaild entry. Please enter number between 1 and 4.")

    num = int(num)

    if num == 1:
        population = 10
    elif num == 2:
        population = 100
    elif num == 3:
        population = 1000
    else:
        population = 10000


    percent = int(population*0.4)
    nodes = []

    # keep looping until optimal solution
    while len(nodes) != population:
        filledGrid = fillGrid(initGrid)
        nodes.append(Node(filledGrid,fitness(filledGrid)))

    count = 0

    while True:


        # sort by fitness, and print best
        nodes.sort(key=lambda x: x.fitness, reverse=True)

        print(count, ": ", nodes[0].fitness)

        # split population into 4 groups, depending on fitness
        selection = []
        selection.append(nodes[0:int(population*0.1)])
        selection.append(nodes[int(population*0.1):int(population*0.3)])
        selection.append(nodes[int(population*0.3):int(population*0.6)])
        selection.append(nodes[int(population*0.6):population])


        # add top 10%
        nodes = selection[0]


        # go through and select nodes to go through to next generation,
        # with more probability of being the ones with better fitness
        while len(nodes) != percent:
            num = np.random.randint(0,10)
            if num < 5 and len(selection[1]) > 0:

                num2 = np.random.randint(0,len(selection[1]))
                nodes.append(selection[1][num2])
                selection[1].pop(num2)

            elif num >=5 and num <8 and len(selection[2]) > 0:

                num2 = np.random.randint(0,len(selection[2]))
                nodes.append(selection[2][num2])
                selection[2].pop(num2)

            elif num >=8 and len(selection[3]) > 0:
                num2 = np.random.randint(0,len(selection[3]))
                nodes.append(selection[3][num2])
                selection[3].pop(num2)


        repopulate()

        count += 1
