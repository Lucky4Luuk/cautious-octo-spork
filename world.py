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
        self.set_chunk(chunk.x, chunk.z, chunk)
        self.chunk_queu.append([chunk, bitmask, buf])

    def process_chunk(self, chunk, bitmask, buf) :
        try :
            for sectionY in range(16) :
                if (bitmask & (1 << sectionY)) != 0 :
                    section = buf.unpack_chunk_section()
                    chunk.set_section(sectionY, section)
        except Exception as e :
            print(e)

        chunk.processed = True
        chunk.process_block_updates()
        # self.set_chunk(chunk.get_x(), chunk.get_z(), chunk)
        self.chunks[chunk.x + 2048][chunk.z + 2048].block_data = chunk.block_data
        #print("Chunk done")

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

    def get_blocks_in_radius(self, x,y,z, radius, square=True) :
        if square :
            block_data = [0] * (radius * 2 + 1)
            for i in range(radius * 2 + 1) :
                block_data[i] = [0] * (radius * 2 + 1)
                for j in range(radius * 2 + 1) :
                    block_data[i][j] = [0] * (radius * 2 + 1)

            min_x = x - radius  ; chunk_x_min = math.floor(min_x / 16)
            max_x = x + radius+1; chunk_x_max = math.floor(max_x / 16)
            min_y = y - radius
            max_y = y + radius+1
            min_z = z - radius  ; chunk_z_min = math.floor(min_z / 16)
            max_z = z + radius+1; chunk_z_max = math.floor(max_z / 16)

            chunk_x = chunk_x_min
            chunk_z = chunk_z_min

            for ix in range(min_x, max_x) :
                if ix % 16 == 16 :
                    chunk_x += 1
                for iz in range(min_z, max_z) :
                    if iz % 16 == 16 :
                        chunk_z += 1
                    for iy in range(min_y, max_y) :
                        cur_chunk = self.get_chunk(chunk_x, chunk_z)
                        if cur_chunk and cur_chunk.processed :
                            block_data[ix - min_x][iy - min_y][iz - min_z] = cur_chunk.get_block_id(ix % 16, iy % 16, iz % 16)
            return block_data

        else :
            raise Exception()
