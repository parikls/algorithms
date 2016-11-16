import queue


class Vertex:
    """
    helper class for BFS and DFS algorithms which
    stores coordinates of current vertex and its "father"
    """

    def __init__(self, coords, father=None):
        self.coords = coords
        self.father = father

    def get_path(self):
        """
        Return path from current vertex to root vertex
        """
        path = []
        path.append(self.coords)
        father = self.father
        while father is not None:
            path.append(father.coords)
            father = father.father
        path.reverse()
        return path

    def get_neighbours(self, lab):
        """Assuming that we can't travel in diagonals"""
        neighbours = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                neihbour_coord = (self.coords[0] + i, self.coords[1] + j,)
                # choose only vertical or horizontal neighbours
                if (neihbour_coord[0] == self.coords[0] or neihbour_coord[1] == self.coords[1]) \
                        and neihbour_coord != self.coords:

                    neighbours.append(neihbour_coord)
        return neighbours

    def __eq__(self, other):
        return self.coords == other.coords

    def __str__(self):
        return "Coords={}; ".format(self.coords)


class VertexAStar(Vertex):
    """
    Vertex for A* algorithm must implement 3 new fields:
    g - length from start vertex to current vertex. Initially it will be equals to 0,
        On each loop iteration it will be equals to father.g + cost of move from
        previous point to current point. For vertical and horizontal moves cost will be 10.
        For diagonal moves - 14 (sqrt(2) * 10)
    h - approximate cost of path to end point using only vertical and horizontal moves
    f - sum of g and h

    """
    DEFAULT_MOVE_COST = 10

    def __init__(self, coords, father=None):
        super(VertexAStar).__init__(coords, father)
        if father:
            # assuming that we have only horizontal and vertical moves, cost for move always will be 10
            self.g = father.g + self.DEFAULT_MOVE_COST
        else:
            self.g = 0
        self.h = None
        self.f = None

    def calculate_h(self, end_coords):
        horizontal_path_cost = abs(end_coords[0] - self.coords[0])
        vertical_path_cost = abs(end_coords[1] - self.coords[1])
        self.h = (horizontal_path_cost + vertical_path_cost) * self.DEFAULT_MOVE_COST

    def calculate_f(self):
        self.f = self.g + self.h

    def __str__(self):
        return super(VertexAStar).__str__() + "g={}; h={}; f={}".format(self.g, self.h, self.f)


def bfs(lab, start_coord, end_coord):
    # we will store our next edges in FIFO queue
    q = queue.Queue()
    start_edge = Vertex(start_coord)
    q.put(start_edge)

    # already visited edges
    visited = []

    while not q.empty():
        current_edge = q.get()

        if current_edge.coords == end_coord:
            # we have found our path
            return current_edge.get_path()

        if current_edge.coords in visited:
            continue

        neighbours = current_edge.get_neighbours(lab)
        for n in neighbours:
            # if we haven't been here yet, and there is not wall
            if n not in visited and lab[n[0]][n[1]] != 1:
                n_edge = Vertex(n)
                n_edge.father = current_edge
                q.put(n_edge)
        visited.append(current_edge.coords)


def dfs(lab, start_coord, end_coord):
    # for DFS purposes we should store next edged in LIFO queue
    q = queue.LifoQueue()

    start_edge = Vertex(start_coord)
    q.put(start_edge)

    # already visited edges
    visited = []

    while not q.empty():
        current_edge = q.get()

        if current_edge.coords == end_coord:
            # we have found our path
            return current_edge.get_path()

        neighbours = current_edge.get_neighbours(lab)
        for n in neighbours:
            # if we haven't been here yet, and there is not wall
            if n not in visited and lab[n[0]][n[1]] != 1:
                n_edge = Vertex(n)
                n_edge.father = current_edge
                q.put(n_edge)
        visited.append(current_edge.coords)


def a_star(lab, start_coord, end_coord):
    # we cannot pick queue for this task, because after each iteration we must sort our
    # list, to pick most suitable vertex with lowest F
    opened = []
    closed = []

    start_edge = VertexAStar(start_coord)
    opened.append(start_edge)

    while opened:

        # sort by lowest f
        opened.sort(key=lambda vertex: vertex.f)
        # pick vertex with lowest f
        current_edge = opened.pop(0)
        if current_edge.coords == end_coord:
            # path found !
            return current_edge.get_path()

        if current_edge.coords in closed:
            continue

        neighbours = current_edge.get_neighbours(lab)
        for n in neighbours:
            # if we haven't been here and this is not a wall
            if n not in closed and lab[n[0]][n[1]] != 1:
                neighbour_edge = VertexAStar(coords=n, father=current_edge)
                neighbour_edge.calculate_h(end_coord)
                neighbour_edge.calculate_f()
                opened.append(neighbour_edge)

        closed.append(current_edge.coords)


def main():
    # labyrinth is taken from CheckIO task
    labirynths = [
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
            [1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ],
        [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    ]

    start_coord = (1, 1,)
    end_coord = (10, 10,)

    for lab in labirynths:

        print("Breadth first search: ", bfs(lab, start_coord, end_coord))
        print("Depth first search:   ", dfs(lab, start_coord, end_coord))
        print("A*:                   ", a_star(lab, start_coord, end_coord))
        print("="*100)


if __name__ == '__main__':
    main()
