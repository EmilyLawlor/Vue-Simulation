class Packet():
    seqnum = 0
    def __init__(self, data='data'):
        Packet.seqnum += 1
        self.data = data
        self.state = True    

    def resetSeqnum(self):
        Packet.seqnum = 0    


class ACK():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  


class NAK():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  

class ResendPacket():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  
