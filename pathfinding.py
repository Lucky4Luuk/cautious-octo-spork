from globals import *

#G cost: distance from starting node
#H cost: distance from end node
#F cost: G cost + H cost
#Algorithm keeps track of all nodes. It always works from the node with the lowest F cost

def length(a) :
    return math.sqrt(a[0]**2 + a[1]**2 + a[2]**2)

def distance(a, b) :
    return math.sqrt(distance2(a,b))

def distance2(a, b) :
    return (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2

def get_g_cost(start_point, cur_point) :
    return math.floor(distance(cur_point, start_point) * 10)

def get_h_cost(end_point, cur_point) :
    return math.floor(distance(cur_point, end_point) * 10)

def get_f_cost(start_point, end_point, cur_point) :
    return get_g_cost(start_point, cur_point) + get_h_cost(end_point, cur_point)

class AStar() :
    def __init__(self) :
        self.nodes = []
        self.start_point = [0,0,0]
        self.end_point = [1,0,0]

    def get_node_lowest_f_cost(self) :
        best_node = None
        best_idx = -1

        idx = 0
        for node in self.node_queu :
            if best_node :
                if node["f_cost"] < best_node["f_cost"] :
                    best_node = node
                    best_idx = idx
            else :
                best_node = node
                best_idx = idx
            idx += 1
        return best_node, best_idx

    def _get_neighbours(self, x,y,z) :
        neighbours = []
        for i in range(-1,2) :
            for j in range(-1,2) :
                for k in range(-1,2) :
                    if i != 0 and j != 0 and k != 0 :
                        if x+i >= 0 and y+j >= 0 and z+k >= 0 and x+i < len(self.nodes)-1 and y+j < len(self.nodes[0])-1 and z+k < len(self.nodes[0][0])-1 :
                            node = self.nodes[x+i][y+j][z+k]
                            if node["allowed"] :
                                neighbours.append(node)
        return neighbours

    def _block_allowed(self, block_data, x,y,z) :
        if y > 0 :
            if y < len(block_data[0])-2 :
                if block_data[x][y-1][z] > 0 :# and block_data[x][y][z] == 0 : #and block_data[x][y+1][z] == 0 :
                    return True
            else :
                if y == len(block_data[0]) - 1 : #Build limit. Might be 1 block under build limit tho lol
                    return False #Let's not yet give it the go single for this lol. Still need to look into this

        return False

    def _get_new_node(self, block_data, x,y,z) :
        if self._block_allowed(block_data, x,y,z) :
            return {"allowed": True, "start":False, "end":False, "visited": False, "pos": [x,y,z], "f_cost": math.inf, "g_cost": math.inf, "prev_node": None}
        return {"allowed": False, "pos": [x,y,z]}

    def _block_data_to_nodes(self, block_data) :
        block_data_size_x = len(block_data)
        block_data_size_y = len(block_data[0])
        block_data_size_z = len(block_data[0][0])

        self.nodes = [0] * block_data_size_x
        for x in range(block_data_size_x) :
            self.nodes[x] = [0] * block_data_size_y
            for y in range(block_data_size_y) :
                # self.nodes[x][y] = [self._get_new_node(block_data, x,y,z) for z in range(block_data_size_z)]
                self.nodes[x][y] = [0] * block_data_size_z

        for x in range(block_data_size_x) :
            for y in range(block_data_size_y) :
                for z in range(block_data_size_z) :
                    self.nodes[x][y][z] = self._get_new_node(block_data, x,y,z)

    def _is_in_queu(self, node) :
        for n in self.node_queu :
            if node["pos"][0] == n["pos"][0] and node["pos"][1] == n["pos"][1] and node["pos"][2] == n["pos"][2] :
                return True
        return False

    def calculate_path(self, start_point, end_point, block_data) :
        self.nodes = []
        self.node_queu = []
        self._block_data_to_nodes(block_data)
        self.nodes[start_point[0]][start_point[1]][start_point[2]]["start"] = True
        self.nodes[start_point[0]][start_point[1]][start_point[2]]["visited"] = True
        self.nodes[start_point[0]][start_point[1]][start_point[2]]["g_cost"] = 0
        self.nodes[start_point[0]][start_point[1]][start_point[2]]["f_cost"] = 0
        print("Start: "+str(self.nodes[start_point[0]][start_point[1]][start_point[2]]))
        self.nodes[end_point[0]][end_point[1]][end_point[2]]["end"] = True
        print("End:   "+str(self.nodes[end_point[0]][end_point[1]][end_point[2]]))
        self.start_point = start_point
        self.end_point = end_point
        self.block_data = block_data
        self.max_block_data_idx = len(self.block_data[0])

        # self._process_neighbour_chunks(self.nodes[start_point[0]][start_point[1]][start_point[2]])
        self.node_queu.append(self.nodes[start_point[0]][start_point[1]][start_point[2]])
        self.reached_end = False

        self.last_node_processed = self.nodes[start_point[0]][start_point[1]][start_point[2]]

    def step(self) :
        if len(self.node_queu) > 0 :
            cur_node, idx = self.get_node_lowest_f_cost()
            if cur_node :
                # print(cur_node)
                if cur_node["end"] :
                    print("We did it boys")
                    self.reached_end = True
                    # sys.exit(0)
                    return True
                self.nodes[cur_node["pos"][0]][cur_node["pos"][1]][cur_node["pos"][2]]["visited"] = True
                self.last_node_processed = self.nodes[cur_node["pos"][0]][cur_node["pos"][1]][cur_node["pos"][2]]
                self.node_queu.pop(idx)
                neighbours = self._get_neighbours(cur_node["pos"][0], cur_node["pos"][1], cur_node["pos"][2])
                for node in neighbours :
                    if node["visited"] :
                        continue
                    tentative_g_cost = cur_node["g_cost"] + math.floor(distance(cur_node["pos"], node["pos"])*10)
                    if tentative_g_cost < node["g_cost"] :
                        node["g_cost"] = tentative_g_cost
                        node["f_cost"] = tentative_g_cost + get_h_cost(self.end_point, node["pos"])
                        node["prev_node"] = cur_node["pos"]
                        self.nodes[node["pos"][0]][node["pos"][1]][node["pos"][2]] = node
                        if not self._is_in_queu(node) :
                            # print("Added a node!")
                            self.node_queu.append(node)
        else :
            self.reached_end = True
            # print(self.nodes[self.end_point[0]][self.end_point[1]][self.end_point[2]]["visited"])
            print(self.last_node_processed)
            print("Done! Somehow we didn't reach the end.")
            # sys.exit(0)
