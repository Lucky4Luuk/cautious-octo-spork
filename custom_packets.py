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
