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

class ChunkColumnDataPacket(Packet):
    id = 0x21

    packet_name = 'chunk column data'

    def read(self, file_object) :
        self.file_object = file_object
