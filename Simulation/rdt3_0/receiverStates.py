from Simulation.rdt3_0.state import State


class Waiting(State):
    def __init__(self, seqnum):
        super(Waiting, self).__init__('Waiting', seqnum)


class Receiving(State):
    def __init__(self, seqnum):
        self.seqnum = seqnum
        super(Receiving, self).__init__('Receiving', seqnum)
