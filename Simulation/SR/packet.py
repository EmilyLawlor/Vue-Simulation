class Packet():
    seqnum = 1
    def __init__(self, data):
        self.seqnum = Packet.seqnum
        self.data = data
        self.state = True   
        Packet.seqnum += 1 


class ACK(Packet):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True 


class ResendPacket(Packet):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  
