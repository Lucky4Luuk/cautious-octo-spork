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
        #print("Section {}".format(section_id))
        i = 0
        for block in section_block_array :
            if block > 0 :
                block_z = int(i / 256)
                ii = int(i - (block_z * 256))
                block_y = int(ii / 16)
                block_x = int(ii % 16)

                if block_x == 8 and block_y + section_id * 16 == 7 and block_z == 7 :
                    print(REGISTRY.decode_block(val=block))

                #print("{}; {}; {} = {}".format(block_x, block_y, block_z, REGISTRY.decode_block(val=block)))
                self.block_data[block_x][block_y + section_id * 16][block_z] = block

            i += 1

    # def __getitem__(self, n) :
    #     return self.block_data[n]

    def get_block_id(self, x,y,z) :
        return self.block_data[x][y][z]

    def get_block(self, x,y,z) :
        return REGISTRY.decode_block(val=self.block_data[x][y][z])
