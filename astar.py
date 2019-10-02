from globals import *

def distance(a, b) :
    return math.sqrt((a.pos[0] - b.pos[0])**2 + (a.pos[1] - b.pos[1])**2 + (a.pos[2] - b.pos[2])**2)

class Node() :
    def __init__(self, x,y,z, type, g_score=-1, f_score=-1, prev_node=None) :
        self.pos = [x,y,z]
        self.type = type
        self.g_score = g_score
        self.f_score = f_score
        self.prev_node = prev_node

    def __repr__(self) :
        return "Node ({};{};{}) - <type: {}, g_score: {}, f_score: {}>".format(self.pos[0],self.pos[1],self.pos[2], self.type, self.g_score, self.f_score)

class Path() :
    def __init__(self, top_node, world_offset) :
        top_node.pos[0] += world_offset[0]
        top_node.pos[2] += world_offset[1]
        self.nodes = [top_node]
        while top_node.prev_node :
            top_node = top_node.prev_node
            top_node.pos[0] += world_offset[0]
            top_node.pos[2] += world_offset[1]
            self.nodes.append(top_node)

        self.nodes.reverse()

    def has_next_node(self) :
        return len(self.nodes) > 0

    def get_next_node(self) :
        next_node = self.nodes[0]
        self.nodes.pop(0)
        return next_node

class AStar() :
    def __init__(self, start_node=None, end_node=None, block_data=None) :
        self.nodes = []
        self.open_set = []
        self.closed_set = []
        self.start_node = start_node
        self.end_node = end_node
        self.block_data = block_data

    def _block_allowed(self, block_data, x,y,z) :
        if block_data[x][y][z] > 0 :
            return False
        if y > 0 :
            if y < len(block_data[0])-2 :
                if block_data[x][y-1][z] > 0 :# and block_data[x][y][z] == 0 : #and block_data[x][y+1][z] == 0 :
                    return True
            else :
                if y == len(block_data[0]) - 1 : #Build limit. Might be 1 block under build limit tho lol
                    return False #Let's not yet give it the go single for this lol. Still need to look into this

        return False

    def _block_data_to_nodes(self, block_data) :
        block_data_size_x = len(block_data)
        block_data_size_y = len(block_data[0])
        block_data_size_z = len(block_data[0][0])

        for x in range(block_data_size_x) :
            for y in range(block_data_size_y) :
                for z in range(block_data_size_z) :
                    if x != self.start_node.pos[0] or y != self.start_node.pos[1] or z != self.start_node.pos[2] :
                        if x != self.end_node.pos[0] or y != self.end_node.pos[1] or z != self.end_node.pos[2] :
                            if self._block_allowed(block_data, x,y,z) :
                                node = Node(x,y,z, "normal")
                                self.nodes.append(node)
                    #     else :
                    #         print("End node!")
                    # else :
                    #     print("Start node!")

    def _get_lowest_f_cost(self) :
        lowest_node = None
        for node in self.open_set :
            if lowest_node :
                if node.f_score < lowest_node.f_score :
                    lowest_node = node
            else :
                lowest_node = node
        return lowest_node

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
        # for i in range(-1,2) :
        #     for j in range(-1,2) :
        #         for k in range(-1,2) :
        #             if i != 0 and j != 0 and k != 0 :
        #                 if node.pos[0] + i == item.pos[0] and node.pos[1] + j == item.pos[1] and node.pos[2] + k == item.pos[2] :
        #                     return True
        dist = math.floor(distance(node, item) * 10)
        if (not self._nodes_equal(node, item)) and dist < 18 :
            return True
        return False

    def _is_neighbour_allowed(self, node, item) :
        dx = node.pos[0] - item.pos[0]
        dy = node.pos[1] - item.pos[1]
        dz = node.pos[2] - item.pos[2]
        if self.block_data[node.pos[0] - dx][node.pos[1]][node.pos[2]] > 0 :
            return False
        if self.block_data[node.pos[0]][node.pos[1] - dy][node.pos[2]] > 0 :
            return False
        if self.block_data[node.pos[0]][node.pos[1]][node.pos[2] - dz] > 0 :
            return False

        return True

    def _get_neighbours(self, node) :
        neighbours = []
        for item in self.nodes :
            if self._is_neighbour(node, item) and self._is_neighbour_allowed(node, item) :
                neighbours.append(item)
        return neighbours

    def step(self) :
        current = self._get_lowest_f_cost()
        # print("Current: {}".format(current))
        if current == None :
            print("Wtf, open set is empty?")
            return True
        self.last_node = current
        if current.type == "goal" :
            return True

        self._remove_node_open(current)
        self.closed_set.append(current)

        neighbours = self._get_neighbours(current)
        # print(len(neighbours))
        for neighbour in neighbours :
            tentative_g_score = neighbour.g_score + math.floor(distance(current, neighbour) * 10)
            if self._node_in_closed(neighbour) and tentative_g_score >= neighbour.g_score :
                continue

            if (not self._node_in_open(neighbour)) or tentative_g_score < neighbour.g_score or neighbour.g_score == -1 :
                neighbour.prev_node = current
                neighbour.g_score = tentative_g_score
                neighbour.f_score = tentative_g_score + math.floor(distance(neighbour, self.start_node) * 10)
                if not self._node_in_open(neighbour) :
                    self.open_set.append(neighbour)

    def new_path(self, start_node, end_node, block_data, block_data_offset) :
        now = time.process_time()
        print("Pathing started!")
        self.start_node = start_node
        self.end_node = end_node
        self.block_data = block_data
        self.block_data_offset = block_data_offset

        self.nodes = []
        self.open_set = []
        self.closed_set = []

        self.nodes.append(start_node)
        self.nodes.append(end_node)
        self.open_set.append(start_node)
        self.last_node = self.nodes[0]

        self._block_data_to_nodes(block_data)

        # print("{} nodes to consider...".format(len(self.nodes)))

        steps = 0
        max_steps = 1000
        result = None

        while len(self.open_set) > 0 and steps < max_steps :
            result = self.step()
            # print("Step!")
            steps += 1

        if result :
            print("Reached the end!")
            # self.last_node.pos[0] += block_data_offset[0]
            # self.last_node.pos[2] += block_data_offset[1]
            # print("Last node processed:\n{}".format(self.last_node))
        else :
            # self.last_node.pos[0] += block_data_offset[0]
            # self.last_node.pos[2] += block_data_offset[1]
            print("Somehow didn't reach the end. Last node processed:\n{}".format(self.last_node))
        # print("Reconstructing path...")
        path = Path(self.last_node, block_data_offset)
        # print("Path reconstructed!")
        print("Pathing took {}ms".format( (time.process_time() - now) * 1000 ))
        return path
        # sys.exit(0)
