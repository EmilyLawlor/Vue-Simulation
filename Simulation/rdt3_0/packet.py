class Packet():
    def __init__(self, data):
        self.seqnum = 0
        self.data = data
        self.state = True    


class ACK(Packet):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True 


class ResendPacket(Packet):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  
