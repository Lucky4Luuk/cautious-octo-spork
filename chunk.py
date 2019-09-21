from globals import *

class Chunk() :
    def __init__(self, x,z) :
        self.x = x
        self.z = z

        self.processed = False
        self.block_updates = []

        self.block_data = [0] * 16
        for i in range(16) :
            self.block_data[i] = [0] * 256
            for j in range(256) :
                self.block_data[i][j] = [0] * 16

    def set_section(self, section_id, section_block_array) :
        global REGISTRY

        #block_array stores the blocks as x,z,y
        for x in range(16) :
            for y in range(16) :
                for z in range(16) :
                    idx = x + y * 16 + z * 16 * 16
                    if section_block_array[idx] :
                        block = section_block_array[idx]
                        # if block > 0 :
                        #     print("{};{};{} - {}".format(x,z + section_id * 16,y, REGISTRY.decode_block(val=block)))

                        self.block_data[x][z + section_id * 16][y] = block

    # def __getitem__(self, n) :
    #     return self.block_data[n]

    def get_block_id(self, x,y,z) :
        return self.block_data[x][y][z]

    def get_block(self, x,y,z) :
        return REGISTRY.decode_block(self.block_data[x][y][z])

    def set_block_id(self, x,y,z, id) :
        if self.processed :
            self.block_data[x][y][z] = id
        else :
            self.block_updates.append([x,y,z, id])

    def set_block(self, x,y,z, block) :
        id = REGISTRY.encode_block(block)
        if self.processed :
            self.block_data[x][y][z] = id
        else :
            self.block_updates.append([x,y,z, id])

    def process_block_updates(self) :
        for update in self.block_updates :
            self.set_block_id(update[0], update[1], update[2], update[3])
