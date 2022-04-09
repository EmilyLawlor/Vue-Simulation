class Packet():
    id = 0
    def __init__(self, data):
        self.seqnum = 0
        self.data = data
        self.state = True   
        self.id = Packet.id
        Packet.id += 1


    def setSeqnum(self, newSeqnum):
        if newSeqnum == 0 or newSeqnum == 1:
            self.seqnum = newSeqnum

    def resetId():
        Packet.id = 0    


class ACK(Packet):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True 
        self.id = id


class ResendPacket(Packet):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True  
        self.id = id
