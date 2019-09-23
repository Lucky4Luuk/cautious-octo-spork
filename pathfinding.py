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

    def old_get_node_lowest_f_cost(self) :
        if len(self.nodes) > 0 :
            min_f_node = self.nodes[0]
            for node in self.nodes :
                f_cost = node[3]
                if f_cost < min_f_node[3] :
                    min_f_node = node
            return node
        return None

    def get_node_lowest_f_cost(self) :
        best_node = None
        best_idx = -1
        # for x in range(len(self.nodes)) :
        #     for y in range(len(self.nodes[0])) :
        #         for z in range(len(self.nodes[0][0])) :
        #             node = self.nodes[x][y][z]
        #             if node["allowed"] and node["visited"] == False :
        #                 if best_node == None :
        #                     best_node = node
        #                 else :
        #                     if node["f_cost"] < best_node["f_cost"] :
        #                         best_node = node
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

    def _process_neighbour_chunks(self, node) :
        node_x = node["pos"][0]
        node_y = node["pos"][1]
        node_z = node["pos"][2]

        for i in range(-1,2) :
            for j in range(-1,2) :
                for k in range(-1,2) :
                    #Not the node itself
                    if i != 0 and j != 0 and k != 0 and node_x+i >= 0 and node_x+i < len(self.nodes)-1 and node_y+j >= 0 and node_y+j < len(self.nodes[0])-1 and node_z+k >= 0 and node_z+k < len(self.nodes[0][0])-1 :
                        #This node is available for pathfinding
                        print(self.nodes[node_x+i][node_y+j][node_z+k])
                        if self.nodes[node_x+i][node_y+j][node_z+k]["allowed"] :
                            g_cost = node["g_cost"] + math.floor(length([i,j,k]) * 10)
                            f_cost = get_h_cost(self.end_point, node["pos"]) + g_cost
                            if self.nodes[node_x+i][node_y+j][node_z+k]["visited"] :
                                if f_cost < self.nodes[node_x+i][node_y+j][node_z+k]["f_cost"] :
                                    self.nodes[node_x+i][node_y+j][node_z+k]["f_cost"] = f_cost
                                    self.nodes[node_x+i][node_y+j][node_z+k]["g_cost"] = g_cost
                                    self.nodes[node_x+i][node_y+j][node_z+k]["prev_node"] = node["pos"]
                                    # self.node_queu.append(self.nodes[node_x+i][node_y+j][node_z+k])
                            else :
                                self.nodes[node_x+i][node_y+j][node_z+k]["f_cost"] = f_cost
                                self.nodes[node_x+i][node_y+j][node_z+k]["g_cost"] = g_cost
                                self.nodes[node_x+i][node_y+j][node_z+k]["prev_node"] = node["pos"]
                                self.nodes[node_x+i][node_y+j][node_z+k]["visited"] = True
                                self.node_queu.append(self.nodes[node_x+i][node_y+j][node_z+k])
                                print("Added a node!")

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
            return {"allowed": True, "start":False, "end":False, "visited": False, "pos": [x,y,z], "f_cost": 0, "g_cost": 0, "prev_node": [0,0,0]}
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

    #TODO:  when self.reached_end is set to True, also store the previous node as the last node.
    #       then use this to get the path and spawn armor stands here for visualization
    def calculate_path(self, start_point, end_point, block_data) :
        self.nodes = []
        self.node_queu = []
        self._block_data_to_nodes(block_data)
        self.nodes[start_point[0]][start_point[1]][start_point[2]]["start"] = True
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

    def step(self) :
        if self.reached_end == False :
            best_node, best_idx = self.get_node_lowest_f_cost()
            if best_node :
                self.node_queu.pop(best_idx)
                pos = best_node["pos"]
                print(best_node)
                if best_node["end"] :
                    self.reached_end = True
                    print("We did it!")
                elif best_node["visited"] == False :
                    self._process_neighbour_chunks(best_node)
            else :
                print("Uhh?")
                self.reached_end = True
        else :
            print("Done!")
            sys.exit(0)
