class Packet():
    def __init__(self, seqnum):
        self.seqnum = seqnum
        self.state = True


class DataPacket(Packet):   
    id = 0
    def __init__(self, seqnum, data):
        self.data = data
        self.id = DataPacket.id
        super().__init__(seqnum)
        DataPacket.id += 1

    def resetId():
        DataPacket.id = 0

class ACK(Packet):
    def __init__(self, seqnum, id):
        self.id = id
        super().__init__(seqnum)


class NAK(Packet):
    def __init__(self, seqnum, id):
        self.id = id
        super().__init__(seqnum)

class ResendPacket(Packet):
    def __init__(self, seqnum, id):
        self.id = id
        super().__init__(seqnum)
