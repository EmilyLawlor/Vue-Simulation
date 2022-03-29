class Packet():
    id = 0
    def __init__(self, seqnum, data):
        self.seqnum = seqnum
        self.data = data
        self.state = True    
        self.id = Packet.id
        Packet.id += 1
        

    def resetId():
        Packet.id = 0    


class ACK():
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True 
        self.id = id


class ResendPacket():
    def __init__(self, seqnum, id):
        self.seqnum = seqnum
        self.state = True  
        self.id = id
