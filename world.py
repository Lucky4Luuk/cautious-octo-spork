from globals import *

class World() :
    def __init__(self) :
        #Create 2D array of size 4096x4096
        self.chunks = [None] * 4096
        for i in range(4096) :
            self.chunks[i] = [None] * 4096
        #Center is at 2048, 2048

    def set_chunk(self, x,z, chunk) :
        # print("Chunk stored at {}; {}".format(x,z))
        self.chunks[x + 2048][z + 2048] = chunk

    def get_chunk(self, x,z) :
        return self.chunks[x + 2048][z + 2048]
