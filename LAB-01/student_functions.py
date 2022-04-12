from queue import PriorityQueue
import math


def convertMatrixToAdjacencyMatrixDict(matrix):
    result = {}
    for i in range(0, len(matrix)):
        result[i] = []
        for j in range(0, len(matrix)):
            if(matrix[i][j] != 0):
                result[i].append(j)
    return result


def convertMatrixToAdjacencyMatrixDictWeight(matrix):
    result = {}
    for i in range(0, len(matrix)):
        result[i] = []
        for j in range(0, len(matrix)):
            if(matrix[i][j] != 0):
                result[i].append((matrix[i][j], j))
    return result


def BFS(matrix, start, end):
    """
    BFS algorithm
     Parameters:
    ---------------------------
    matrix: np array
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node

    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node,
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO:
    path = []
    visited = {}
    queue = [[start]]  # store all path

    adjMatrix = convertMatrixToAdjacencyMatrixDict(matrix)

    if start == end: #Start equal end
        return

    while queue:
        path = queue.pop(0)  # pop the first path in the queue
        node = path[-1]  # get the last node in the path
        if node not in visited:
            # add the node to the visited dictionary
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None

            if node == end:  # finish
                break

            for neighbor in adjMatrix[node]:
                if neighbor not in visited:
                    newPath = path+[neighbor]
                    queue.append(newPath)

    return visited, path


def DFS(matrix, start, end):
    """
    DFS algorithm:
    Parameters:
    ---------------------------
    matrix: np array
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node

    Returns
    ---------------------
    visited
        The dictionary contains visited nodes, each key is a visited node,
        each value is the adjacent node visited before it.
    path: list
        Founded path
    """
    # TODO:
    path = []
    visited = {}
    stack = [[start]]  # store all path

    adjMatrix = convertMatrixToAdjacencyMatrixDict(matrix)

    if start == end: #start equal end
        return visited, path

    while stack:
        path = stack.pop(0)  # pop the first path in the stack
        node = path[-1]  # get the last node in the path
        if node not in visited:

            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None

            if node == end: # finish
                break

            for n in adjMatrix[node]:
                if n not in visited:
                    stack.insert(0, path + [n])
    return visited, path


def UCS(matrix, start, end):
    """
    Uniform Cost Search algorithm
     Parameters:visited
    ---------------------------
    matrix: np array
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node

    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node,
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO:
    adjMatrix = convertMatrixToAdjacencyMatrixDictWeight(matrix)
    priQueue = PriorityQueue()
    priQueue.put((0, [start]))  # (priority, [node])

    path = []
    visited = {}
    while not priQueue.empty():

        ucs_w, path = priQueue.get()
        node = path[-1]

        if node == end:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            break

        if node not in visited:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous

            else:
                visited[node] = None
            for neighbor in adjMatrix[node]:

                if neighbor[1] not in visited:
                    newPath = path+[neighbor[1]]
                    priQueue.put((
                        ucs_w + neighbor[0],
                        newPath
                    ))
    return visited, path

def heuristic(adjMatrix, start, end):
    priQueue = PriorityQueue()
    priQueue.put((0, [start]))  # (priority, node)

    path = []
    visited = {}
    while not priQueue.empty():

        ucs_w, path = priQueue.get()
        node = path[-1]

        if node == end:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            return ucs_w
        if node not in visited:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            for neighbor in adjMatrix[node]:

                if neighbor[1] not in visited:
                    newPath = path+[neighbor[1]]
                    priQueue.put((
                        ucs_w + neighbor[0],
                        newPath
                    ))


def GBFS(matrix, start, end):
    adjMatrix = convertMatrixToAdjacencyMatrixDictWeight(matrix)
    priQueue = PriorityQueue()
    priQueue.put((0, [start]))  # (priority, node)

    path = []
    visited = {}
    while not priQueue.empty():
        priority, path = priQueue.get()
        node = path[-1]
        if node == end:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            break
        if node not in visited:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None

            for neighbor in adjMatrix[node]:
                if neighbor[1] not in visited:
                    newPath = path+[neighbor[1]]
                    priQueue.put((
                        heuristic(adjMatrix, neighbor[1], end),
                        newPath
                    ))
    return visited, path

def eclideanDistance(pos, current, goal):
    x = (pos[current][0] - pos[goal][0])**2
    y = (pos[current][1] - pos[goal][1])**2
    return math.sqrt(x+y)


def Astar(matrix, start, end, pos):
    """
    A* Search algorithm
     Parameters:
    ---------------------------
    matrix: np array UCS
        The graph's adjacency matrix
    start: integer
        starting node
    end: integer
        ending node
    pos: dictionary. keys are nodes, values are positions
        positions of graph nodes
    Returns
    ---------------------
    visited
        The dictionary contains visited nodes: each key is a visited node,
        each value is the key's adjacent node which is visited before key.
    path: list
        Founded path
    """
    # TODO:
    adjMatrix = convertMatrixToAdjacencyMatrixDictWeight(matrix)
    priQueue = PriorityQueue()
    priQueue.put((0, [start]))  # (priority, node)

    path = []
    visited = {}
    while not priQueue.empty():
        priority, path = priQueue.get()
        node = path[-1]
        if node == end: #finish
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            break

        if node not in visited:
            if path[:-1]:
                for previous, current in zip(path, path[1:]):
                    if current == node:
                        visited[node] = previous
            else:
                visited[node] = None
            for neighbor in adjMatrix[node]:

                if neighbor[1] not in visited:
                    newPath = path+[neighbor[1]]
                    priQueue.put((
                        eclideanDistance(pos, neighbor[1], end) +
                        heuristic(adjMatrix, start, neighbor[1]),
                        newPath
                    ))
    return visited, path
