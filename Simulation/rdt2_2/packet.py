class Packet():
    def __init__(self, seqnum, data):
        self.seqnum = seqnum
        self.data = data
        self.state = True        


class ACK():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True 


class ResendPacket():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True  
