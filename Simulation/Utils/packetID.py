class PacketID():
    id = 0
    def __init__(self):
        self.seqnum = 0
        self.state = True   
        self.id = PacketID.id
        PacketID.id += 1


    def setSeqnum(self, newSeqnum):
        if newSeqnum == 0 or newSeqnum == 1:
            self.seqnum = newSeqnum

    def resetId():
        PacketID.id = 0    


class ACKID(PacketID):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.id = id
        self.state = True


class NAKID(PacketID):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.id = id
        self.state = True


class ResendPacketID(PacketID):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.id = id
        self.state = True