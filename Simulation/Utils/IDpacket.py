class IDPacket():
    id = 0
    def __init__(self):
        self.seqnum = 0
        self.state = True   
        self.id = IDPacket.id
        IDPacket.id += 1


    def setSeqnum(self, newSeqnum):
        if newSeqnum == 0 or newSeqnum == 1:
            self.seqnum = newSeqnum

    def resetId():
        IDPacket.id = 0    


class IDACK(IDPacket):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True 
        self.id = id


class IDNAK(IDPacket):
    def __init__(self, seqnum, id):
        self.id = id
        self.seqnum = seqnum
        self.state = True


class IDResendPacket(IDPacket):
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True  
        self.id = id