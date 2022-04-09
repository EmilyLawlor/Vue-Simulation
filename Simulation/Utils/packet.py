class Packet():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True   


class ACK(Packet):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True 
