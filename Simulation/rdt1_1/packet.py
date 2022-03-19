class Packet():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True


class DataPacket(Packet):   
    def __init__(self, seqnum, data):
        self.data = data
        super().__init__(seqnum)

class ACK(Packet):
    def __init__(self, seqnum):
        super().__init__(seqnum)


class NAK(Packet):
    def __init__(self, seqnum):
        super().__init__(seqnum)

class ResendPacket(Packet):
    def __init__(self, seqnum):
        super().__init__(seqnum)
