import math

def distance(a, b) :
    return math.sqrt((a.pos[0] - b.pos[0])**2 + (a.pos[1] - b.pos[1])**2 + (a.pos[2] - b.pos[2])**2)

class Node() :
    def __init__(self, x,y,z, type, g_score=math.inf, prev_node=None) :
        self.pos = [x,y,z]
        self.type = type
        self.g_score = g_score
        self.prev_node = prev_node

class AStar() :
    def __init__(self, start_node=None, end_node=None) :
        self.nodes = []
        self.open_set = []
        self.closed_set = []
        self.start_node = start_node
        self.end_node = end_node

    def _get_lowest_f_cost(self) :
        lowest_node = None

    def _nodes_equal(self, a,b) :
        return a.pos[0] == b.pos[0] and a.pos[1] == b.pos[1] and a.pos[2] == b.pos[2]# and a.type == b.type

    def _remove_node_open(self, node) :
        self.open_set = [item for item in self.open_set if self._nodes_equal(node, item) == False]

    def _remove_node_closed(self, node) :
        self.closed_set = [item for item in self.closed_set if self._nodes_equal(node, item) == False]

    def _node_in_open(self, node) :
        for item in self.open_set :
            if self._nodes_equal(node, item) :
                return True
        return False

    def _node_in_closed(self, node) :
        for item in self.closed_set :
            if self._nodes_equal(node, item) :
                return True
        return False

    def _is_neighbour(self, node, item) :
        for i in range(-1,2) :
            for j in range(-1,2) :
                for k in range(-1,2) :
                    if i != 0 and j != 0 and k != 0 :
                        if node.pos[0] + i == item.pos[0] and node.pos[1] + j == item.pos[1] and node.pos[2] + k == item.pos[2] :
                            return True
        return False

    def _get_neighbours(self, node) :
        neighbours = []
        for item in self.nodes :
            if self._is_neighbour(node, item) :
                neighbours.append(item)
        return neighbours

    def step(self) :
        current = self._get_lowest_f_cost()
        if current.type == "goal" :
            return current

        self._remove_node_open(current)
        self.closed_set.append(current)

        neighbours = self._get_neighbours(current)
        for neighbour in neighbours :
            tentative_g_score = neighbour.g_score + math.floor(distance(current, neighbour) * 10)
            if self._node_in_closed(neighbour) and tentative_g_score >= neighbour.g_score :
                continue

            if (not self._node_in_open(neighbour)) or tentative_g_score < neighbour.g_score :
                neighbour.prev_node = current
                neighbour.g_score = tentative_g_score
                neighbour.f_score = tentative_g_score + math.floor(distance(neighbour, self.start_node) * 10)
                if not self._node_in_open(neighbour) :
                    self.open_set.append(neighbour)

    def new_path(self, start_node, end_node) :
        self.start_node = start_node
        self.end_node = end_node
