from Simulation.rdt2_2.state import State


class Waiting(State):
    def __init__(self, seqnum):
        super(Waiting, self).__init__('Waiting', seqnum)


class Sending(State):
    def __init__(self, seqnum):
        super(Sending, self).__init__('Sending', seqnum)
