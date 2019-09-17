from globals import *

class Chunk() :
    def __init__(self, x,y) :
        self.x = x
        self.y = y

        self.block_data = [0] * 16
        for i in range(16) :
            self.block_data[i] = [0] * 256
            for i in range(256) :
                self.block_data[i] = [0] * 16

    def set_section(self, section_id, section_block_array) :
        return
