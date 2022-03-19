class Packet():
    seqnum = 0
    def __init__(self, data):
        Packet.seqnum += 1
        self.data = data


class ACK():
    def __init__(self, packet_num):
        self.packet_num = packet_num
