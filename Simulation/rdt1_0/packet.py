class Packet():
    seqnum = 0
    def __init__(self, data='data'):
        Packet.seqnum += 1
        self.data = data

    
    def resetSeqnum(self):
        Packet.seqnum = 0


class ACK():
    def __init__(self, packet_num):
        self.packet_num = packet_num
