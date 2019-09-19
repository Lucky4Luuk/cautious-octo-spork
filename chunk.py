from globals import *

class Chunk() :
    def __init__(self, x,z) :
        self.x = x
        self.z = z

        self.block_data = [0] * 16
        for i in range(16) :
            self.block_data[i] = [0] * 256
            for j in range(256) :
                self.block_data[i][j] = [0] * 16

    def set_section(self, section_id, section_block_array) :
        global REGISTRY

        # rust_chunk = rust2py.RustChunk(0,0)
        # # print(rust_chunk.get_block_data())
        # # print(type( rust_chunk.get_block_data() ))
        # # block_array = BlockArray.empty(REGISTRY)
        # print(rust_chunk.set_section(section_id, section_block_array))

        #print("Section {}".format(section_id))
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
        self.block_data[x][y][z] = id

    def set_block(self, x,y,z, block) :
        self.block_data[x][y][z] = REGISTRY.encode_block(block)
