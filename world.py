from globals import *

class World() :
    def __init__(self) :
        #Create 2D array of size 4096x4096
        self.chunks = [None] * 4096
        for i in range(4096) :
            self.chunks[i] = [None] * 4096
        #Center is at 2048, 2048

        #Dictionary for entities
        self.entities = {}

        #Dictionary for players
        self.players = {}

    def set_chunk(self, x,z, chunk) :
        # print("Chunk stored at {}; {}".format(x,z))
        self.chunks[x + 2048][z + 2048] = chunk

    def get_chunk(self, x,z) :
        return self.chunks[x + 2048][z + 2048]

    def chunk_set_block_id(self, x,z, bx,by,bz, block_id) :
        self.chunks[x + 2048][z + 2048].set_block_id(bx,by,bz, block_id)

    def chunk_set_block(self, x,z, bx,by,bz, block) :
        self.chunks[x + 2048][z + 2048].set_block(bx,by,bz, block)

    def add_player(self, uuid, name, gamemode, ping) :
        self.players[uuid] = {
                                "name": name,
                                "gamemode": gamemode,
                                "ping": ping
                             }

    def remove_player(self, uuid) :
        self.players.pop(uuid)

    def get_player(self, uuid) :
        return self.players[uuid]

    def get_player_count(self) :
        return len(self.players)
