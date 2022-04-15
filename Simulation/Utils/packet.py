class Packet():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True   


class ACK(Packet):
    def __init__(self, seqnum):
        super().__init__(seqnum)


class NAK(Packet):
    def __init__(self, seqnum):
        super().__init__(seqnum)
