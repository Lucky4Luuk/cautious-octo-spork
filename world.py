from globals import *

class World() :
    def __init__(self) :
        self.chunk_queu = []
        self.started_processing_chunks = False

        #Create 2D array of size 4096x4096
        self.chunks = [None] * 4096
        for i in range(4096) :
            self.chunks[i] = [None] * 4096
        #Center is at 2048, 2048

        #Dictionary for entities
        self.entities = {}

        #Dictionary for players
        self.players = {}

    def update(self) :
        if len(self.chunk_queu) > 0 :
            self.started_processing_chunks = True
            self.process_chunk(self.chunk_queu[0][0], self.chunk_queu[0][1], self.chunk_queu[0][2])
            self.chunk_queu.pop(0)

    def add_chunk_queu(self, chunk, bitmask, buf) :
        self.chunk_queu.append([chunk, bitmask, buf])

    def process_chunk(self, chunk, bitmask, buf) :
        try :
            for sectionY in range(16) :
                if (bitmask & (1 << sectionY)) != 0 :
                    section = buf.unpack_chunk_section()
                    chunk.set_section(sectionY, section)
        except Exception as e :
            print(e)

        self.set_chunk(chunk.get_x(), chunk.get_z(), chunk)
        print("Chunk done")

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
