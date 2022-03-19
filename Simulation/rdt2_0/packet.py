class Packet():
    seqnum = 0
    def __init__(self, data):
        Packet.seqnum += 1
        self.data = data
        self.state = True        


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
