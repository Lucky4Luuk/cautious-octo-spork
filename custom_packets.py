from globals import *

from minecraft.networking.packets import (
    Packet, AbstractKeepAlivePacket, AbstractPluginMessagePacket
)

from minecraft.networking.types import *

#https://github.com/ammaraskar/pyCraft/issues/55

def add_play_packets(func):
    def wrap(func,context):
        packets=func(context)
        # packets.add(ChunkSectionDataPacket)
        packets.add(ChunkColumnDataPacket)
        return packets
    return staticmethod(lambda x:wrap(func,x))
PlayingReactor.get_clientbound_packets=add_play_packets(PlayingReactor.get_clientbound_packets)

#Found here: https://github.com/ammaraskar/pyCraft/issues/130#issuecomment-500292517
# class ChunkSectionDataPacket(Packet):
#     id = 0x22
#
#     packet_name = 'chunk data'
#
#     def read(self, file_object):
#         # '''
#         #     A chunk is 16x256x16 (x y z) blocks.
#         #     Each chunk has 16 chunk sections where each section represents 16x16x16 blocks.
#         #     The number of chunk sections is equal to the number of bits set in Primary Bit Mask.
#         #
#         #     Chunk:
#         #        Section:
#         #           Block Data:    2 bytes per block. Total 8192 bytes. format: blockId << 4 | meta
#         #           Emitted Light: 4 bits per block (1/2 byte). Total 2048 bytes
#         #           Skylight:      4 bits per block (1/2 byte). Total 2048 bytes (only included in overworld)
#         #        Biome: 1 byte per block column. 256 bytes. (only included if all sections are in chunk)
#         # '''
#         # self.chunk_x = Integer.read(file_object)
#         # self.chunk_z = Integer.read(file_object)
#         # self.full = Boolean.read(file_object)
#         #
#         # if self.context.protocol_version >= 107:
#         #     self.mask = VarInt.read(file_object)
#         # else:
#         #     self.mask = UnsignedShort.read(file_object)
#         #
#         # # size of data in bytes
#         # self.data_size = VarInt.read(file_object)
#
#         print("Received package of id 0x22")

class ChunkColumnDataPacket(Packet):
    id = 0x21

    packet_name = 'chunk column data'

    def read(self, file_object) :
        self.file_object = file_object

    def _read(self, file_object):
        # raw_data = file_object.read()
        # block_data_size = 8
        # tmp = ""
        # file = open("raw_chunk_data.txt", "w+")
        # for i in range(len(raw_data)) :
        #     file.write(str(raw_data[i]) + "; ")
        #     if i%16 == 15 :
        #         file.write("\n\n")
        # file.close()

        chunk_x = Integer.read(file_object)
        chunk_z = Integer.read(file_object)

        full_chunk = Boolean.read(file_object) #full = true means new chunk, full = false means chunk update

        primary_bit_mask = VarInt.read(file_object)

        heightmaps = file_object.read(288 + 21) #256 entries at 9 bits per entry, so 288 bytes of data

        data_size = VarInt.read(file_object)

        data = file_object.read(data_size)
        # data = []
        # for i in range(data_size) :
        #     data.append()
        # data = TrailingByteArray.read(file_object)
        # data = ShortPrefixedByteArray.read(file_object, data_size)

        #print(file_object.read())

        #block_entities_count = VarInt.read(file_object)

        file = open("raw_chunk_data.txt", "wb")
        file.write(heightmaps)
        file.close()

        print("Loading chunk at {}; {}".format(chunk_x, chunk_z))
        print("Chunk data:")
        print(str(full_chunk))
        print(str(primary_bit_mask))
        #print(" - " + str(heightmaps))
        print(str(data_size))
        #print(str(data))
        #print(str(block_entities_count))

        #block_count = Short.read(file_object)
        #print(block_count)

        #print("Done writing data")

        # self.skylight = Boolean.read(file_object)
        # columns = VarInt.read(file_object)
        # self.chunk_columns = []
        # for i in range(columns):
        #     record = ChunkDataPacket.read(file_object)
        #     self.chunk_columns.append(record)

        #sys.exit()
    #
    # def write_fields(self, packet_buffer):
    #     Boolean.send(self.skylight, packet_buffer)
    #     Integer.send(len(self.chunk_columns), packet_buffer)
    #     for chunk_column in self.chunk_columns:
    #         chunk_column.write_fields(packet_buffer)
